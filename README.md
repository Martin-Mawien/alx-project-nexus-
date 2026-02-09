### alx-project-nexus
> A production-ready RESTful API backend designed to manage job postings, categories, applications, and user roles with enterprise-grade authentication and real-time search.
Built on Django REST Framework and PostgreSQL, it delivers secure role‑based access, optimized queries performance, and comprehensive Swagger/OpenAPI documentation for sealess integration.
----

![Build Status](https://img.shields.io/github/actions/workflow/status/Martin-Mawien/alx-project-nexus-/ci.yml?branch=main)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Django Version](https://img.shields.io/badge/django-4.2.26-green)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Code-Coverage](https://img.shields.io/badge/coverage-95%25-brightgreen)

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Technologies](#-technologies)
- [Database Schema (ERD)](#-database-schema-erd)
- [API Endpoints](#-api-endpoints)
- [Project Structure](#-project-structure)
- [Setup & Installation](#-setup--installation)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [API Documentation](#-api-documentation)
- [Contributing](#-contributing)
- [License](#-license)

---
## 🎯 Overview
---
## ALX Project Nexus
A production-ready RESTful API backend designed to manage job postings, categories, applications, and user roles with enterprise-grade authentication and real-time search.
Built on Django REST Framework and PostgreSQL, it delivers secure role‑based access, optimized queries performance, and comprehensive Swagger/OpenAPI documentation for sealess integration.

## ✨ Festures
- Role - baased authentication (JWT in production)
- Job postings with category classification
- Applications with resume upload and workflow status
- Real - time search and filtering
- Swagger/OpenAPI documentation
- CI/CD pipeline with Github Actions
- Dockerized deployment with PostgreSQL

## Tech Stack
- **Backend:** Django REST framework
- **Database:** PostgreSQL
- **Auth:** JWT (production), session (develiopment)
- **Deployment:** Docker, Gunicorn, Render
- **CI/CD:** Github Actions
- **Docs:** Swagger, Redoc, Postman

## SETUP
```bash
git clone https://github.com/Martin-Mawien/alx-project-nexus-.git
cd alx-project-nexus
cp .env,example .env
docker-compose up --build
```

### Key Highlights

- ✅ **RESTful API Design** - Clean, intuitive endpoints following REST principles
- ✅ **Role-Based Access Control** - Granular permissions for Admins, Employers, and Job Seekers
- ✅ **Optimized Performance** - Database indexing and query optimization for fast search
- ✅ **Comprehensive Testing** - 95%+ code coverage with unit and integration tests
- ✅ **Production Ready** - Docker containerization, CI/CD pipeline, and cloud deployment
- ✅ **API Documentation** - Interactive Swagger/OpenAPI documentation

## ✨ Features
### Core Functionality

- **Job Management**
  - Create, read, update, and delete job postings (Admin/Employer only)
  - Advanced filtering by category, location, job type, and salary range
  - Full-text search with indexed queries for optimal performance
  - Pagination support for large datasets

- **User Authentication & Authorization**
  - JWT-based authentication with access and refresh tokens
  - Role-based permissions (Admin, Employer, Job Seeker)
  - Secure password hashing with Django's built-in security
  - Email verification and password reset functionality

- **Application Management**
  - Job seekers can apply to multiple positions
  - Resume/CV upload and management
  - Application status tracking (Pending, Reviewed, Shortlisted, Rejected, Accepted)
  - Admin dashboard for reviewing applications

- **Category Organization**
  - Hierarchical job categorization
  - CRUD operations for managing categories (Admin only)
  - Category-based job filtering and analytics

### Advanced Features

- **Real-time Notifications** - Email alerts for new applications and status updates
- **Analytics Dashboard** - Job posting analytics and application metrics
- **Rate Limiting** - API throttling to prevent abuse
- **CORS Support** - Configured for frontend integration
- **Caching** - Redis caching for frequently accessed data

## 🛠️ Technologies
### Backend Framework
- **Django 4.2.26** - High-level Python web framework with security patches
- **Django REST Framework 3.14+** - Powerful toolkit for building Web APIs
- **Python 3.10+** - Modern Python with type hints and performance improvements

### Database
- **PostgreSQL 14+** - Advanced open-source relational database
- **psycopg2** - PostgreSQL adapter for Python

### Authentication & Security
- **djangorestframework-simplejwt** - JSON Web Token authentication
- **django-cors-headers** - Cross-Origin Resource Sharing (CORS) handling
- **python-decouple** - Secure environment variable management

### API Documentation
- **drf-yasg** - Yet another Swagger generator for Django REST Framework
- **Swagger/OpenAPI 3.0** - Interactive API documentation

### Testing & Quality
- **pytest** - Advanced Python testing framework
- **pytest-django** - Django plugin for pytest
- **pytest-cov** - Coverage reporting for pytest
- **factory-boy** - Test fixtures for Django models

### DevOps & Deployment
- **Docker** - Containerization platform
- **Docker Compose** - Multi-container Docker applications
- **GitHub Actions** - CI/CD automation
- **Render** - Cloud platform for deployment
- **Gunicorn** - Python WSGI HTTP Server
- **Whitenoise** - Static file serving for Python web apps

### Additional Tools
- **Celery** - Asynchronous task queue (for email notifications)
- **Redis** - In-memory data structure store (caching & task queue)
- **Pillow** - Python Imaging Library (for image handling)

---

## 📊 Database Schema (ERD)

```mermaid
erDiagram
   ROLE {
   int id PK
   string name
   string description
   timestamp created_at
}
```
----

## PostgreSQL Schema

```sql
CREATE TABLE role (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL
DEFAULT NOW(),
    CONSTRAINT role_name_check
        CHECK (name IN ('admin',
'employer', 'job_seeker'))
);

/* ============================================================
   USER TABLE
   ============================================================ */
CREATE TABLE app_user (
    id SERIAL PRIMARY KEY,
    username VARCHAR(150) NOT NULL UNIQUE,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    role_id INTEGER NOT NULL REFERENCES role(id) ON DELETE RESTRICT,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

/* ============================================================
   CATEGORY TABLE
   ============================================================ */
CREATE TABLE category (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE,
    description TEXT,
    slug VARCHAR(150) NOT NULL UNIQUE,
    parent_id INTEGER REFERENCES category(id) ON DELETE SET NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

/* ============================================================
   JOB TABLE
   ============================================================ */
CREATE TABLE job (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    category_id INTEGER NOT NULL REFERENCES category(id) ON DELETE RESTRICT,
    location VARCHAR(200) NOT NULL,
    job_type VARCHAR(50) NOT NULL,
    salary_min NUMERIC(12,2),
    salary_max NUMERIC(12,2),
    currency VARCHAR(10),
    posted_by INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
    status VARCHAR(50) NOT NULL,
    deadline TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT job_type_check CHECK (job_type IN ('full-time', 'part-time', 'contract', 'remote')),
    CONSTRAINT job_status_check CHECK (status IN ('active', 'closed', 'draft'))
);

/* ============================================================
   APPLICATION TABLE
   ============================================================ */
CREATE TABLE application (
    id SERIAL PRIMARY KEY,
    job_id INTEGER NOT NULL REFERENCES job(id) ON DELETE CASCADE,
    user_id INTEGER NOT NULL REFERENCES app_user(id) ON DELETE CASCADE,
    resume_url VARCHAR(500) NOT NULL,
    cover_letter TEXT,
    status VARCHAR(50) NOT NULL,
    applied_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    reviewed_at TIMESTAMPTZ,
    reviewed_by INTEGER REFERENCES app_user(id) ON DELETE SET NULL,
    admin_notes TEXT,
    CONSTRAINT application_status_check CHECK (
        status IN ('pending', 'reviewed', 'shortlisted', 'rejected', 'accepted')
    )
);

/* ============================================================
   INDEXES FOR PERFORMANCE
   ============================================================ */

-- USER
CREATE INDEX idx_app_user_email ON app_user (email);
CREATE INDEX idx_app_user_username ON app_user (username);
CREATE INDEX idx_app_user_role_id ON app_user (role_id);

-- ROLE
CREATE INDEX idx_role_name ON role (name);

-- CATEGORY
CREATE INDEX idx_category_parent_id ON category (parent_id);
CREATE INDEX idx_category_slug ON category (slug);

-- JOB
CREATE INDEX idx_job_category_id ON job (category_id);
CREATE INDEX idx_job_posted_by ON job (posted_by);
CREATE INDEX idx_job_status ON job (status);
CREATE INDEX idx_job_job_type ON job (job_type);
CREATE INDEX idx_job_deadline ON job (deadline);

-- APPLICATION
CREATE INDEX idx_application_job_id ON application (job_id);
CREATE INDEX idx_application_user_id ON application (user_id);
CREATE INDEX idx_application_status ON application (status);
CREATE INDEX idx_application_reviewed_by ON application (reviewed_by);

/* ============================================================
   SEED DATA FOR ROLES
   ============================================================ */
INSERT INTO role (name, description)
VALUES
    ('admin', 'Platform administrator with full access'),
    ('employer', 'Employer who can post and manage jobs'),
    ('job_seeker', 'User who can search and apply for jobs')
ON CONFLICT (name) DO NOTHING;

```
---

## 📂 API Endpoints

### Authentication
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| POST | `/api/auth/register/` | Register new user account | Public |
| POST | `/api/auth/login/` | Authenticate user & return JWT tokens | Public |
| POST | `/api/auth/refresh/` | Refresh access token | Authenticated |
| POST | `/api/auth/logout/` | Invalidate refresh token | Authenticated |
| POST | `/api/auth/password-reset/` | Request password reset | Public |
| POST | `/api/auth/password-reset-confirm/` | Confirm password reset | Public |
| GET | `/api/auth/verify-email/{token}/` | Verify email address | Public |

### User Management
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/users/me/` | Get current user profile | Authenticated |
| PUT | `/api/users/me/` | Update current user profile | Authenticated |
| PATCH | `/api/users/me/` | Partial update current user | Authenticated |
| DELETE | `/api/users/me/` | Delete current user account | Authenticated |

### Jobs
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/jobs/` | List all jobs with filters | Public |
| POST | `/api/jobs/` | Create new job posting | Admin/Employer |
| GET | `/api/jobs/{id}/` | Retrieve job details | Public |
| PUT | `/api/jobs/{id}/` | Update job posting | Admin/Owner |
| PATCH | `/api/jobs/{id}/` | Partial update job | Admin/Owner |
| DELETE | `/api/jobs/{id}/` | Delete job posting | Admin/Owner |
| GET | `/api/jobs/{id}/applications/` | List applications for job | Admin/Owner |

**Query Parameters for Job Listing:**
- `category` - Filter by category ID
- `location` - Filter by location (partial match)
- `job_type` - Filter by job type
- `salary_min` - Minimum salary
- `salary_max` - Maximum salary
- `search` - Full-text search in title and description
- `ordering` - Sort by field (e.g., `-created_at`, `salary_min`)
- `page` - Page number for pagination
- `page_size` - Items per page (default: 20, max: 100)

### Categories
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/categories/` | List all categories | Public |
| POST | `/api/categories/` | Create new category | Admin |
| GET | `/api/categories/{id}/` | Retrieve category details | Public |
| PUT | `/api/categories/{id}/` | Update category | Admin |
| PATCH | `/api/categories/{id}/` | Partial update category | Admin |
| DELETE | `/api/categories/{id}/` | Delete category | Admin |
| GET | `/api/categories/{id}/jobs/` | List jobs in category | Public |

### Applications
| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/api/applications/` | List user's applications | Authenticated |
| POST | `/api/applications/` | Apply for a job | Job Seeker |
| GET | `/api/applications/{id}/` | Retrieve application details | Owner/Admin |
| PUT | `/api/applications/{id}/` | Update application | Owner/Admin |
| PATCH | `/api/applications/{id}/status/` | Update application status | Admin/Employer |
| DELETE | `/api/applications/{id}/` | Withdraw application | Owner |

---

## 📁 Project Structure

```
alx-project-nexus/
├── apps/
│   ├── users/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py          # User and Role models
│   │   ├── serializers.py     # User serializers
│   │   ├── views.py           # User viewsets and authentication
│   │   ├── urls.py            # User-related routes
│   │   ├── permissions.py     # Custom permissions
│   │   ├── tests.py           # User app tests
│   │   └── admin.py           # Django admin configuration
│   │
│   ├── jobs/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py          # Job model
│   │   ├── serializers.py     # Job serializers
│   │   ├── views.py           # Job viewsets
│   │   ├── urls.py            # Job-related routes
│   │   ├── filters.py         # Custom job filters
│   │   ├── tests.py           # Job app tests
│   │   └── admin.py           # Django admin configuration
│   │
│   ├── categories/
│   │   ├── migrations/
│   │   ├── __init__.py
│   │   ├── models.py          # Category model
│   │   ├── serializers.py     # Category serializers
│   │   ├── views.py           # Category viewsets
│   │   ├── urls.py            # Category-related routes
│   │   ├── tests.py           # Category app tests
│   │   └── admin.py           # Django admin configuration
│   │
│   └── applications/
│       ├── migrations/
│       ├── __init__.py
│       ├── models.py          # Application model
│       ├── serializers.py     # Application serializers
│       ├── views.py           # Application viewsets
│       ├── urls.py            # Application-related routes
│       ├── signals.py         # Email notification signals
│       ├── tests.py           # Application app tests
│       └── admin.py           # Django admin configuration
│
├── config/
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py            # Base settings
│   │   ├── development.py     # Development settings
│   │   ├── production.py      # Production settings
│   │   └── testing.py         # Test settings
│   ├── urls.py                # Main URL configuration
│   ├── wsgi.py                # WSGI application
│   └── asgi.py                # ASGI application
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py            # Pytest configuration and fixtures
│   ├── factories.py           # Model factories for testing
│   └── integration/           # Integration tests
│
├── docs/
│   ├── api/                   # API documentation
│   ├── deployment.md          # Deployment guide
│   └── postman/               # Postman collection
│
├── .github/
│   └── workflows/
│       ├── ci.yml             # Continuous Integration
│       └── deploy.yml         # Continuous Deployment
│
├── docker/
│   ├── Dockerfile             # Docker image definition
│   ├── docker-compose.yml     # Multi-container setup
│   └── entrypoint.sh          # Container entrypoint script
│
├── static/                    # Static files
├── media/                     # User-uploaded files (resumes, etc.)
├── .env.example               # Environment variables template
├── .gitignore                 # Git ignore rules
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── requirements-dev.txt       # Development dependencies
├── pytest.ini                 # Pytest configuration
├── CONTRIBUTING.md            # Contribution guidelines
├── LICENSE                    # MIT License
└── README.md                  # This file
```

### Best Practices Implemented

- **Modular Apps**: Each Django app (`users`, `jobs`, `categories`, `applications`) is self-contained
- **Separation of Concerns**: Models, serializers, views, and URLs are clearly separated
- **Settings Split**: Environment-specific settings (development, production, testing)
- **Custom Permissions**: Granular permission classes for role-based access
- **Model Managers**: Custom querysets and managers for complex queries
- **Signals**: Email notifications and post-save operations
- **Factory Pattern**: Test fixtures using factory-boy for consistent test data

---

## 🚀 Setup & Installation

### Prerequisites

- Python 3.10 or higher
- PostgreSQL 14 or higher
- Redis (optional, for caching and Celery)
- Git
- Virtual environment tool (venv, virtualenv, or conda)

### Local Development Setup

1. **Clone the Repository**

```bash
git clone https://github.com/Martin-Mawien/alx-project-nexus-.git
cd alx-project-nexus-
```

2. **Create and Activate Virtual Environment**

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/MacOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

3. **Install Dependencies**

```bash
# Install production dependencies
pip install -r requirements.txt

# Install development dependencies (for testing and linting)
pip install -r requirements-dev.txt
```

4. **Configure Environment Variables**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and configure the following variables:
# - SECRET_KEY: Django secret key (generate using: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')
# - DEBUG: Set to True for development
# - DATABASE_URL: PostgreSQL connection string
# - ALLOWED_HOSTS: Comma-separated list of allowed hosts
# - CORS_ALLOWED_ORIGINS: Allowed CORS origins
```

**Example `.env` file:**

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://username:password@localhost:5432/fursa_db

# JWT Settings
JWT_ACCESS_TOKEN_LIFETIME=60  # minutes
JWT_REFRESH_TOKEN_LIFETIME=1440  # minutes (24 hours)

# Email Configuration (for notifications)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# CORS Settings
CORS_ALLOWED_ORIGINS=http://localhost:3000,http://127.0.0.1:3000

# Redis (optional)
REDIS_URL=redis://localhost:6379/0

# File Upload Settings
MAX_UPLOAD_SIZE=5242880  # 5MB in bytes
```

5. **Set Up Database**

```bash
# Create PostgreSQL database
createdb jobboard_db

# Run migrations
python manage.py migrate

# Create superuser (admin account)
python manage.py createsuperuser

# Load initial data (optional)
python manage.py loaddata initial_roles initial_categories
```

6. **Collect Static Files**

```bash
python manage.py collectstatic --noinput
```

7. **Run Development Server**

```bash
python manage.py runserver
```

The API will be available at `http://localhost127.0.0.1:8000/`

8. **Access API Documentation**

- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- Django Admin: `http://localhost:8000/admin/`

### Docker Setup (Alternative)

```bash
# Build and start containers
docker-compose up -d

# Run migrations
docker-compose exec web python manage.py migrate

# Create superuser
docker-compose exec web python manage.py createsuperuser

# View logs
docker-compose logs -f web
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests with coverage report
pytest --cov=apps --cov-report=html --cov-report=term

# Run specific test file
pytest apps/users/tests.py

# Run with verbose output
pytest -v

# Run tests and stop on first failure
pytest --maxfail=1

# Run tests in parallel (faster)
pytest -n auto
```

### Test Coverage

```bash
# Generate HTML coverage report
pytest --cov=apps --cov-report=html

# Open coverage report
# On Linux/MacOS:
open htmlcov/index.html

# On Windows:
start htmlcov/index.html
```

### Testing Guidelines

- Maintain **95%+ code coverage**
- Write unit tests for models, serializers, and utility functions
- Write integration tests for API endpoints
- Use factory-boy for creating test data
- Mock external services (email, file uploads)
- Test both success and error scenarios
- Test permission and authentication logic

### Example Test Structure

```python
# apps/jobs/tests.py
import pytest
from rest_framework.test import APIClient
from tests.factories import UserFactory, JobFactory

@pytest.mark.django_db
class TestJobAPI:
    def test_list_jobs_public_access(self):
        """Public users can view job listings"""
        client = APIClient()
        JobFactory.create_batch(5)
        
        response = client.get('/api/jobs/')
        
        assert response.status_code == 200
        assert len(response.data['results']) == 5
    
    def test_create_job_requires_authentication(self):
        """Creating a job requires authentication"""
        client = APIClient()
        
        response = client.post('/api/jobs/', {})
        
        assert response.status_code == 401
```

---

## 🌐 Deployment

### Deployment Platforms

This application is configured for deployment on:
- **Render** (recommended for easy setup)
- **Heroku**
- **AWS (EC2, ECS, or Elastic Beanstalk)**
- **DigitalOcean App Platform**
- **Google Cloud Run**

### Render Deployment (Recommended)

1. **Create a Render Account**
   - Sign up at [render.com](https://render.com)

2. **Create PostgreSQL Database**
   - Create a new PostgreSQL database instance
   - Copy the internal database URL

3. **Create Web Service**
   - Connect your GitHub repository
   - Configure build and start commands:
    - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
     - Start Command: `gunicorn config.wsgi:application`

4. **Set Environment Variables**
   ```
   SECRET_KEY=<your-secret-key>
   DEBUG=False
   DATABASE_URL=<postgres-internal-url>
   ALLOWED_HOSTS=<your-app-name>.onrender.com
   DJANGO_SETTINGS_MODULE=config.settings.production
   ```

5. **Deploy**
   - Push changes to main branch
   - Render will automatically build and deploy

### CI/CD Pipeline (GitHub Actions)

The repository includes a GitHub Actions workflow for automated testing and deployment:

```yaml
# .github/workflows/ci.yml
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:14
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run tests
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost/test_db
        run: pytest --cov=apps --cov-report=xml
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - name: Deploy to Render
        env:
          RENDER_API_KEY: ${{ secrets.RENDER_API_KEY }}
          RENDER_SERVICE_ID: ${{ secrets.RENDER_SERVICE_ID }}
        run: |
          curl -X POST "https://api.render.com/v1/services/$RENDER_SERVICE_ID/deploys" \
            -H "Authorization: Bearer $RENDER_API_KEY" \
            -H "Content-Type: application/json"
```

### Environment-Specific Settings

The project uses environment-specific settings:

- **Development** (`config.settings.development`): Debug enabled, SQLite database option
- **Production** (`config.settings.production`): Debug disabled, security settings enforced
- **Testing** (`config.settings.testing`): Fast test database, disabled migrations

---

## 📖 API Documentation

### Swagger/OpenAPI

Interactive API documentation is available at:
- **Swagger UI**: `/api/docs/` - Interactive API explorer
- **ReDoc**: `/api/redoc/` - Clean API reference documentation
- **OpenAPI Schema**: `/api/schema/` - Raw OpenAPI 3.0 schema (JSON/YAML)

### Postman Collection

A comprehensive Postman collection is available in the `docs/postman/` directory:

1. **Import Collection**
   - Open Postman
   - Click Import → Upload Files
   - Select `docs/postman/Job_Board_API.postman_collection.json`

2. **Configure Environment**
   - Import `docs/postman/Job_Board_API.postman_environment.json`
   - Update variables:
    - `base_url`: Your API base URL
     - `access_token`: JWT access token (obtained from login)

3. **Authentication Flow**
   - Register a new user → `/api/auth/register/`
   - Login → `/api/auth/login/` (saves token automatically)
   - All subsequent requests will use the saved token

### API Response Format

All API responses follow a consistent format:

**Success Response:**
```json
{
  "count": 42,
  "next": "http://api.example.com/jobs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Senior Backend Developer",
      "description": "We are seeking...",
      "category": {
        "id": 2,
        "name": "Software Development"
      },
      "location": "Remote",
      "job_type": "full-time",
      "salary_min": 80000,
      "salary_max": 120000,
      "created_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

**Error Response:**
```json
{
  "error": "ValidationError",
  "message": "Invalid input data",
  "details": {
    "title": ["This field is required."],
    "category": ["Invalid category ID."]
  }
}
```

### Rate Limiting

API endpoints are rate-limited to prevent abuse:
- **Anonymous users**: 100 requests per hour
- **Authenticated users**: 1000 requests per hour
- **Admin users**: Unlimited

Rate limit headers are included in all responses:
```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1642345678
```

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Quick Contribution Guide

1. **Fork the Repository**
   ```bash
   # Click "Fork" on GitHub, then clone your fork
   git clone https://github.com/YOUR-USERNAME/alx-project-nexus-.git
   cd alx-project-nexus-
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/bug-description
   ```

3. **Make Your Changes**
   - Follow PEP 8 style guide
   - Write meaningful commit messages
   - Add tests for new features
   - Update documentation as needed

4. **Run Tests and Linting**
   ```bash
   # Run tests
   pytest

   # Check code style
   flake8 apps/
   black apps/ --check
   isort apps/ --check-only
   ```

5. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add job search by salary range"
   ```

6. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then create a pull request on GitHub.

### Commit Message Convention

Follow [Conventional Commits](https://www.conventionalcommits.org/):

- `feat:` - New feature
- `fix:` - Bug fix
- `docs:` - Documentation changes
- `style:` - Code style changes (formatting, missing semi-colons, etc.)
- `refactor:` - Code refactoring
- `perf:` - Performance improvements
- `test:` - Adding or updating tests
- `chore:` - Maintenance tasks
- `ci:` - CI/CD pipeline changes

**Examples:**
```
feat: add job filtering by salary range
fix: resolve application submission error for authenticated users
docs: update API endpoint documentation
perf: optimize job search query with database indexes
test: add unit tests for user registration
```

### Code Style

- Follow [PEP 8](https://pep8.org/) style guide
- Use [Black](https://github.com/psf/black) for code formatting
- Use [isort](https://pycqa.github.io/isort/) for import sorting
- Use [flake8](https://flake8.pycqa.org/) for linting
- Maximum line length: 88 characters (Black default)
- Use type hints where applicable

### Pull Request Guidelines

- Provide a clear description of changes
- Reference related issues (e.g., "Fixes #123")
- Ensure all tests pass
- Maintain or improve code coverage
- Update documentation if needed
- Request reviews from maintainers

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 Job Board Backend Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- [Django](https://www.djangoproject.com/) - The web framework for perfectionists with deadlines
- [Django REST Framework](https://www.django-rest-framework.org/) - Powerful and flexible toolkit for building Web APIs
- [PostgreSQL](https://www.postgresql.org/) - The world's most advanced open source database
- All contributors who help improve this project

---

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/Martin-Mawien/alx-project-nexus-/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Martin-Mawien/alx-project-nexus-/discussions)
- **Email**: support@jobboard-api.com

---

**Built with ❤️ by the Job Board Team**
