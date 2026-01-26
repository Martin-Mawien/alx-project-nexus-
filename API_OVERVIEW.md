# API Overview

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints except registration and login require authentication via Token.

Include the token in the Authorization header:
```
Authorization: Token <your-token-here>
```

## Response Format
All responses follow this structure:
```json
{
  "count": 10,
  "next": "http://localhost:8000/api/jobs/?page=2",
  "previous": null,
  "results": [...]
}
```

## User Roles

### EMPLOYER
- Can create, update, delete their own jobs
- Can view applications for their jobs
- Can update application status

### JOB_SEEKER
- Can view all jobs
- Can submit applications
- Can view their own applications

### ADMIN
- Full access to all resources

## Common Query Parameters

### Pagination
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)

### Filtering
Jobs can be filtered by:
- `category` - Category ID
- `job_type` - FULL_TIME, PART_TIME, CONTRACT, INTERNSHIP, TEMPORARY
- `experience_level` - ENTRY, INTERMEDIATE, SENIOR, EXECUTIVE
- `is_remote` - true/false
- `is_active` - true/false
- `employer` - Employer user ID

Applications can be filtered by:
- `status` - PENDING, REVIEWING, SHORTLISTED, REJECTED, ACCEPTED
- `job` - Job ID

### Search
- `search` - Search in title, description, location, requirements (jobs)
- `search` - Search in username, email, company name (users)

### Ordering
- `ordering` - Field name to order by (prefix with `-` for descending)
  - Jobs: `created_at`, `title`, `deadline`
  - Applications: `created_at`, `status`
  - Categories: `name`, `created_at`

## Error Responses

### 400 Bad Request
```json
{
  "field_name": ["Error message"]
}
```

### 401 Unauthorized
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden
```json
{
  "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found
```json
{
  "detail": "Not found."
}
```

## Rate Limiting
Currently no rate limiting is implemented. Consider adding in production.

## CORS
CORS is not configured by default. Add `django-cors-headers` if needed for frontend applications.
