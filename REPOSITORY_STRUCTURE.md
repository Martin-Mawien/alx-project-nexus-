# Job Board Backend - Repository Structure Guide

This document outlines the recommended Django project structure for the Job Board Backend API, following best practices and industry standards.

## 📁 Complete Project Structure

```
job-board-backend/
│
├── apps/                           # Django applications
│   ├── __init__.py
│   │
│   ├── users/                      # User management app
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models.py               # User, Role models
│   │   ├── serializers.py          # User serializers (registration, profile, etc.)
│   │   ├── views.py                # Authentication & user viewsets
│   │   ├── urls.py                 # User-related URL routes
│   │   ├── permissions.py          # Custom permission classes (IsAdmin, IsOwner)
│   │   ├── managers.py             # Custom user manager
│   │   ├── signals.py              # User-related signals (email verification)
│   │   ├── validators.py           # Custom validators
│   │   ├── tests.py                # User app tests
│   │   ├── admin.py                # Django admin configuration
│   │   └── apps.py                 # App configuration
│   │
│   ├── jobs/                       # Job management app
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models.py               # Job model with fields and methods
│   │   ├── serializers.py          # Job serializers (list, detail, create)
│   │   ├── views.py                # Job viewsets and custom actions
│   │   ├── urls.py                 # Job-related URL routes
│   │   ├── filters.py              # Custom filter backends for search
│   │   ├── permissions.py          # Job-specific permissions
│   │   ├── querysets.py            # Custom querysets and managers
│   │   ├── tests.py                # Job app tests
│   │   ├── admin.py                # Django admin configuration
│   │   └── apps.py                 # App configuration
│   │
│   ├── categories/                 # Category management app
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models.py               # Category model (hierarchical)
│   │   ├── serializers.py          # Category serializers
│   │   ├── views.py                # Category viewsets
│   │   ├── urls.py                 # Category-related URL routes
│   │   ├── managers.py             # Category tree manager
│   │   ├── tests.py                # Category app tests
│   │   ├── admin.py                # Django admin configuration
│   │   └── apps.py                 # App configuration
│   │
│   ├── applications/               # Job application management app
│   │   ├── migrations/
│   │   │   └── __init__.py
│   │   ├── __init__.py
│   │   ├── models.py               # Application model
│   │   ├── serializers.py          # Application serializers
│   │   ├── views.py                # Application viewsets
│   │   ├── urls.py                 # Application-related URL routes
│   │   ├── permissions.py          # Application permissions
│   │   ├── signals.py              # Email notifications on status change
│   │   ├── tasks.py                # Celery tasks for email sending
│   │   ├── tests.py                # Application app tests
│   │   ├── admin.py                # Django admin configuration
│   │   └── apps.py                 # App configuration
│   │
│   └── core/                       # Shared utilities (optional)
│       ├── __init__.py
│       ├── models.py               # Abstract base models (TimeStampedModel)
│       ├── serializers.py          # Base serializers
│       ├── permissions.py          # Common permissions
│       ├── pagination.py           # Custom pagination classes
│       ├── exceptions.py           # Custom exception handlers
│       └── utils.py                # Utility functions
│
├── config/                         # Project configuration
│   ├── __init__.py
│   ├── settings/
│   │   ├── __init__.py
│   │   ├── base.py                 # Base settings (shared)
│   │   ├── development.py          # Development-specific settings
│   │   ├── production.py           # Production-specific settings
│   │   └── testing.py              # Test-specific settings
│   ├── urls.py                     # Main URL configuration
│   ├── wsgi.py                     # WSGI application entry point
│   ├── asgi.py                     # ASGI application entry point
│   └── celery.py                   # Celery configuration
│
├── tests/                          # Centralized test suite
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures and configuration
│   ├── factories.py                # Model factories (factory-boy)
│   ├── fixtures/                   # Test data fixtures
│   │   ├── users.json
│   │   ├── jobs.json
│   │   └── categories.json
│   ├── unit/                       # Unit tests
│   │   ├── __init__.py
│   │   ├── test_models.py
│   │   ├── test_serializers.py
│   │   └── test_utils.py
│   └── integration/                # Integration tests
│       ├── __init__.py
│       ├── test_auth_api.py
│       ├── test_jobs_api.py
│       ├── test_categories_api.py
│       └── test_applications_api.py
│
├── docs/                           # Documentation
│   ├── api/
│   │   ├── authentication.md       # Authentication guide
│   │   ├── endpoints.md            # API endpoints reference
│   │   └── examples.md             # Request/response examples
│   ├── deployment.md               # Deployment guide
│   ├── development.md              # Development setup guide
│   ├── architecture.md             # System architecture
│   └── postman/
│       ├── Job_Board_API.postman_collection.json
│       └── Job_Board_API.postman_environment.json
│
├── .github/                        # GitHub specific files
│   ├── workflows/
│   │   ├── ci.yml                  # CI/CD pipeline
│   │   └── deploy.yml              # Deployment workflow
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   └── PULL_REQUEST_TEMPLATE.md
│
├── docker/                         # Docker configuration
│   ├── Dockerfile                  # Main Dockerfile
│   ├── docker-compose.yml          # Multi-container setup
│   ├── entrypoint.sh               # Container entrypoint script
│   └── nginx/
│       └── nginx.conf              # Nginx configuration (for production)
│
├── static/                         # Static files (CSS, JS, images)
│   ├── admin/                      # Django admin static files
│   ├── css/
│   ├── js/
│   └── images/
│
├── media/                          # User-uploaded files
│   ├── resumes/                    # Uploaded resumes
│   └── documents/                  # Other documents
│
├── staticfiles/                    # Collected static files (production)
│
├── locale/                         # Internationalization files
│   ├── en/
│   │   └── LC_MESSAGES/
│   │       ├── django.po
│   │       └── django.mo
│   └── es/
│       └── LC_MESSAGES/
│           ├── django.po
│           └── django.mo
│
├── scripts/                        # Utility scripts
│   ├── init_db.sh                  # Database initialization
│   ├── backup_db.sh                # Database backup
│   ├── deploy.sh                   # Deployment script
│   └── seed_data.py                # Seed database with sample data
│
├── .env.example                    # Environment variables template
├── .env                            # Environment variables (not in git)
├── .gitignore                      # Git ignore rules
├── .dockerignore                   # Docker ignore rules
├── .editorconfig                   # Editor configuration
├── .pre-commit-config.yaml         # Pre-commit hooks configuration
│
├── manage.py                       # Django management script
├── requirements.txt                # Production dependencies
├── requirements-dev.txt            # Development dependencies
│
├── pytest.ini                      # Pytest configuration
├── setup.cfg                       # Project metadata and tool configs
├── pyproject.toml                  # Python project configuration (Black, isort)
│
├── Makefile                        # Common development commands
│
├── README.md                       # Project documentation
├── CONTRIBUTING.md                 # Contribution guidelines
├── LICENSE                         # License file (MIT)
├── CHANGELOG.md                    # Version history
└── CODE_OF_CONDUCT.md              # Code of conduct
```

