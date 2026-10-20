#!/bin/bash
# NextPanel Command Line Utility

IP=$(ip=$(hostname -I | awk '{print $1}'); if [[ $ip == 10.* || $ip == 172.* || $ip == 192.168.* ]]; then ip=$(curl -m 5 -s ifconfig.me); [[ -z $ip ]] && ip=$(hostname -I | awk '{print $1}'); fi; echo $ip)
PORT=8443
if [ -f /etc/nextpanel/port ]; then
    PORT=$(cat /etc/nextpanel/port)
fi

TIME1=$(date -I)
TIME2=$(date +%H:%M:%S)
RAM=$(free -m 2>/dev/null | awk 'NR==2{printf "%s/%sMB (%.2f%%)\n", $3,$2,$3*100/$2 }')
LOAD=$(uptime 2>/dev/null | awk -F'[a-z]:' '{ print $2}' | xargs)
DISK=$(df -h / 2>/dev/null | awk 'NR==2{printf "%d/%dGB (%s)\n", $3,$2,$5}')
UPTIME=$(uptime -p 2>/dev/null || uptime)

show_banner() {
echo -e "\033[1;34m"
cat << "EOF"
  _   _           _   _____                  _ 
 | \ | |         | | |  __ \                | |
 |  \| | _____  _| |_| |__) |_ _ _ __   ___| |
 | . ` |/ _ \ \/ / __|  ___/ _` | '_ \ / _ \ |
 | |\  |  __/>  <| |_| |  | (_| | | | |  __/ |
 |_| \_|\___/_/\_\\__|_|   \__,_|_| |_|\___|_|
                                               
           Free & Open Cloud Hosting Control Panel
EOF
echo -e "\033[0m"
echo -e "Web Panel URL      : \033[1;32mhttps://${IP}:${PORT}\033[0m"
echo -e "Server Time        : ${TIME1} ${TIME2}"
echo -e "Load Average       : ${LOAD}"
echo -e "RAM Usage          : ${RAM}"
echo -e "Disk Usage         : ${DISK}"
echo -e "Uptime             : ${UPTIME}"
echo ""
}

case "$1" in
    start)
        systemctl start nextpanel
        systemctl restart nginx 2>/dev/null || systemctl restart lsws 2>/dev/null
        echo "NextPanel services started."
        ;;
    stop)
        systemctl stop nextpanel
        echo "NextPanel services stopped."
        ;;
    restart)
        systemctl restart nextpanel
        systemctl restart nginx 2>/dev/null || systemctl restart lsws 2>/dev/null
        echo "NextPanel services restarted."
        ;;
    status)
        systemctl status nextpanel
        ;;
    port)
        if [ -n "$2" ]; then
            echo "$2" > /etc/nextpanel/port
            sed -i "s/listen [0-9]\+ ssl/listen $2 ssl/g" /etc/nginx/sites-available/nextpanel 2>/dev/null
            systemctl restart nginx 2>/dev/null || systemctl restart nextpanel
            echo "Port changed to $2"
        else
            echo "Current port: $PORT"
        fi
        ;;
    password)
        if [ -n "$2" ]; then
            /root/venv/bin/python /usr/local/nextpanel/manage.py shell -c "from django.contrib.auth.models import User; u = User.objects.get(username='admin'); u.set_password('$2'); u.save(); print('Password updated successfully!')"
        else
            echo "Usage: nextpanel password <new-password>"
        fi
        ;;
    info|*)
        show_banner
        ;;
esac
