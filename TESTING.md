# Testing Guide

## Manual Testing

### Prerequisites
- Server running: `python manage.py runserver`
- Database seeded: `python manage.py seed_data`

### Test Scenarios

#### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/auth/users/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123",
    "role": "JOB_SEEKER",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Expected**: 201 Created with user data and token

#### 2. User Login
```bash
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "jdoe",
    "password": "seeker123"
  }'
```

**Expected**: 200 OK with token and user data
**Save the token** for subsequent requests

#### 3. Get Current User Profile
```bash
curl -H "Authorization: Token YOUR_TOKEN_HERE" \
  http://localhost:8000/api/auth/users/me/
```

**Expected**: 200 OK with current user data

#### 4. List Categories
```bash
curl http://localhost:8000/api/categories/
```

**Expected**: 200 OK with paginated list of categories

#### 5. List Jobs
```bash
# All jobs
curl http://localhost:8000/api/jobs/

# Remote jobs only
curl http://localhost:8000/api/jobs/?is_remote=true

# Search for Python jobs
curl http://localhost:8000/api/jobs/?search=python

# Filter by category
curl http://localhost:8000/api/jobs/?category=1
```

**Expected**: 200 OK with paginated list of jobs

#### 6. Get Job Details
```bash
curl http://localhost:8000/api/jobs/senior-python-developer-techcorp-inc/
```

**Expected**: 200 OK with detailed job information

#### 7. Create Job (Employer Only)
```bash
# First login as employer
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "techcorp", "password": "employer123"}'

# Then create job
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Authorization: Token EMPLOYER_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Job Position",
    "slug": "test-job-position-techcorp",
    "description": "This is a test job",
    "requirements": "Test requirements",
    "category_id": 1,
    "job_type": "FULL_TIME",
    "experience_level": "INTERMEDIATE",
    "location": "Remote",
    "is_remote": true,
    "salary_min": 80000,
    "salary_max": 120000
  }'
```

**Expected**: 201 Created with job data

#### 8. Submit Job Application (Job Seeker Only)
```bash
# Login as job seeker
curl -X POST http://localhost:8000/api/auth/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "jdoe", "password": "seeker123"}'

# Submit application
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Token JOB_SEEKER_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "job_id": 3,
    "cover_letter": "I am interested in this position",
    "resume_url": "https://example.com/resume.pdf"
  }'
```

**Expected**: 201 Created with application data

#### 9. View Applications (Role-based)
```bash
# Job seeker sees only their applications
curl -H "Authorization: Token JOB_SEEKER_TOKEN_HERE" \
  http://localhost:8000/api/applications/

# Employer sees applications for their jobs
curl -H "Authorization: Token EMPLOYER_TOKEN_HERE" \
  http://localhost:8000/api/applications/
```

**Expected**: 200 OK with role-filtered applications

#### 10. Update Application Status (Employer Only)
```bash
curl -X PATCH http://localhost:8000/api/applications/1/update_status/ \
  -H "Authorization: Token EMPLOYER_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "status": "REVIEWING",
    "notes": "Good candidate, will schedule interview"
  }'
```

**Expected**: 200 OK with updated application

## Testing Permission Errors

### 1. Try to Create Job as Job Seeker
```bash
curl -X POST http://localhost:8000/api/jobs/ \
  -H "Authorization: Token JOB_SEEKER_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"title": "Test", ...}'
```

**Expected**: 403 Forbidden

### 2. Try to Apply to Same Job Twice
```bash
# Apply first time (should succeed)
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Token JOB_SEEKER_TOKEN_HERE" \
  -d '{"job_id": 1, "cover_letter": "..."}'

# Apply second time (should fail)
curl -X POST http://localhost:8000/api/applications/ \
  -H "Authorization: Token JOB_SEEKER_TOKEN_HERE" \
  -d '{"job_id": 1, "cover_letter": "..."}'
```

**Expected**: 400 Bad Request - "You have already applied to this job"

### 3. Try to Update Other Employer's Job
```bash
curl -X PUT http://localhost:8000/api/jobs/senior-python-developer-techcorp-inc/ \
  -H "Authorization: Token OTHER_EMPLOYER_TOKEN_HERE" \
  -d '{"title": "Modified"}'
```

**Expected**: 403 Forbidden

## Automated Testing (Future)

Create tests in `jobs/tests.py` and `accounts/tests.py`:

```python
from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

class JobAPITestCase(APITestCase):
    def test_list_jobs(self):
        response = self.client.get('/api/jobs/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_create_job_as_employer(self):
        # Test implementation
        pass
```

Run with: `python manage.py test`
