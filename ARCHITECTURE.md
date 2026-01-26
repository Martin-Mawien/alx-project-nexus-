# Job Board Backend - System Architecture

## Database Schema

```
┌─────────────────────────────────────────────────────────────────┐
│                           User Model                             │
│  (Custom User with Role-based Authentication)                   │
├─────────────────────────────────────────────────────────────────┤
│ - id (PK)                                                        │
│ - username (Unique)                                              │
│ - email                                                          │
│ - role (ADMIN, EMPLOYER, JOB_SEEKER)                            │
│ - company_name                                                   │
│ - phone_number                                                   │
│ - bio                                                            │
│ - created_at                                                     │
│ - updated_at                                                     │
└─────────────────────────────────────────────────────────────────┘
         │                                    │
         │ (employer)                         │ (applicant)
         │                                    │
         ▼                                    ▼
┌──────────────────────┐            ┌──────────────────────┐
│   Category Model     │            │  Application Model   │
├──────────────────────┤            ├──────────────────────┤
│ - id (PK)            │            │ - id (PK)            │
│ - name               │            │ - job (FK → Job)     │
│ - slug (Unique)      │            │ - applicant (FK)     │
│ - description        │            │ - cover_letter       │
│ - created_at         │            │ - resume_url         │
│ - updated_at         │            │ - status             │
└──────────────────────┘            │ - notes              │
         │                          │ - created_at         │
         │ (category)               │ - updated_at         │
         ▼                          └──────────────────────┘
┌──────────────────────┐                     ▲
│     Job Model        │                     │
├──────────────────────┤                     │
│ - id (PK)            │─────────────────────┘
│ - title              │
│ - slug (Unique)      │
│ - description        │
│ - requirements       │
│ - responsibilities   │
│ - category (FK)      │
│ - employer (FK)      │
│ - job_type           │
│ - experience_level   │
│ - location           │
│ - is_remote          │
│ - salary_min         │
│ - salary_max         │
│ - salary_currency    │
│ - is_active          │
│ - deadline           │
│ - created_at         │
│ - updated_at         │
└──────────────────────┘
```

## API Endpoints Structure

```
/api/
├── auth/
│   └── users/
│       ├── register/         [POST]   - Register new user
│       ├── login/            [POST]   - Login and get token
│       ├── logout/           [POST]   - Logout (authenticated)
│       ├── me/               [GET]    - Get current user profile
│       ├── {id}/             [GET]    - Get user details
│       ├── {id}/             [PUT]    - Update user
│       └── {id}/             [DELETE] - Delete user
│
├── categories/
│   ├── /                     [GET]    - List all categories
│   ├── /                     [POST]   - Create category
│   ├── {slug}/               [GET]    - Get category details
│   ├── {slug}/               [PUT]    - Update category
│   ├── {slug}/               [DELETE] - Delete category
│   └── {slug}/jobs/          [GET]    - Get jobs in category
│
├── jobs/
│   ├── /                     [GET]    - List all jobs (with filters)
│   ├── /                     [POST]   - Create job (employer only)
│   ├── {slug}/               [GET]    - Get job details
│   ├── {slug}/               [PUT]    - Update job (owner only)
│   ├── {slug}/               [DELETE] - Delete job (owner only)
│   └── {slug}/applications/  [GET]    - Get job applications (owner only)
│
├── applications/
│   ├── /                     [GET]    - List applications (role-filtered)
│   ├── /                     [POST]   - Submit application (job seeker only)
│   ├── {id}/                 [GET]    - Get application details
│   ├── {id}/                 [PUT]    - Update application
│   └── {id}/update_status/   [PATCH]  - Update status (employer only)
│
├── docs/                     [GET]    - Swagger UI documentation
├── redoc/                    [GET]    - ReDoc documentation
└── schema/                   [GET]    - OpenAPI schema (JSON/YAML)
```

## Role-Based Access Control

