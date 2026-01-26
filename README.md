# Job Board Backend

A production-ready backend system for managing job postings, categories, and applications. Built with Django REST Framework and PostgreSQL, it features role-based authentication, optimized queries, and Swagger/OpenAPI documentation.

## 🚀 Features

### Core Functionality
- **Job Posting Management**: Create, update, delete, and search job postings
- **Category Organization**: Organize jobs into categories
- **Application System**: Submit and track job applications
- **User Management**: Role-based authentication (Admin, Employer, Job Seeker)

### Technical Features
- **RESTful API**: Fully featured REST API with Django REST Framework
- **Authentication**: Token-based authentication with secure role management
- **Database**: PostgreSQL support with SQLite fallback for development
- **Query Optimization**: Efficient database queries with `select_related` and `prefetch_related`
- **Filtering & Search**: Advanced filtering, search, and ordering capabilities
- **Pagination**: Built-in pagination for all list endpoints
- **API Documentation**: Interactive Swagger/OpenAPI documentation
- **Admin Interface**: Django admin panel for easy management

## 📋 Requirements

- Python 3.8+
- PostgreSQL 12+ (or SQLite for development)
- pip (Python package manager)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Martin-Mawien/alx-project-nexus-.git
cd alx-project-nexus-
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the project root (you can copy from `.env.example`):

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
# Database Configuration (PostgreSQL)
DB_NAME=jobboard_db
DB_USER=postgres
DB_PASSWORD=your_password_here
DB_HOST=localhost
DB_PORT=5432

# Django Configuration
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

**For Development (SQLite)**: Set environment variable:
```bash
export USE_SQLITE=True
```

### 4. Run Database Migrations

```bash
python manage.py migrate
```

### 5. Create Sample Data (Optional)

```bash
python manage.py seed_data
```

This creates test users:
- **Admin**: `username=admin, password=admin123`
- **Employer**: `username=techcorp, password=employer123`
- **Employer**: `username=innovate, password=employer123`
- **Job Seeker**: `username=jdoe, password=seeker123`
- **Job Seeker**: `username=asmith, password=seeker123`

### 6. Create a Superuser (Alternative)

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

### Interactive Documentation
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Admin Panel
- **Django Admin**: http://localhost:8000/admin/

## 🔑 API Endpoints

### Authentication (`/api/auth/`)
- `POST /api/auth/users/register/` - Register a new user
- `POST /api/auth/users/login/` - Login and get authentication token
- `POST /api/auth/users/logout/` - Logout (requires authentication)
- `GET /api/auth/users/me/` - Get current user profile

### Categories (`/api/categories/`)
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category (requires authentication)
- `GET /api/categories/{slug}/` - Get category details
- `PUT /api/categories/{slug}/` - Update a category
- `DELETE /api/categories/{slug}/` - Delete a category
- `GET /api/categories/{slug}/jobs/` - Get all jobs in a category

### Jobs (`/api/jobs/`)
- `GET /api/jobs/` - List all jobs (with filtering, search, pagination)
- `POST /api/jobs/` - Create a new job (employers only)
- `GET /api/jobs/{slug}/` - Get job details
- `PUT /api/jobs/{slug}/` - Update a job (job owner only)
- `DELETE /api/jobs/{slug}/` - Delete a job (job owner only)
- `GET /api/jobs/{slug}/applications/` - Get applications for a job (job owner only)

### Applications (`/api/applications/`)
- `GET /api/applications/` - List applications (filtered by role)
- `POST /api/applications/` - Submit a job application (job seekers only)
- `GET /api/applications/{id}/` - Get application details
- `PUT /api/applications/{id}/` - Update application
- `PATCH /api/applications/{id}/update_status/` - Update application status (employer only)

## 🔍 API Usage Examples

### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "user@example.com",
    "password": "securepass123",
    "password_confirm": "securepass123",
    "role": "JOB_SEEKER",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### Login

```bash
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jdoe",
    "password": "seeker123"
  }'
```

Response:
```json
{
  "token": "your-auth-token-here",
  "user": {
    "id": 1,
    "username": "jdoe",
    "email": "jdoe@email.com",
    "role": "JOB_SEEKER",
    ...
  }
}
```

### List Jobs with Filters

```bash
# Get all remote jobs
curl http://localhost:8000/api/jobs/?is_remote=true

# Search for Python jobs
curl http://localhost:8000/api/jobs/?search=python

# Filter by category
curl http://localhost:8000/api/jobs/?category=1

# Combine filters
curl http://localhost:8000/api/jobs/?is_remote=true&job_type=FULL_TIME&search=developer
```

### Create a Job (Employer Only)

```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Backend Developer",
    "slug": "backend-developer-acme",
    "description": "We are looking for a backend developer...",
    "requirements": "Python, Django, REST APIs",
    "category_id": 1,
    "job_type": "FULL_TIME",
    "experience_level": "INTERMEDIATE",
    "location": "San Francisco, CA",
    "is_remote": true,
    "salary_min": 100000,
    "salary_max": 140000
  }'
```

### Submit a Job Application (Job Seeker Only)

```bash
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Token your-auth-token" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 1,
    "cover_letter": "I am very interested in this position...",
    "resume_url": "https://example.com/resume.pdf"
  }'
```

## 🏗️ Database Models

### User Model
- Custom user model extending Django's AbstractUser
- Fields: username, email, role, company_name, phone_number, bio
- Roles: ADMIN, EMPLOYER, JOB_SEEKER

### Category Model
- Fields: name, slug, description
- One-to-many relationship with Job

### Job Model
- Fields: title, slug, description, requirements, responsibilities
- Employment details: job_type, experience_level, location, is_remote
- Salary information: salary_min, salary_max, salary_currency
- Foreign keys: category, employer (User)
- Indexed fields for optimized queries

### Application Model
- Fields: cover_letter, resume_url, status, notes
- Foreign keys: job (Job), applicant (User)
- Status choices: PENDING, REVIEWING, SHORTLISTED, REJECTED, ACCEPTED
- Unique constraint: One application per user per job

## 🔐 Role-Based Permissions

### Admin
- Full access to all resources
- Can manage users, categories, jobs, and applications

### Employer
- Can create, update, and delete their own job postings
- Can view and manage applications for their jobs
- Can update application status

### Job Seeker
- Can view all jobs and categories
- Can submit applications to jobs
- Can view and update their own applications (limited fields)

## 🚀 Performance Optimizations

- **Query Optimization**: Uses `select_related()` and `prefetch_related()` for efficient database queries
- **Database Indexing**: Indexed fields for faster lookups
- **Pagination**: Reduces payload size for large datasets
- **Caching Ready**: Structure supports easy integration with caching solutions

## 🧪 Testing

Run tests (when test suite is implemented):

```bash
python manage.py test
```

## 📦 Production Deployment

### PostgreSQL Setup

1. Create PostgreSQL database:
```sql
CREATE DATABASE jobboard_db;
CREATE USER jobboard_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE jobboard_db TO jobboard_user;
```

2. Update `.env` with PostgreSQL credentials
3. Remove `USE_SQLITE` environment variable
4. Run migrations: `python manage.py migrate`

### Security Checklist

- [ ] Set `DEBUG=False` in production
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Use environment variables for sensitive data
- [ ] Set up HTTPS
- [ ] Configure CORS if needed
- [ ] Set up database backups
- [ ] Configure static files serving

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License.

## 👥 Authors

- Martin Mawien - Initial work

## 🙏 Acknowledgments

- Django REST Framework for the excellent API framework
- drf-spectacular for automatic API documentation
- The Django community for continuous support
