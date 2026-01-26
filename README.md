### alx-project-nexus-
Job Board Backend   A production‑ready backend system for managing job postings, categories, and applications. Built with Django REST Framework and PostgreSQL, it features role‑based authentication, optimized queries, and Swagger/OpenAPI documentation.
----

## 🚀 Objectives
  - Apply backend technologies to a real world project.
  - Design scalable and efficient backend solutions.
  - Demonstrate problem solving in databae and API design
  - Improve collabrotion, documentation, and presentation skills.
----

## 🛠️ Technologies
  - Django + Django Rest framewoork
  - PostgreSQL
  - JWT Authentication
  - Docker
  - Swagger/OpenAPI
  - Github Actions (CI/CD)
  - Render (Deployment)

----

📊 Database Schema (ERD)
erDiagram
    
    USER {
        int id PK
        string name
        string email
        string password
        string role_id FK

    }
    Role {
        int id PK
        string name
    }

    JOB { 
        int id PK
        string title
        string description
        int category_id FK
        string location
        string type
        int posted_by FK
        datetime created_at
        
     }

    CATEGORY {
        int id PK
        string name
        string description

    }

    APPLICATIPON {
        int id PK
        int job_id FK
        int user_id FK
        string resume_link
        string status
        datetime applied_at

    }
    
      USER ||--o{ APPLICATION : "applies"
      JOB ||--o{ APPLICATION : "has"
      CATEGORY ||--o{ JOB : "categorizes"
      ROLE ||--o{ USER : "assigns"
      USER ||--o{ JOB : "posts"

----

📂 API Endpoints
Auth
POST /auth/register → Register user

POST /auth/login → Authenticate & return JWT

Jobs
GET /jobs → List jobs with filters

POST /jobs → Create job (Admin only)

GET /jobs/{id} → Retrieve job details

PUT /jobs/{id} → Update job (Admin only)

DELETE /jobs/{id} → Delete job (Admin only)

Categories
GET /categories → List categories

POST /categories → Create category (Admin only)

GET /categories/{id} → Retrieve category

PUT /categories/{id} → Update category (Admin only)

DELETE /categories/{id} → Delete category (Admin only)

Applications
GET /applications → List applications (Admin only)

POST /applications → Apply for job (User only)

GET /applications/{id} → Retrieve application

PUT /applications/{id} → Update status (Admin only)

DELETE /applications/{id} → Withdraw application (User only)

# Clone repo
git clone https://github.com/your-username/job-board-backend.git
cd job-board-backend

# Setup environment
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start server
python manage.py runserver

----

pytest --disable-warnings --maxfail=1 --cov=.

----

🚀 Deployment
Dockerized app deployed on Render.

CI/CD pipeline via GitHub Actions.

Secrets managed securely (RENDER_API_KEY, RENDER_SERVICE_ID).

📖 Documentation
Swagger/OpenAPI at /api/docs.

README includes ERD diagram + setup guide.

🤝 Contribution Guidelines
Follow Git commit conventions (feat:, fix:, perf:, docs:).

Use pull requests for new features.

Ensure tests pass before merging.

✅ Evaluation Criteria
Functionality: CRUD + role‑based access.

Code Quality: Modular, Django best practices.

Performance: Indexed queries, efficient search.

Documentation: Swagger + README + ERD.

Deployment: CI/CD pipeline with Render.

✨ Features
  - Job Management: CRUD APIs for job postings with category and location filters.
  - Role Base Access: Admins manage jobs/categories; users apply for jobs.
  - Optimized search: Indexed queries for fast filtering.
  - Applications: users apply, admins review/update status.
  - API Docs: Swagger hosted at /api/docs.
----