---

## 🏗️ Detailed Component Breakdown

### 1. Apps Directory (`apps/`)

Each Django app follows a modular structure with clear separation of concerns:

#### **Users App** (`apps/users/`)

Handles user authentication, registration, and profile management.

**Key Files:**
- `models.py`: Custom User model extending AbstractUser, Role model
- `serializers.py`: UserRegistrationSerializer, UserProfileSerializer, LoginSerializer
- `views.py`: RegisterView, LoginView, LogoutView, UserProfileViewSet
- `permissions.py`: IsOwnerOrAdmin, IsAdmin
- `managers.py`: UserManager for custom user creation logic

**Example Model:**
```python
# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class Role(models.Model):
    ADMIN = 'admin'
    EMPLOYER = 'employer'
    JOB_SEEKER = 'job_seeker'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (EMPLOYER, 'Employer'),
        (JOB_SEEKER, 'Job Seeker'),
    ]
    
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.get_name_display()

class User(AbstractUser):
    email = models.EmailField(unique=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name='users')
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=20, blank=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    
    def __str__(self):
        return self.email
```

#### **Jobs App** (`apps/jobs/`)

Manages job postings with advanced filtering and search.

**Key Files:**
- `models.py`: Job model with category, location, salary fields
- `serializers.py`: JobListSerializer, JobDetailSerializer, JobCreateSerializer
- `views.py`: JobViewSet with custom actions
- `filters.py`: JobFilter using django-filter for advanced filtering
- `querysets.py`: Custom queryset methods for optimized queries

