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

On a clean server, run:

```bash
git clone <your-repo-url> nextpanel
cd nextpanel
sudo bash install.sh
```

Once installation finishes, your panel will be live at:
```
https://<YOUR_SERVER_IP>:8443
```

---

## 🛠️ CLI Commands

```bash
nextpanel info      # View server status and login details
nextpanel start     # Start NextPanel services
nextpanel stop      # Stop NextPanel services
nextpanel restart   # Restart NextPanel services
nextpanel port 9090 # Change panel access port
```
