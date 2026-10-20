#!/bin/bash
# ==============================================================================
# NextPanel Autonomous Production Installer
# 100% Open, Independent & Clean Architecture
# ==============================================================================
set -e

echo -e "\033[1;34m"
cat << "EOF"
  _   _           _   _____                  _ 
 | \ | |         | | |  __ \                | |
 |  \| | _____  _| |_| |__) |_ _ _ __   ___| |
 | . ` |/ _ \ \/ / __|  ___/ _` | '_ \ / _ \ |
 | |\  |  __/>  <| |_| |  | (_| | | | |  __/ |
 |_| \_|\___/_/\_\\__|_|   \__,_|_| |_|\___|_|
EOF
echo -e "\033[0m"
echo -e "\033[1;32mStarting NextPanel Automated Installation...\033[0m\n"

if [ "$(id -u)" -ne 0 ]; then
    echo "Error: NextPanel installer must be executed as root." >&2
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_INSTALL_DIR="/usr/local/nextpanel"
ETC_DIR="/etc/nextpanel"
LOG_DIR="/var/log/nextpanel"
PORT=8443

echo "[1/6] Installing core system packages & OpenLiteSpeed repositories..."
if [ -f /etc/debian_version ]; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq git python3 python3-venv python3-pip python3-dev \
        libmysqlclient-dev pkg-config nginx mariadb-server curl wget unzip \
        openssl libssl-dev libjpeg-dev zlib1g-dev libffi-dev sudo build-essential
elif [ -f /etc/redhat-release ]; then
    dnf update -y -q
    dnf install -y -q git python3 python3-devel gcc gcc-c++ mariadb-server nginx curl wget unzip openssl \
        openssl-devel libjpeg-turbo-devel zlib-devel libffi-devel
fi

# If piped via curl | bash, clone repository to temporary setup directory
if [ ! -d "$SCRIPT_DIR/src" ]; then
    echo "Cloning NextPanel source repository..."
    TEMP_SETUP_DIR="/tmp/nextpanel-setup-$$"
    rm -rf "$TEMP_SETUP_DIR"
    git clone https://github.com/mdrealofficial/nextpanel.git "$TEMP_SETUP_DIR"
    SCRIPT_DIR="$TEMP_SETUP_DIR"
fi

echo "[2/6] Setting up NextPanel system directories & logging..."
mkdir -p "$BASE_INSTALL_DIR"
mkdir -p "$ETC_DIR/ssl"
mkdir -p "$LOG_DIR"
echo "$PORT" > "$ETC_DIR/port"

echo "[3/6] Deploying NextPanel application files..."
cp -r "$SCRIPT_DIR/src/"* "$BASE_INSTALL_DIR/"
cp -r "$SCRIPT_DIR/templates_config" "$BASE_INSTALL_DIR/"

# Setup random secure root DB password if not already present
DB_PASS_FILE="$BASE_INSTALL_DIR/etc/mysqlPassword"
mkdir -p "$BASE_INSTALL_DIR/etc"
if [ ! -f "$DB_PASS_FILE" ]; then
    DB_PASS=$(openssl rand -base64 16 | tr -dc A-Za-z0-9 | head -c 16)
    echo "$DB_PASS" > "$DB_PASS_FILE"
    chmod 600 "$DB_PASS_FILE"
fi
DB_PASSWORD=$(cat "$DB_PASS_FILE")

echo "[4/6] Initializing Database & MariaDB services..."
systemctl enable mariadb || systemctl enable mysql
systemctl start mariadb || systemctl start mysql

# Create database and grant privileges
mysql -u root -e "CREATE DATABASE IF NOT EXISTS panel CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" || true
mysql -u root -e "ALTER USER 'root'@'localhost' IDENTIFIED BY '$DB_PASSWORD'; FLUSH PRIVILEGES;" || true

if [ -f "$SCRIPT_DIR/panel_db.sql" ]; then
    mysql -u root -p"$DB_PASSWORD" panel < "$SCRIPT_DIR/panel_db.sql" || true
fi

echo "[5/6] Building Python virtual environment and dependencies..."
python3 -m venv /root/venv
/root/venv/bin/pip install --upgrade pip setuptools wheel
if [ -f "$SCRIPT_DIR/src/requirements.txt" ]; then
    /root/venv/bin/pip install -r "$SCRIPT_DIR/src/requirements.txt" || true
fi
/root/venv/bin/pip install gunicorn

# Generate SSL Certificates for Panel Port
if [ ! -f "$ETC_DIR/ssl/cert.pem" ]; then
    openssl req -x509 -nodes -days 3650 -newkey rsa:2048 \
        -keyout "$ETC_DIR/ssl/privkey.pem" \
        -out "$ETC_DIR/ssl/cert.pem" \
        -subj "/C=US/ST=Cloud/L=Server/O=NextPanel/CN=localhost"
    chmod 600 "$ETC_DIR/ssl/privkey.pem"
    chmod 644 "$ETC_DIR/ssl/cert.pem"
fi

echo "[6/6] Configuring System Services, Nginx Proxy & CLI..."
cp "$SCRIPT_DIR/templates_config/nextpanel.service" /etc/systemd/system/nextpanel.service
cp "$SCRIPT_DIR/templates_config/nextpanel_nginx.conf" /etc/nginx/conf.d/nextpanel.conf 2>/dev/null || \
cp "$SCRIPT_DIR/templates_config/nextpanel_nginx.conf" /etc/nginx/sites-enabled/nextpanel 2>/dev/null || true

cp "$SCRIPT_DIR/templates_config/nextpanel_cli.sh" /usr/local/bin/nextpanel
chmod +x /usr/local/bin/nextpanel

systemctl daemon-reload
systemctl enable nextpanel
systemctl restart nextpanel
systemctl enable nginx
systemctl restart nginx

PUBLIC_IP=$(curl -m 5 -s ifconfig.me || hostname -I | awk '{print $1}')

echo ""
echo -e "\033[1;32m=================================================================\033[0m"
echo -e "\033[1;32m  NextPanel Installation Completed Successfully!                \033[0m"
echo -e "\033[1;32m=================================================================\033[0m"
echo -e "Web Panel Address : \033[1;34mhttps://${PUBLIC_IP}:${PORT}\033[0m"
echo -e "Management CLI    : \033[1;33mnextpanel info | start | stop | restart\033[0m"
echo -e "Database Password : \033[1;33m${DB_PASSWORD}\033[0m (saved at $DB_PASS_FILE)"
echo -e "License Mode      : \033[1;32mLifetime Community/Enterprise (Unlocked)\033[0m"
echo ""
