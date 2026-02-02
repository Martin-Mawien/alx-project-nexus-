# Deployment Guide

This guide covers deploying the Job Board Backend API to various platforms.

## 🎯 Prerequisites

Before deploying, ensure you have:

- A working Git repository with your code
- All tests passing locally
- Environment variables configured
- Database migrations tested
- Static files collected

---

## 🚀 Deployment Options

### Option 1: Render (Recommended)

Render provides an easy, free-tier deployment option with PostgreSQL database included.

#### Step 1: Prepare Your Repository

1. Ensure your repository is pushed to GitHub
2. Add a `render.yaml` file (optional but recommended):

```yaml
services:
  - type: web
    name: jobboard-api
    env: python
    region: oregon
    plan: free
    branch: main
    buildCommand: "pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate"
    startCommand: "gunicorn config.wsgi:application"
    envVars:
      - key: PYTHON_VERSION
        value: 3.10.0
      - key: DJANGO_SETTINGS_MODULE
        value: config.settings.production
      - key: SECRET_KEY
        generateValue: true
      - key: DEBUG
        value: False
      - key: DATABASE_URL
        fromDatabase:
          name: jobboard-db
          property: connectionString

databases:
  - name: jobboard-db
    plan: free
    databaseName: jobboard
    user: jobboard
```

#### Step 2: Create a Render Account

