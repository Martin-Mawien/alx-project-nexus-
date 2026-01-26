# API Documentation Guide

This guide provides information on how to use and integrate with the Job Board Backend API.

## 📚 Documentation Types

The API documentation is available in multiple formats:

### 1. Swagger UI (Interactive)
- **URL**: `http://localhost:8000/api/docs/`
- **Features**: 
  - Interactive API explorer
  - Try out endpoints directly in the browser
  - View request/response schemas
  - Test authentication flows

### 2. ReDoc (Reference)
- **URL**: `http://localhost:8000/api/redoc/`
- **Features**:
  - Clean, organized reference documentation
  - Search functionality
  - Code samples in multiple languages
  - Downloadable OpenAPI schema

### 3. OpenAPI Schema
- **URL**: `http://localhost:8000/api/schema/`
- **Formats**: JSON, YAML
- **Usage**: Import into API clients, generate SDKs

---

## 🔧 Setting Up Swagger/OpenAPI

### Installation

The API uses `drf-yasg` for Swagger/OpenAPI documentation.

```bash
pip install drf-yasg
```

### Configuration

Add to `config/settings/base.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'drf_yasg',
]
```

### URL Configuration

Add to `config/urls.py`:

```python
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Job Board API",
        default_version='v1',
        description="""
        RESTful API for Job Board Application
        
        ## Features
        - JWT Authentication
        - Job Management (CRUD)
        - Category Management
        - Application Tracking
        - Role-Based Access Control
        
        ## Authentication
        To access protected endpoints, include the JWT token in the Authorization header:
        ```
        Authorization: Bearer <your-access-token>
        ```
        
        Obtain tokens via `/api/auth/login/` endpoint.
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@jobboard-api.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    # API documentation
    re_path(r'^api/docs/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    re_path(r'^api/schema/$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    
    # API endpoints
    path('api/', include('apps.users.urls')),
    path('api/', include('apps.jobs.urls')),
    path('api/', include('apps.categories.urls')),
    path('api/', include('apps.applications.urls')),
]
```

---

## 📝 Documenting Your API

### 1. Documenting Views

Use docstrings to add descriptions to ViewSets:

```python
from rest_framework import viewsets
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class JobViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing job postings.
    
    list:
    Return a list of all jobs with optional filtering.
    
    create:
    Create a new job posting (Admin/Employer only).
    
    retrieve:
    Return details of a specific job.
    
    update:
    Update a job posting (Admin/Owner only).
    
    partial_update:
    Partially update a job posting (Admin/Owner only).
    
    destroy:
    Delete a job posting (Admin/Owner only).
    """
    
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    
    @swagger_auto_schema(
        operation_description="Get list of jobs with filtering options",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by category ID",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'location',
                openapi.IN_QUERY,
                description="Filter by location (partial match)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'job_type',
                openapi.IN_QUERY,
                description="Filter by job type",
                type=openapi.TYPE_STRING,
                enum=['full-time', 'part-time', 'contract', 'remote']
            ),
        ],
        responses={
            200: JobSerializer(many=True),
            400: "Bad Request"
        }
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
```

### 2. Documenting Serializers

Add help text to serializer fields:

```python
from rest_framework import serializers

class JobSerializer(serializers.ModelSerializer):
    """Serializer for Job model with all fields."""
    
    category_name = serializers.CharField(
        source='category.name',
        read_only=True,
        help_text="Name of the job category"
    )
    
    posted_by_email = serializers.EmailField(
        source='posted_by.email',
        read_only=True,
        help_text="Email of the user who posted the job"
    )
    
    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category', 'category_name',
            'location', 'job_type', 'salary_min', 'salary_max', 'currency',
            'posted_by', 'posted_by_email', 'status', 'deadline',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'posted_by', 'created_at', 'updated_at']
```

### 3. Custom Actions

Document custom actions with `@swagger_auto_schema`:

```python
from rest_framework.decorators import action
from rest_framework.response import Response

class JobViewSet(viewsets.ModelViewSet):
    # ... other methods
    
    @swagger_auto_schema(
        method='get',
        operation_description="Get all applications for this job",
        responses={
            200: ApplicationSerializer(many=True),
            403: "Permission denied - Admin/Owner only",
            404: "Job not found"
        }
    )
    @action(detail=True, methods=['get'])
    def applications(self, request, pk=None):
        """Get all applications for a specific job."""
        job = self.get_object()
        applications = job.applications.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data)
```

---

## 🔐 Authentication in Swagger

### JWT Authentication Setup

Configure JWT authentication in Swagger:

```python
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        # ... other info
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    authentication_classes=[],  # Disable authentication for schema view
)
```

### Using Authentication in Swagger UI

1. Navigate to Swagger UI (`/api/docs/`)
2. Click the "Authorize" button (top right)
3. Enter your JWT token in the format: `Bearer <your-token>`
4. Click "Authorize"
5. All subsequent requests will include the token

### Obtaining a JWT Token

