# 🏠 Household Expense Tracker

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Django](https://img.shields.io/badge/Django-6.1-green?logo=django)
![Gunicorn](https://img.shields.io/badge/Gunicorn-WSGI-darkgreen?logo=gunicorn)
![Nginx](https://img.shields.io/badge/Nginx-Reverse%20Proxy-009639?logo=nginx)
![Debian](https://img.shields.io/badge/OS-Debian%2012-red?logo=debian)
![Cloudflare](https://img.shields.io/badge/Cloudflare-Tunnel-orange?logo=cloudflare)

A full-featured web application built with **Django** for tracking, managing, and analyzing household budgets and personal expenses in real time. Designed for easy local network deployment and remote access via secure tunnels.

---

## ✨ Features

- 👤 **User Authentication & Isolation:** Secure signup and login system ensuring complete data privacy per user.
- 💸 **Expense Management (CRUD):** Add, view, edit, and delete daily expenses with categorization and custom dates.
- 📊 **Dynamic Budget Tracking:** Set monthly budget limits with automatic calculations of remaining funds and interactive visual progress bars.
- 🖥️ **Self-Hosted Deployment:** Fully configured on a local **Debian 12** server using **Gunicorn** and **Nginx** reverse proxy.
- 🌐 **Global Access:** Integrated with **Cloudflare Tunnel (`cloudflared`)** for secure HTTPS external access without port forwarding.

---

## 🛠️ Tech Stack & Architecture

- **Backend:** Python 3.12, Django 6.1
- **Database:** SQLite (Development & Local Hosting)
- **WSGI Server:** Gunicorn
- **Web Server / Reverse Proxy:** Nginx
- **OS / Environment:** Debian 12 (Linux), Systemd Service Management
- **Networking & Tunnels:** Cloudflare Tunnel (`cloudflared`)

---

## 🚀 Quick Start (Local Development)

### Prerequisites
- Python 3.12+
- Git

### Installation Steps

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/OmarShaabanDev/household-expense-tracker.git](https://github.com/OmarShaabanDev/household-expense-tracker.git)
   cd household-expense-tracker

2. **Set up a virtual environment:**
- For Linux/Mac:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   
- For Windows:
   ```bash
   python -m venv venv
   venv\Scripts\activate

3. **Install dependencies:**
    ```bash
    pip install -r requirements.txt

4. **Run migrations:**
   ```bash
   python manage.py migrate

5. **Start the local server:**
   ```bash
   python manage.py runserver

Access the app at http://127.0.0.1:8000/expenses/
   

## 👨‍💻 Author

**Omar Shaaban**
- **GitHub:** [@omarshaabandev-hub](https://github.com/omarshaabandev-hub)
- **LinkedIn:** [Omar Shaaban](https://www.linkedin.com/in/omar-shaaban-887a01323)
- **Email:** omarshaaban.dev@gmail.com
