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
- **Database**: Postgres (default), can be configured to use SQLite
- **Frontend**: HTML, JavaScript, Tailwind CSS
- **Message Queue**: Redis
- **Encryption**: cryptography.fernet

## Prerequisites

- Python 3.8 or higher
- Redis Server *(included in Docker stack; must be installed separately for traditional installation)*
- Docker Compose *(Docker installation only)*
- Git


# Installation
___

### Choose an installation method:

1. [Docker Compose (for development only)](#install-via-docker-compose-for-development)
2. Docker Compose (for production) *(coming soon!)*
3. [Traditional Venv](#install-via-traditional-virtual-environment)

### Install via Docker Compose (for development)

*See the [official Docker documentation](https://docs.docker.com/compose/install/) for more information on Compose, including installation.*

#### 1. Clone the Repository
```bash
$ git clone https://github.com/frzn23/zeenchat.git
$ cd zeenchat
```

#### 3. Update .env file

```bash
$ cp docker/env.example .env
$ nano docker/.env
```

Update applicable ENV file entries. 
- At a minimum, update the REDIS_PASSWORD and DB_PASSWORD entries. 
- For production deployment, additional entries must be updated. See [Environment Variables](#docker-environment-variables) for more information.

#### 4. Create and Start Containers
```bash
$ docker compose -f docker/compose.dev.yaml up --build -d
```

The application will be available at http://localhost:8000.

#### 5. Create Superuser

```bash
# First, get the container ID for the server
$ docker ps

# Then, exec in to create Superuser
$ docker exec -it <container_id> python manage.py createsupuser
```

## Install via Traditional Virtual Environment

#### 1. Clone the Repository
```bash
$ git clone https://github.com/frzn23/zeenchat.git
$ cd zeenchat
```

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

### 3. Install Dependencies
```bash
$ pip install -r requirements.txt
```

### 4. Install and Start Redis Server

#### Windows
1. Download Redis for Windows from [Redis Downloads](https://pilotfiber.dl.sourceforge.net/project/redis-for-windows.mirror/v5.0.14.1/Redis-x64-5.0.14.1.msi?viasf=1)
2. Install and start the Redis service

#### Linux
```bash
$ sudo apt update
$ sudo apt install redis-server
$ sudo systemctl start redis-server
```

#### MacOS
```bash
% brew install redis
% brew services start redis
```

### 5. Database Setup
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

### 6. Create Superuser (Admin)
```bash
$ python manage.py createsuperuser
```

### 7. Run Development Server
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
│   ├── static/              # Static files (JS, CSS)
│   ├── templates/           # HTML templates
│   ├── consumers.py         # WebSocket consumers
│   ├── middleware.py        # App Middleware
│   ├── models.py            # Database models
│   └── views.py             # View controllers
├── zeenchat/                # Project settings
├── manage.py                # Django management script
├── docker/                  # Docker configuration file(s)
└── redis/
    └── conf/                # Redis configuration file(s)
```

## Docker Environment Variables

### `DJANGO_SECRET_KEY`

**Default:** ' ' (Empty string) *(**REQUIRED** for production deployment)*

A secret key for a particular Django installation. This is used to provide cryptographic signing, and should be set to a unique, unpredictable value. See [Django documentation](https://docs.djangoproject.com/en/5.1/ref/settings/#secret-key) for more information.

### `DJANGO_DEBUG`

**Default:** *False* *(optional)*

A boolean that turns on/off debug mode. See [Django documentation](https://docs.djangoproject.com/en/5.1/ref/settings/#debug) for more information.

**SECURITY NOTE**: Never deploy a site into production with DEBUG turned on.

### `DJANGO_ALLOWED_HOSTS`

**Default:** *[]* *(Empty list) (**REQUIRED** for production deployment)*

A comma-seperated list of strings representing the host/domain names that this Django site can serve. This is a security measure to prevent HTTP Host header attacks, which are possible even under many seemingly-safe web server configurations. See [Django documentation](https://docs.djangoproject.com/en/5.1/ref/settings/#allowed-hosts) for more information.

Example  ENV file entry: `DJANGO_ALLOWED_HOSTS=localhost, 127.0.0.1, yourdomain.com`

### `CSRF_TRUSTED_ORIGINS`

**Default:** *[]* *(Empty list) (**REQUIRED** for production deployment)*

A comma-seperated list of trusted origins for unsafe requests (e.g. POST). See [Django documentation](https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-trusted-origins) for more information.

Example  ENV file entry: `CSRF_TRUSTED_ORIGINS=http://localhost, http://127.0.0.1, http://yourdomain.com, https://yourdomain.com`

### `CSRF_COOKIE_SECURE`

**Default:** *False* (**REQUIRED** for production deployment)*

Whether to use a secure cookie for the CSRF cookie. See [Django documentation](https://docs.djangoproject.com/en/5.1/ref/settings/#csrf-cookie-secure) for more information.

**SECURITY NOTE**: Warning:  Must be True for production deployment.

### `DATABASE` 

**Default:** *Postgres* *(optional)*

Specify database engine to use. Use mapping below:
- 'sqlite3': SQLite3
- 'pg': Postgres
- ' ' *(null entry)*: Postgres

Example ENV file entry: `DATABASE=sqlite3`

### `DB_NAME`

**Default:** *AppDatabase* *(optional)*

To set custom database name (ignored when using SQLite3).

### `DB_USER`

**Default:** *appuser* *(optional)*

To set custom database user (ignored when using SQLite3).

### `DB_PASSWORD`

**Default:** *appuser* *(**REQUIRED**) unless using SQLite3)*

To set custom database password (ignored when using SQLite3).

### `DB_HOST`

**Default:** *db* *(optional)*

To set custom database hostname (ignored when using SQLite3).

### `DB_PORT`

**Default:** *5432* *(optional)*

To set custom database port number (ignored when using SQLite3).

### `REDIS_PASSWORD`

**Default:** *none* ***(REQUIRED)***

To set password for Redis. See [Redis documentation]() for more information.

**SECURITY NOTE**: Warning: since Redis is pretty fast, an outside user can try up to 1 million passwords per second against a modern box. This means that you should use very strong passwords, otherwise they will be very easy to break.

### `REDIS_HOST`

**Default:** *redis* *(optional)*

To set custom Redis hostname.

### `REDIS_PORT`

**Default:** *6379* *(optional)*

To set custom Redis port number.

## Production Deployment
___
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