1. Use the `/api/auth/login/` endpoint
2. Provide username/email and password
3. Copy the `access` token from the response
4. Use this token in the Authorize dialog

---

## 📱 Postman Collection

### Importing the Collection

1. Open Postman
2. Click "Import" button
3. Select `docs/postman/Job_Board_API.postman_collection.json`
4. Import the environment file: `docs/postman/Job_Board_API.postman_environment.json`

### Environment Variables

The Postman collection uses the following variables:

- `base_url`: API base URL (e.g., `http://localhost:8000`)
- `access_token`: JWT access token (auto-populated after login)
- `refresh_token`: JWT refresh token (auto-populated after login)
- `user_id`: Current user ID
- `job_id`: Sample job ID for testing
- `category_id`: Sample category ID for testing

### Authentication Flow in Postman

The collection includes pre-request and test scripts that automatically:

1. Store tokens after login
2. Refresh tokens when expired
3. Include tokens in protected requests

**Login Request Example:**

```javascript
// Test script in Login request
if (pm.response.code === 200) {
    var jsonData = pm.response.json();
    pm.environment.set("access_token", jsonData.access);
    pm.environment.set("refresh_token", jsonData.refresh);
}
```

**Protected Request Example:**

```javascript
// Pre-request script
pm.request.headers.add({
    key: 'Authorization',
    value: 'Bearer ' + pm.environment.get('access_token')
});
```

---

## 🌐 CORS Configuration

For frontend integration, configure CORS in `config/settings/base.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    # ... other middleware
]

# CORS settings
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]
```

---

## 📊 API Response Examples

### Success Response (List)

```json
{
  "count": 25,
  "next": "http://localhost:8000/api/jobs/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "title": "Senior Backend Developer",
      "description": "We are seeking an experienced backend developer...",
      "category": 2,
      "category_name": "Software Development",
      "location": "Remote",
      "job_type": "full-time",
      "salary_min": "80000.00",
      "salary_max": "120000.00",
      "currency": "USD",
      "posted_by": 5,
      "posted_by_email": "employer@example.com",
      "status": "active",
      "deadline": "2024-03-31T23:59:59Z",
      "created_at": "2024-01-15T10:30:00Z",
      "updated_at": "2024-01-15T10:30:00Z"
    }
  ]
}
```

### Success Response (Detail)

```json
{
  "id": 1,
  "title": "Senior Backend Developer",
  "description": "We are seeking an experienced backend developer...",
  "category": 2,
  "category_name": "Software Development",
  "location": "Remote",
  "job_type": "full-time",
  "salary_min": "80000.00",
  "salary_max": "120000.00",
  "currency": "USD",
  "posted_by": 5,
  "posted_by_email": "employer@example.com",
  "status": "active",
  "deadline": "2024-03-31T23:59:59Z",
  "created_at": "2024-01-15T10:30:00Z",
  "updated_at": "2024-01-15T10:30:00Z"
}
```

### Error Response (Validation)

```json
{
  "error": "ValidationError",
  "message": "Invalid input data",
  "details": {
    "title": ["This field is required."],
    "category": ["Invalid pk '999' - object does not exist."],
    "salary_min": ["Ensure this value is greater than or equal to 0."]
  }
}
```

### Error Response (Authentication)

```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Error Response (Permission)

```json
{
  "detail": "You do not have permission to perform this action."
}
```

---

## 🔍 Query Parameters

### Filtering

```
GET /api/jobs/?category=2&location=Remote&job_type=full-time
```

### Searching

```
GET /api/jobs/?search=python developer
```

### Ordering

```
GET /api/jobs/?ordering=-created_at
GET /api/jobs/?ordering=salary_min,title
```

### Pagination

```
GET /api/jobs/?page=2&page_size=20
```

### Combined Filters

```
GET /api/jobs/?category=2&location=Remote&ordering=-salary_max&page=1&page_size=10
```

---

## 🛠️ Testing the API

### Using cURL

**Register a User:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepass123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "securepass123"
  }'
```

**Get Jobs (with token):**
```bash
curl -X GET http://localhost:8000/api/jobs/ \
  -H "Authorization: Bearer <your-access-token>"
```

### Using HTTPie

**Register a User:**
```bash
http POST localhost:8000/api/auth/register/ \
  username=testuser \
  email=test@example.com \
  password=securepass123 \
  first_name=Test \
  last_name=User
```

**Login:**
```bash
http POST localhost:8000/api/auth/login/ \
  email=test@example.com \
  password=securepass123
```

**Get Jobs (with token):**
```bash
http GET localhost:8000/api/jobs/ \
  "Authorization: Bearer <your-access-token>"
```

---

## 📖 Additional Resources

- [Django REST Framework Documentation](https://www.django-rest-framework.org/)
- [drf-yasg Documentation](https://drf-yasg.readthedocs.io/)
- [OpenAPI Specification](https://swagger.io/specification/)
- [JWT Authentication Guide](https://django-rest-framework-simplejwt.readthedocs.io/)

---

This documentation provides a comprehensive guide for using and integrating with the Job Board Backend API.