```
┌─────────────┬────────────────┬─────────────────┬───────────────┐
│   Role      │   Categories   │      Jobs       │  Applications │
├─────────────┼────────────────┼─────────────────┼───────────────┤
│ ADMIN       │ Full CRUD      │ Full CRUD       │ Full CRUD     │
│             │                │                 │               │
│ EMPLOYER    │ Read           │ CRUD (own jobs) │ Read (own)    │
│             │                │ Read (all)      │ Update status │
│             │                │                 │               │
│ JOB_SEEKER  │ Read           │ Read (all)      │ CRUD (own)    │
│             │                │                 │ Submit new    │
│             │                │                 │               │
│ Anonymous   │ Read           │ Read (all)      │ None          │
└─────────────┴────────────────┴─────────────────┴───────────────┘
```

## Request/Response Flow

```
┌──────────┐                ┌──────────────┐                ┌──────────┐
│  Client  │                │  Django REST │                │ Database │
│          │                │  Framework   │                │          │
└────┬─────┘                └──────┬───────┘                └────┬─────┘
     │                             │                             │
     │  1. HTTP Request            │                             │
     │  (with Token Auth)          │                             │
     ├────────────────────────────>│                             │
     │                             │                             │
     │                             │  2. Authenticate            │
     │                             │     & Authorize             │
     │                             │                             │
     │                             │  3. Query Database          │
     │                             │     (Optimized)             │
     │                             ├────────────────────────────>│
     │                             │                             │
     │                             │  4. Return Data             │
     │                             │<────────────────────────────┤
     │                             │                             │
     │                             │  5. Serialize               │
     │                             │     Response                │
     │                             │                             │
     │  6. JSON Response           │                             │
     │<────────────────────────────┤                             │
     │                             │                             │
```

## Query Optimization Techniques

```
Jobs List View:
┌─────────────────────────────────────────────────────────┐
│ Job.objects                                             │
│   .select_related('employer', 'category')   ← JOIN     │
│   .prefetch_related('applications')         ← Separate │
│   .annotate(_applications_count=Count(...)) ← Aggregate│
│   .filter(is_active=True)                              │
│   .order_by('-created_at')                             │
└─────────────────────────────────────────────────────────┘

Result: 1 main query + 1 prefetch query instead of N+1 queries
```

## Authentication Flow

```
Registration:
POST /api/auth/users/register/
  ↓
  Validate data
  ↓
  Create user with hashed password
  ↓
  Generate auth token
  ↓
  Return user + token

Login:
POST /api/auth/users/login/
  ↓
  Authenticate credentials
  ↓
  Get or create token
  ↓
  Return user + token

Authenticated Request:
Header: Authorization: Token <token>
  ↓
  Validate token
  ↓
  Attach user to request
  ↓
  Check permissions
  ↓
  Process request
```

## Technology Stack

```
┌────────────────────────────────────────────────────┐
│                  Application Layer                 │
├────────────────────────────────────────────────────┤
│  Django 5.0.1 + Django REST Framework 3.14.0       │
│  - Token Authentication                            │
│  - ViewSets & Routers                             │
│  - Serializers                                     │
│  - Permissions                                     │
├────────────────────────────────────────────────────┤
│                Documentation Layer                 │
├────────────────────────────────────────────────────┤
│  drf-spectacular 0.27.1                           │
│  - OpenAPI 3.0 Schema                             │
│  - Swagger UI                                      │
│  - ReDoc                                          │
├────────────────────────────────────────────────────┤
│                 Database Layer                     │
├────────────────────────────────────────────────────┤
│  PostgreSQL 12+ (Production)                      │
│  SQLite 3 (Development)                           │
│  - Indexed queries                                │
│  - Foreign key constraints                        │
├────────────────────────────────────────────────────┤
│              Additional Features                   │
├────────────────────────────────────────────────────┤
│  django-filter 23.5  - Filtering                  │
│  python-decouple 3.8 - Environment config         │
└────────────────────────────────────────────────────┘
```
