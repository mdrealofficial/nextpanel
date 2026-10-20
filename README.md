# 🚀 NextPanel — Free & Open-Source Cloud Hosting Control Panel

**NextPanel** is a lightweight, modern, and open-source web hosting control panel designed for managing **OpenLiteSpeed**, **Apache**, and **Nginx** web servers, MariaDB, PowerDNS, Postfix/Dovecot email stacks, and automated SSL.

---

## 📌 Features

- ✅ **No Closed Binaries**: 100% open-source Python (Django) & standard system services.
- ✅ **Completely Unlocked**: All premium features (terminal, multi-user quotas, brand customizer, API modules) are permanently enabled with lifetime status.
- ✅ **OpenLiteSpeed & Multi-Server Switching**: Seamlessly switch between OpenLiteSpeed, Apache, and Nginx.
- ✅ **Standard Production Stack**: Powered by **Gunicorn** & **Nginx** reverse proxy with SSL termination and WebSocket streaming.
- ✅ **Web Terminal & CLI**: Interactive web terminal and custom `/usr/local/bin/nextpanel` CLI tool.
- ✅ **Self-Contained**: No external phoning home to remote license servers.

---

## 🖥️ System Requirements

- **Ubuntu** 20.04 / 22.04 / 24.04 LTS
- **Debian** 11 / 12
- **AlmaLinux** 8 / 9, **Rocky Linux** 8 / 9, **CentOS Stream** 8 / 9

---

## 📥 Installation

Run the following command as `root` on your clean Linux server:

### Option 1: Quick Install via Git

```bash
git clone https://github.com/mdrealofficial/nextpanel.git /usr/local/nextpanel-setup
cd /usr/local/nextpanel-setup
bash install.sh
```

*(If prompted for credentials because the repo is currently private, enter your GitHub username and Personal Access Token, or make the repository public in GitHub Settings).*

### Option 2: One-Liner (Once Public / Download Token)

```bash
curl -fsSL https://raw.githubusercontent.com/mdrealofficial/nextpanel/main/install.sh | bash
```

Once installation finishes, your panel will be live at:
```
https://<YOUR_SERVER_IP>:8443
```
Login with the root database credentials displayed at the end of the installation.

---

## 🛠️ CLI Commands

```bash
nextpanel info      # View server status and login details
nextpanel start     # Start NextPanel services
nextpanel stop      # Stop NextPanel services
nextpanel restart   # Restart NextPanel services
nextpanel port 9090 # Change panel access port
```