**Example Model:**
```python
# apps/jobs/models.py
from django.db import models
from apps.users.models import User
from apps.categories.models import Category

class JobManager(models.Manager):
    def active(self):
        return self.filter(status='active')
    
    def for_category(self, category):
        return self.filter(category=category, status='active')

class Job(models.Model):
    FULL_TIME = 'full-time'
    PART_TIME = 'part-time'
    CONTRACT = 'contract'
    REMOTE = 'remote'
    
    JOB_TYPE_CHOICES = [
        (FULL_TIME, 'Full Time'),
        (PART_TIME, 'Part Time'),
        (CONTRACT, 'Contract'),
        (REMOTE, 'Remote'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    ]
    
    title = models.CharField(max_length=255, db_index=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name='jobs')
    location = models.CharField(max_length=255, db_index=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default='USD')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    deadline = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = JobManager()
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['category', 'status']),
            models.Index(fields=['location', 'status']),
        ]
    
    def __str__(self):
        return self.title
```

#### **Categories App** (`apps/categories/`)

Manages job categories with hierarchical structure support.

**Example Model:**
```python
# apps/categories/models.py
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    parent = models.ForeignKey(
        'self', 
        null=True, 
        blank=True, 
        on_delete=models.CASCADE, 
        related_name='subcategories'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name
```

#### **Applications App** (`apps/applications/`)

Handles job applications with status tracking.

**Example Model:**
```python
# apps/applications/models.py
from django.db import models
from apps.users.models import User
from apps.jobs.models import Job

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
    ]
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume_url = models.URLField(max_length=500)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewed_by = models.ForeignKey(
        User, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL, 
        related_name='reviewed_applications'
    )
    admin_notes = models.TextField(blank=True)
    
    class Meta:
        unique_together = ['job', 'user']
        ordering = ['-applied_at']
        indexes = [
            models.Index(fields=['status', '-applied_at']),
            models.Index(fields=['job', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.email} - {self.job.title}"
```

---

## 🔧 Configuration (`config/`)

### Settings Structure

**Base Settings** (`config/settings/base.py`):
- Shared settings across all environments
- Installed apps, middleware
- Database configuration templates
- Static files, media files
- Email configuration

**Development Settings** (`config/settings/development.py`):
```python
from .base import *

DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

**Production Settings** (`config/settings/production.py`):
```python
from .base import *
import dj_database_url

DEBUG = False
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=lambda v: [s.strip() for s in v.split(',')])

DATABASES = {
    'default': dj_database_url.config(default=config('DATABASE_URL'))
}

# Security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 🧪 Testing Structure

### Factories (`tests/factories.py`)

Use factory-boy for creating test data:

```python
import factory
from apps.users.models import User, Role
from apps.jobs.models import Job

class RoleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Role
    
    name = Role.JOB_SEEKER
    description = "Default job seeker role"

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
    
    username = factory.Sequence(lambda n: f"user{n}")
    email = factory.Sequence(lambda n: f"user{n}@example.com")
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    role = factory.SubFactory(RoleFactory)

class JobFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Job
    
    title = factory.Faker('job')
    description = factory.Faker('paragraph')
    location = factory.Faker('city')
    job_type = Job.FULL_TIME
    posted_by = factory.SubFactory(UserFactory)
```

---

## 📝 Best Practices

### 1. **Model Design**
- Use `db_index=True` for frequently queried fields
- Implement `__str__()` method for all models
- Use `Meta.ordering` for default ordering
- Add database constraints for data integrity

### 2. **Serializer Design**
- Use `ModelSerializer` for CRUD operations
- Create separate serializers for list, detail, and create operations
- Implement custom validation methods
- Use `read_only_fields` and `write_only_fields`

### 3. **View Design**
- Use ViewSets for standard CRUD operations
- Implement custom actions with `@action` decorator
- Use appropriate permission classes
- Return proper HTTP status codes

### 4. **URL Design**
- Use routers for ViewSets
- Group related URLs in app-specific `urls.py`
- Use meaningful URL patterns

### 5. **Testing**
- Write tests for all models, serializers, and views
- Use factories for creating test data
- Test both success and error scenarios
- Maintain high test coverage (95%+)

---

## 🚀 Development Workflow

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature
   ```

2. **Make Changes**
   - Update models, serializers, views
   - Write tests
   - Update documentation

3. **Run Tests**
   ```bash
   pytest
   ```

4. **Check Code Quality**
   ```bash
   black apps/
   isort apps/
   flake8 apps/
   ```

5. **Commit and Push**
   ```bash
   git add .
   git commit -m "feat: add new feature"
   git push origin feature/your-feature
   ```

---

This structure provides a solid foundation for building a scalable, maintainable Django REST API following industry best practices.
