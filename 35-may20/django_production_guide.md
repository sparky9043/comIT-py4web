# 🚀 Django in Production — A Beginner's Guide

> This guide walks you through the most common ways to deploy a Django application to production. No prior deployment experience needed.

---

## Table of Contents

1. [Before You Deploy — Checklist](#1-before-you-deploy--checklist)
2. [Option A — VPS (Virtual Private Server)](#2-option-a--vps-virtual-private-server)
3. [Option B — PaaS (Platform as a Service)](#3-option-b--paas-platform-as-a-service)
4. [Option C — Docker](#4-option-c--docker)
5. [Option D — Serverless](#5-option-d--serverless)
6. [Option E — Shared Hosting (cPanel)](#6-option-e--shared-hosting-cpanel)
7. [Option F — Managed Kubernetes](#7-option-f--managed-kubernetes)
8. [Choosing the Right Option](#8-choosing-the-right-option)
9. [Common Production Settings](#9-common-production-settings)
10. [Environment Variables & Secrets](#10-environment-variables--secrets)

---

## 1. Before You Deploy — Checklist

Before going live, make sure your project is production-ready.

### ✅ Django Settings

Open your `settings.py` and verify these:

```python
# NEVER leave this True in production
DEBUG = False

# List every domain/IP your app will be served from
ALLOWED_HOSTS = ["yourdomain.com", "www.yourdomain.com"]

# Use a strong, unique secret key — never commit it to Git
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY")
```

### ✅ Static & Media Files

Django's built-in dev server does **not** serve static files in production.

```bash
# Collect all static files into one folder
python manage.py collectstatic
```

Set `STATIC_ROOT` in settings:

```python
STATIC_ROOT = BASE_DIR / "staticfiles"
STATIC_URL = "/static/"
```

### ✅ Database

Switch away from SQLite for anything beyond a hobby project:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME"),
        "USER": os.environ.get("DB_USER"),
        "PASSWORD": os.environ.get("DB_PASSWORD"),
        "HOST": os.environ.get("DB_HOST", "localhost"),
        "PORT": "5432",
    }
}
```

Install the PostgreSQL adapter:

```bash
pip install "psycopg[binary]"
```

### ✅ requirements.txt

Make sure it is up to date:

```bash
pip freeze > requirements.txt
```

### ✅ Security Settings (add to settings.py)

```python
# Tells Django it's secure if the proxy sets this header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
```

---

## 2. Option A — VPS (Virtual Private Server)

**Best for:** Full control, custom setups, learning how servers work.
**Examples:** DigitalOcean Droplet, Linode/Akamai, Hetzner, AWS EC2, Vultr.
**Cost:** ~$4–$20/month depending on provider and plan.

A VPS gives you a raw Linux server. You install and configure everything yourself.

### Step 1 — Provision a Server

Sign up with a provider (DigitalOcean is beginner-friendly) and create an Ubuntu 22.04 server. You'll get an IP address and root access via SSH.

```bash
ssh root@YOUR_SERVER_IP
```

### Step 2 — Create a Non-Root User

Running as root is a security risk. Create a regular user:

```bash
adduser deploy
usermod -aG sudo deploy
su - deploy
```

### Step 3 — Install Dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3-pip python3-venv python3-dev \
    postgresql postgresql-contrib nginx git -y
```

### Step 4 — Set Up PostgreSQL

```bash
sudo -u postgres psql

-- Inside the psql shell:
CREATE DATABASE mydb;
CREATE USER myuser WITH PASSWORD 'mypassword';
ALTER ROLE myuser SET client_encoding TO 'utf8';
ALTER ROLE myuser SET default_transaction_isolation TO 'read committed';
ALTER ROLE myuser SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE mydb TO myuser;
\q
```

### Step 5 — Clone Your Project

```bash
cd /home/deploy
git clone https://github.com/yourname/yourproject.git
cd yourproject
```

### Step 6 — Set Up a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install gunicorn
```

### Step 7 — Run Migrations & Collect Static Files

```bash
python manage.py migrate
python manage.py collectstatic --noinput
python manage.py createsuperuser
```

### Step 8 — Configure Gunicorn

Gunicorn is a production-grade WSGI server. Test it first:

```bash
gunicorn --bind 0.0.0.0:8000 yourproject.wsgi
```

Create a systemd service so it starts automatically:

```bash
sudo nano /etc/systemd/system/gunicorn.service
```

```ini
[Unit]
Description=Gunicorn daemon for Django
After=network.target

[Service]
User=deploy
Group=www-data
WorkingDirectory=/home/deploy/yourproject
EnvironmentFile=/home/deploy/yourproject/.env
ExecStart=/home/deploy/yourproject/venv/bin/gunicorn \
    --access-logfile - \
    --workers 3 \
    --bind unix:/run/gunicorn.sock \
    yourproject.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### Step 9 — Configure Nginx

Nginx acts as a reverse proxy, forwarding traffic to Gunicorn and serving static files directly.

```bash
sudo nano /etc/nginx/sites-available/yourproject
```

```nginx
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location /static/ {
        root /home/deploy/yourproject;
    }

    location /media/ {
        root /home/deploy/yourproject;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/yourproject /etc/nginx/sites-enabled/
sudo nginx -t        # test config
sudo systemctl restart nginx
```

### Step 10 — Enable HTTPS with Let's Encrypt (Free SSL)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

Certbot will automatically update your Nginx config and set up auto-renewal.

---

## 3. Option B — PaaS (Platform as a Service)

**Best for:** Beginners who want to focus on code, not servers.
**Examples:** Railway, Render, Heroku, Fly.io.
**Cost:** Free tiers available; paid plans from ~$5/month.

PaaS platforms handle the server, OS, and much of the configuration for you. You just push your code and they take care of the rest.

### Railway (Recommended for Beginners)

1. Sign up at [railway.app](https://railway.app)
2. Click **New Project → Deploy from GitHub Repo**
3. Select your repository
4. Add a PostgreSQL service to your project
5. Set your environment variables in the Railway dashboard
6. Railway auto-detects Django and builds it

Add a `Procfile` in your project root:

```
web: gunicorn yourproject.wsgi --log-file -
```

Add a `runtime.txt` to pin your Python version:

```
python-3.12.0
```

### Render

1. Sign up at [render.com](https://render.com)
2. Create a **New Web Service** and connect your GitHub repo
3. Set **Build Command:**
   ```bash
   pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
   ```
4. Set **Start Command:**
   ```bash
   gunicorn yourproject.wsgi:application
   ```
5. Add a PostgreSQL database from the Render dashboard
6. Set your environment variables

### Heroku

```bash
# Install the Heroku CLI, then:
heroku login
heroku create my-django-app
heroku addons:create heroku-postgresql:essential-0

# Set environment variables
heroku config:set DJANGO_SECRET_KEY="your-secret-key"
heroku config:set DEBUG=False
heroku config:set ALLOWED_HOSTS=".herokuapp.com"

git push heroku main
heroku run python manage.py migrate
```

### Fly.io

```bash
# Install flyctl, then:
fly launch      # auto-detects Django
fly postgres create
fly postgres attach
fly deploy
```

---

## 4. Option C — Docker

**Best for:** Reproducible environments, team projects, scaling.
**Runs on:** Any server, VPS, cloud, or your own machine.
**Cost:** Depends on where you host the containers.

Docker packages your app and all its dependencies into a container. It runs the same everywhere.

### Step 1 — Dockerfile

Create a `Dockerfile` in your project root:

```dockerfile
# Use an official Python base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project source
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Run Gunicorn
CMD ["gunicorn", "yourproject.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Step 2 — docker-compose.yml

`docker-compose` lets you run Django + PostgreSQL + Nginx together:

```yaml
services:
  db:
    image: postgres:15
    volumes:
      - postgres_data:/var/lib/postgresql/data/
    env_file:
      - .env

  web:
    build: .
    command: gunicorn yourproject.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    expose:
      - 8000
    env_file:
      - .env
    depends_on:
      - db

  nginx:
    image: nginx:stable-alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/conf.d/default.conf
      - static_volume:/app/staticfiles
      - media_volume:/app/media
    depends_on:
      - web

volumes:
  postgres_data:
  static_volume:
  media_volume:
```

### Step 3 — Nginx config for Docker

Create `nginx/nginx.conf`:

```nginx
upstream django {
    server web:8000;
}

server {
    listen 80;
    server_name yourdomain.com;

    location /static/ {
        alias /app/staticfiles/;
    }

    location /media/ {
        alias /app/media/;
    }

    location / {
        proxy_pass http://django;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Host $host;
        proxy_redirect off;
    }
}
```

### Step 4 — .env file

```ini
POSTGRES_DB=mydb
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mypassword
DB_HOST=db
DJANGO_SECRET_KEY=your-very-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com
```

### Step 5 — Deploy

```bash
# On your server (VPS, EC2, etc.)
docker compose up -d --build
docker compose exec web python manage.py migrate
docker compose exec web python manage.py createsuperuser
```

---

## 5. Option D — Serverless

**Best for:** Apps with variable traffic, minimal maintenance.
**Examples:** AWS Lambda + Zappa, Google Cloud Run, Azure Functions.
**Cost:** Pay per request — can be very cheap or even free at low scale.

Serverless means you don't manage a server at all. Your code runs on-demand.

### AWS Lambda with Zappa

Zappa packages your Django app and deploys it to AWS Lambda + API Gateway.

```bash
pip install zappa

# Initialize
zappa init
```

This creates a `zappa_settings.json`:

```json
{
    "production": {
        "django_settings": "yourproject.settings",
        "project_name": "yourproject",
        "runtime": "python3.12",
        "s3_bucket": "your-unique-s3-bucket-name",
        "aws_region": "us-east-1"
    }
}
```

```bash
zappa deploy production
zappa manage production migrate
```

> ⚠️ Django's ORM is not ideal for serverless — use a managed database like AWS RDS or PlanetScale.

### Google Cloud Run

Cloud Run runs Docker containers on demand, scaling to zero when idle.

```bash
# Build and push your Docker image to Google Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/django-app

# Deploy
gcloud run deploy django-app \
    --image gcr.io/YOUR_PROJECT_ID/django-app \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

---

## 6. Option E — Shared Hosting (cPanel)

**Best for:** Very small/static sites, extremely budget-conscious.
**Examples:** Namecheap, Bluehost, A2 Hosting.
**Cost:** $2–$10/month, often bundled with a domain.
**Limitations:** Limited control, no root access, often restricted Python versions.

> ⚠️ Shared hosting is **not recommended** for Django in general. Most providers have limited support and you may run into significant restrictions. Consider PaaS instead if cost is a concern.

If you must use it:

1. Your host must support **Passenger** or **WSGI**
2. Check that your provider supports the required Python version
3. Many cPanel hosts have a **Setup Python App** tool in the dashboard
4. Use that tool to point to your Django project and `wsgi.py`

---

## 7. Option F — Managed Kubernetes

**Best for:** Large-scale apps, teams, complex microservices.
**Examples:** AWS EKS, Google GKE, DigitalOcean Kubernetes.
**Cost:** $70+/month. Not for small projects.

Kubernetes (k8s) orchestrates many containers across many servers. It is powerful but complex.

A minimal Django deployment on Kubernetes involves:

- A `Deployment` (runs your Django containers)
- A `Service` (exposes your app internally)
- An `Ingress` (routes external traffic)
- A `ConfigMap` + `Secret` (for environment variables)

```yaml
# Example: deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: django-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: django
  template:
    metadata:
      labels:
        app: django
    spec:
      containers:
        - name: django
          image: yourrepo/yourimage:latest
          ports:
            - containerPort: 8000
          envFrom:
            - secretRef:
                name: django-secrets
```

> 💡 Unless you have a very specific need, skip Kubernetes until your app has outgrown simpler options.

---

## 8. Choosing the Right Option

| Option | Control | Difficulty | Cost | Best For |
|---|---|---|---|---|
| **VPS** | Full | Medium | $4–$20/mo | Learning, custom setups |
| **PaaS (Railway/Render)** | Low | Easy | Free–$20/mo | Beginners, fast deploys |
| **Docker** | Full | Medium | Depends on host | Teams, reproducibility |
| **Serverless** | Low | Medium | Pay per use | Variable traffic |
| **Shared Hosting** | Very Low | Easy | $2–$10/mo | Not recommended |
| **Kubernetes** | Full | Hard | $70+/mo | Large-scale apps |

### 👶 If you're a beginner → Start with Railway or Render
### 🛠️ If you want to learn DevOps → Use a VPS (DigitalOcean + Nginx + Gunicorn)
### 🐳 If you want portability → Use Docker on a VPS
### 💸 If cost is zero → Railway or Render free tiers

---

## 9. Common Production Settings

Here is a clean `settings.py` pattern for production:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ["DJANGO_SECRET_KEY"]
DEBUG = os.environ.get("DEBUG", "False") == "True"
# ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")
ALLOWED_HOSTS = [host.strip() for host in os.environ.get("ALLOWED_HOSTS", "").split(",") if host.strip()]

INSTALLED_APPS = [
    # ... your apps
    "whitenoise.runserver_nostatic",  # add this for static files
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # right after security middleware
    # ... rest of your middleware
]

# Static files — WhiteNoise serves them without Nginx
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Old versions
#STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {"class": "logging.StreamHandler"},
    },
    "root": {
        "handlers": ["console"],
        "level": "WARNING",
    },
}
```

Install WhiteNoise to serve static files without needing Nginx:

```bash
pip install whitenoise
```

---

## 10. Environment Variables & Secrets

**Never hardcode secrets in your code or commit them to Git.**

### Using python-decouple

```bash
pip install python-decouple
```

Create a `.env` file (add this to `.gitignore`!):

```ini
DJANGO_SECRET_KEY=your-super-secret-key-here
DEBUG=False
DATABASE_URL=postgres://user:password@localhost/dbname
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

In `settings.py`:

```python
from decouple import config

SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
#ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="").split(",")
ALLOWED_HOSTS = [host.strip() for host in config("ALLOWED_HOSTS", default="").split(",") if host.strip()]
```

### Using dj-database-url (for DATABASE_URL)

```bash
pip install dj-database-url
```

```python
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=os.environ.get("DATABASE_URL"),
        conn_max_age=600,
    )
}
```

### .gitignore — Always Include

```gitignore
.env
*.pyc
__pycache__/
staticfiles/
media/
db.sqlite3
```

---

## Quick Reference — Useful Commands

```bash
# Run database migrations
python manage.py migrate

# Create an admin user
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Check for deployment issues
python manage.py check --deploy

# Start Gunicorn manually (test)
gunicorn yourproject.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## Further Reading

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Gunicorn Configuration](https://docs.gunicorn.org/en/stable/configure.html)
- [WhiteNoise Documentation](https://whitenoise.readthedocs.io/)
- [Railway Django Guide](https://docs.railway.app/guides/django)
- [Render Django Guide](https://render.com/docs/deploy-django)

---

*Happy deploying! 🎉 Start simple, and scale when you need to.*
