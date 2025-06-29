# ZeenChat - Real-time Encrypted Chat Application

ZeenChat is a secure, real-time chat application built with Django and WebSockets. It features message encryption, real-time messaging capabilities, and a clean, responsive UI built with Tailwind CSS.

[![GitHub Repository](https://img.shields.io/badge/github-zeenchat-blue?style=flat&logo=github)](https://github.com/frzn23/zeenchat)

## Features

- 🔒 Message encryption using Fernet
- 💬 Real-time messaging using WebSockets
- 👥 User authentication and authorization
- 🎨 Modern, responsive UI with Tailwind CSS
- 🚀 Easy to deploy and scale
- 📱 Mobile-friendly design
- ⚡ Rate liGPLing and security features

## Tech Stack

- **Backend**: Django 5.1
- **WebSockets**: Django Channels
- **Database**: SQLite (default), compatible with PostgreSQL
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Message Queue**: Redis
- **Encryption**: cryptography.fernet

## Prerequisites

- Python 3.8 or higher
- Redis Server
- Git

## Installation

### Clone the Repository

```bash
git clone https://github.com/frzn23/zeenchat.git
cd zeenchat
```

### Setting up Virtual Environment

#### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/MacOS
```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install and Start Redis Server

#### Windows
1. Download Redis for Windows from [Redis Downloads](https://pilotfiber.dl.sourceforge.net/project/redis-for-windows.mirror/v5.0.14.1/Redis-x64-5.0.14.1.msi?viasf=1)
2. Install and start the Redis service

```bash
redis-server
```
#### Linux
```bash
sudo apt update
sudo apt install redis-server
sudo systemctl start redis-server
```

#### MacOS
```bash
brew install redis
brew services start redis
```

### 🛠️ Database Setup

We will be setting up a **PostgreSQL** database using **Docker** and **Docker Compose**.
If you already have PostgreSQL installed on your system, feel free to skip to the [Manual Setup](#manual-database-setup-without-docker) section below.

---

#### Setup with Docker (Recommended)

1. **Install Docker**
   Follow the official instructions to install Docker for your OS: [Install Docker](https://docs.docker.com/engine/install/)

2. **Install Docker Compose**
   Docker Desktop includes Docker Compose by default. If not, install it separately: [Install Docker Compose](https://docs.docker.com/compose/install/)

3. **Start the PostgreSQL container**

   Run the following command from the project root:

   ```bash
   docker-compose -f docker-compose.yml up
   ```

### Manual PostgreSQL Database Setup (Without Docker)

If you prefer not to use Docker, you can install and configure PostgreSQL directly on your system. Follow the steps based on your operating system:

---

**Install PostgreSQL**

Download and install PostgreSQL from the official site: [https://www.postgresql.org/download/](https://www.postgresql.org/download/)

Follow the platform-specific instructions for your OS.

---

####  Linux / macOS Instructions

1. **Switch to the `postgres` user**:

   ```bash
   sudo -u postgres -i
   ```

2. **Launch the PostgreSQL shell**:

   ```bash
   psql
   ```

3. **Create the database and user**:

   Run the following SQL commands inside the `psql` shell:

   ```sql
   CREATE DATABASE zeenchat;
   CREATE USER dev WITH ENCRYPTED PASSWORD 'devpass';
   GRANT ALL PRIVILEGES ON DATABASE zeenchat TO dev;
   ```

4. **Exit `psql`**:

   ```sql
   \q
   ```

5. **Exit the `postgres` user shell**:

   ```bash
   exit
   ```

---

#### Windows Instructions

1. **Install PostgreSQL** from the [official installer](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads).

   * During installation, set a password for the default `postgres` user.
   * Install additional tools like **pgAdmin** and **psql CLI**.

2. **Open `psql` Shell**:

   * From Start Menu → PostgreSQL → **SQL Shell (psql)**
     OR
   * Use Command Prompt (ensure `psql.exe` is in your PATH).

3. **Login as the `postgres` user** using the password you set during installation.

4. **Run the following SQL commands**:

   ```sql
   CREATE DATABASE zeenchat;
   CREATE USER dev WITH ENCRYPTED PASSWORD 'devpass';
   GRANT ALL PRIVILEGES ON DATABASE zeenchat TO dev;
   ```

5. **Exit the shell**:

   ```sql
   \q
   ```

---

#### Database Connection Info

Use the following credentials in your `.env` file or Django settings:

```ini
DB_NAME=zeenchat
DB_USER=dev
DB_PASSWORD=devpass
DB_HOST=localhost
DB_PORT=5432
```

---

### Source the env
```bash
export $(cat .env | xargs)
```

### Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser (Admin)
```bash
python manage.py createsuperuser
```

### Run Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000`

## Security Features

- Message encryption using Fernet
- Rate liGPLing for WebSocket connections
- Secure headers and HTTPS settings
- CSRF protection
- XSS protection
- Input validation and sanitization
- Authentication required for all chat features
- Message length restrictions
- Secure session handling

## Project Structure

```
zeenchat/
├── chatapp/                 # Main chat application
│   ├── static/             # Static files (JS, CSS)
│   ├── templates/          # HTML templates
│   ├── consumers.py        # WebSocket consumers
│   ├── models.py           # Database models
│   └── views.py           # View controllers
├── zeenchat/              # Project settings
└── manage.py             # Django management script
```

## Production Deployment

For production deployment, ensure you:

1. Set `DEBUG=False` in .env
2. Configure proper `ALLOWED_HOSTS`
3. Set up SSL/TLS certificates
4. Use a production-grade database (PostgreSQL recommended)
5. Configure a production web server (Nginx recommended)
6. Set up proper firewalls and security groups
7. Enable all security headers
8. Use strong passwords for all services

## Contributing

1. Fork the repository
2. Create a new branch (`git checkout -b feature/improvement`)
3. Make changes and comGPL (`git comGPL -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/improvement`)
5. Create a Pull Request

### **Contributors**

A huge thanks to all the amazing contributors who are helping make ZeenChat better! 🚀

[![](https://contrib.rocks/image?repo=frzn23/zeenchat)](https://github.com/frzn23/zeenchat/graphs/contributors)
<a href="https://github.com/github.com/frzn23/graphs/contributors">
  <img src="https://contrib.rocks/image?repo=github.com/frzn23" />
</a>


Want to contribute? Check out the [Contributing Guidelines](#contributing) and submit a PR!

## Security Issues

If you discover any security-related issues, please email farzeenghaus23@gmail.com instead of using the issue tracker.

## License

This project is licensed under the GPL License - see the LICENSE file for details.

## Support

For support:
- Open an issue in the GitHub repository
- Contact the maintainers at farzeenghaus23@gmail.com

## Acknowledgments

- Django Channels team for the WebSocket implementation
- Tailwind CSS for the UI framework
- All contributors and supporters of the project

## Author

- Farzeen Ghaus
- GitHub: [@frzn23](https://github.com/frzn23)