1. Go to [render.com](https://render.com)
2. Sign up with your GitHub account
3. Authorize Render to access your repositories

#### Step 3: Create a PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. Configure:
   - Name: `jobboard-db`
   - Database: `jobboard`
   - User: `jobboard`
   - Region: `Oregon (US West)`
   - Plan: `Free`
3. Click "Create Database"
4. Copy the "Internal Database URL" for later

#### Step 4: Create a Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - Name: `jobboard-api`
   - Region: `Oregon (US West)`
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: 
     ```bash
     pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
     ```
   - Start Command:
     ```bash
     gunicorn config.wsgi:application
     ```

#### Step 5: Configure Environment Variables

Add the following environment variables in Render dashboard:

```
SECRET_KEY=<generate-random-secret-key>
DEBUG=False
ALLOWED_HOSTS=<your-app-name>.onrender.com
DATABASE_URL=<paste-internal-database-url>
DJANGO_SETTINGS_MODULE=config.settings.production
```

#### Step 6: Deploy

1. Click "Create Web Service"
2. Render will automatically build and deploy
3. Wait for deployment to complete (5-10 minutes)
4. Your API will be available at: `https://<your-app-name>.onrender.com`

#### Step 7: Create Superuser

Use Render Shell to create an admin user:

1. Go to your web service dashboard
2. Click "Shell" tab
3. Run:
   ```bash
   python manage.py createsuperuser
   ```

---

### Option 2: Heroku

#### Step 1: Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Ubuntu
curl https://cli-assets.heroku.com/install.sh | sh

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli
```

#### Step 2: Login to Heroku

```bash
heroku login
```

#### Step 3: Create Heroku App

```bash
heroku create jobboard-api
```

#### Step 4: Add PostgreSQL

```bash
heroku addons:create heroku-postgresql:hobby-dev
```

#### Step 5: Configure Environment Variables

```bash
heroku config:set SECRET_KEY=<your-secret-key>
heroku config:set DEBUG=False
heroku config:set DJANGO_SETTINGS_MODULE=config.settings.production
heroku config:set ALLOWED_HOSTS=<your-app-name>.herokuapp.com
```

#### Step 6: Create Procfile

Create a `Procfile` in your project root:

```
web: gunicorn config.wsgi:application --log-file -
release: python manage.py migrate
```

#### Step 7: Deploy

```bash
git push heroku main
```

#### Step 8: Run Migrations and Create Superuser

```bash
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

#### Step 9: Scale Dynos

```bash
heroku ps:scale web=1
```

---

### Option 3: DigitalOcean App Platform

#### Step 1: Create DigitalOcean Account

1. Sign up at [digitalocean.com](https://www.digitalocean.com)
2. Add payment method

#### Step 2: Create Database

1. Go to Databases → Create Database Cluster
2. Choose PostgreSQL 14
3. Select a datacenter region
4. Choose $15/month plan (or higher)
5. Name: `jobboard-db`

#### Step 3: Create App

1. Go to Apps → Create App
2. Connect your GitHub repository
3. Configure:
   - Branch: `main`
   - Source Directory: `/`
   - Autodeploy: `Yes`

#### Step 4: Configure Build Settings

```yaml
name: jobboard-api
region: nyc
services:
  - name: web
    github:
      repo: your-username/alx-project-nexus-
      branch: main
    build_command: pip install -r requirements.txt && python manage.py collectstatic --noinput
    run_command: gunicorn config.wsgi:application --workers 2
    envs:
      - key: SECRET_KEY
        value: <your-secret-key>
      - key: DEBUG
        value: "False"
      - key: DATABASE_URL
        value: <database-connection-string>
    http_port: 8000
databases:
  - engine: PG
    name: jobboard-db
    version: "14"
```

---

### Option 4: AWS Elastic Beanstalk

#### Step 1: Install EB CLI

```bash
pip install awsebcli
```

#### Step 2: Initialize EB

```bash
eb init -p python-3.10 jobboard-api --region us-east-1
```

#### Step 3: Create Environment

```bash
eb create jobboard-env
```

#### Step 4: Configure Environment Variables

```bash
eb setenv SECRET_KEY=<your-secret-key> \
         DEBUG=False \
         DJANGO_SETTINGS_MODULE=config.settings.production \
         DATABASE_URL=<rds-connection-string>
```

#### Step 5: Deploy

```bash
eb deploy
```

#### Step 6: Open Application

```bash
eb open
```

---

## 📋 Production Checklist

Before deploying to production, ensure:

### Security

- [ ] `DEBUG = False` in production settings
- [ ] Strong `SECRET_KEY` generated and set
- [ ] `ALLOWED_HOSTS` properly configured
- [ ] SSL/HTTPS enabled
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`
- [ ] `CSRF_COOKIE_SECURE = True`
- [ ] Environment variables stored securely
- [ ] Database credentials not in code
- [ ] CORS configured properly

### Database

- [ ] PostgreSQL configured (not SQLite)
- [ ] Database backups enabled
- [ ] Connection pooling configured
- [ ] Migrations tested
- [ ] Database indexes created

### Performance

- [ ] Static files collected and served properly
- [ ] Gunicorn workers configured (2-4 workers recommended)
- [ ] Redis caching configured (optional)
- [ ] Database query optimization
- [ ] API rate limiting enabled

### Monitoring

- [ ] Error tracking configured (Sentry, Rollbar)
- [ ] Application monitoring (New Relic, DataDog)
- [ ] Log aggregation (Papertrail, Loggly)
- [ ] Uptime monitoring (Pingdom, UptimeRobot)

### Testing

- [ ] All tests passing
- [ ] CI/CD pipeline configured
- [ ] Automated deployments working
- [ ] Health check endpoint implemented

---

## 🔧 Production Settings

Create `config/settings/production.py`:

```python
from .base import *
import dj_database_url
import os

DEBUG = False

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# Security Settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Static Files
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Email (use production email backend)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
```

---

## 🔍 Troubleshooting

### Common Issues

**1. Static Files Not Loading**

Solution:
```bash
python manage.py collectstatic --noinput
```

Add to settings:
```python
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

**2. Database Connection Error**

- Verify `DATABASE_URL` is correct
- Check database credentials
- Ensure database server is running
- Check firewall rules

**3. 500 Internal Server Error**

- Check application logs
- Verify `DEBUG = False` with proper error handling
- Check `ALLOWED_HOSTS` includes your domain
- Verify all environment variables are set

**4. Migration Errors**

```bash
# Reset migrations (use carefully!)
python manage.py migrate --fake-initial

# Or run specific migration
python manage.py migrate app_name migration_name
```

---

## 📊 Monitoring and Logs

### Viewing Logs

**Render:**
```bash
# From dashboard or CLI
render logs jobboard-api
```

**Heroku:**
```bash
heroku logs --tail
```

**DigitalOcean:**
- View logs in App Platform dashboard

### Health Check Endpoint

Add to `config/urls.py`:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({'status': 'healthy'}, status=200)

urlpatterns = [
    path('health/', health_check),
    # ... other urls
]
```

---

## 🔄 Continuous Deployment

The GitHub Actions workflow automatically deploys to Render when changes are pushed to the `main` branch.

### Setup Required Secrets

In your GitHub repository settings, add:

1. `RENDER_API_KEY` - Your Render API key
2. `RENDER_SERVICE_ID` - Your Render service ID
3. `RENDER_SERVICE_URL` - Your deployed app URL

### Manual Deployment

To manually trigger a deployment:

1. Go to GitHub Actions
2. Select "CI/CD Pipeline" workflow
3. Click "Run workflow"
4. Choose branch and click "Run"

---

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/)
- [Render Docs](https://render.com/docs)
- [Heroku Django Guide](https://devcenter.heroku.com/articles/django-app-configuration)
- [DigitalOcean Tutorials](https://www.digitalocean.com/community/tutorials)
- [AWS Elastic Beanstalk](https://docs.aws.amazon.com/elasticbeanstalk/)

---

**Deployment complete! Your Job Board API is now live! 🎉**
