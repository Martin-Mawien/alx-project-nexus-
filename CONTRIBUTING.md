# Contributing to Job Board Backend API

Thank you for your interest in contributing to the Job Board Backend API! This document provides guidelines and instructions for contributing to this project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive experience for everyone. We expect all contributors to:

- Use welcoming and inclusive language
- Be respectful of differing viewpoints and experiences
- Gracefully accept constructive criticism
- Focus on what is best for the community
- Show empathy towards other community members

### Unacceptable Behavior

- Harassment, discriminatory comments, or personal attacks
- Trolling, insulting/derogatory comments, and public or private harassment
- Publishing others' private information without permission
- Other conduct that could reasonably be considered inappropriate

---

## Getting Started

### Prerequisites

Before contributing, ensure you have:

- Python 3.10 or higher
- PostgreSQL 14 or higher
- Git
- A GitHub account
- Basic knowledge of Django and Django REST Framework

### Setting Up Your Development Environment

1. **Fork the Repository**
   
   Click the "Fork" button at the top right of the repository page.

2. **Clone Your Fork**

   ```bash
   git clone https://github.com/YOUR-USERNAME/alx-project-nexus-.git
   cd alx-project-nexus-
   ```

3. **Add Upstream Remote**

   ```bash
   git remote add upstream https://github.com/Martin-Mawien/alx-project-nexus-.git
   ```

4. **Create Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

5. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt
   ```

6. **Set Up Database**

   ```bash
   createdb jobboard_dev
   cp .env.example .env
   # Edit .env with your database credentials
   python manage.py migrate
   ```

7. **Run Tests**

   ```bash
   pytest
   ```

---

## How to Contribute

### Types of Contributions

We welcome various types of contributions:

- **Bug Reports**: Found a bug? Let us know!
- **Feature Requests**: Have an idea? Share it with us!
- **Code Contributions**: Fix bugs or implement features
- **Documentation**: Improve or add documentation
- **Tests**: Add or improve test coverage
- **Performance**: Optimize existing code

### Reporting Bugs

Before creating a bug report:

1. Check if the bug has already been reported in [Issues](https://github.com/Martin-Mawien/alx-project-nexus-/issues)
2. Ensure you're using the latest version
3. Verify the bug is reproducible

When creating a bug report, include:

- **Clear Title**: Descriptive summary of the issue
- **Description**: Detailed explanation of the problem
- **Steps to Reproduce**: Step-by-step instructions
- **Expected Behavior**: What you expected to happen
- **Actual Behavior**: What actually happened
- **Environment**: Python version, OS, database version
- **Error Messages**: Full stack traces or error logs
- **Screenshots**: If applicable

**Bug Report Template:**

```markdown
## Bug Description
A clear and concise description of the bug.

## Steps to Reproduce
1. Go to '...'
2. Click on '...'
3. Scroll down to '...'
4. See error

## Expected Behavior
What you expected to happen.

## Actual Behavior
What actually happened.

## Environment
- Python Version: 3.10
- Django Version: 4.2
- PostgreSQL Version: 14
- OS: Ubuntu 22.04

## Error Messages
```
Paste error messages or stack traces here
```

## Additional Context
Any other relevant information.
```

### Requesting Features

When requesting a feature:

1. Check existing feature requests
2. Provide a clear use case
3. Explain why this feature would be valuable
4. Consider backward compatibility

**Feature Request Template:**

```markdown
## Feature Description
A clear description of the feature you'd like to see.

## Problem It Solves
Describe the problem this feature addresses.

## Proposed Solution
How you envision this feature working.

## Alternatives Considered
Other solutions you've thought about.

## Additional Context
Any other relevant information, mockups, or examples.
```

---

## Development Workflow

### Branching Strategy

We follow a simplified Git Flow:

- `main` - Production-ready code
- `develop` - Development branch
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates
- `refactor/*` - Code refactoring
- `perf/*` - Performance improvements

### Creating a Feature Branch

```bash
# Update your local main branch
git checkout main
git pull upstream main

# Create a new feature branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/bug-description
```

### Making Changes

1. **Write Code**
   - Follow our [coding standards](#coding-standards)
   - Keep changes focused and atomic
   - Write self-documenting code

2. **Write Tests**
   - Add unit tests for new functions
   - Add integration tests for API endpoints
   - Maintain or improve code coverage

3. **Update Documentation**
   - Update docstrings
   - Update README if needed
   - Add API documentation

4. **Commit Changes**
   - Follow our [commit guidelines](#commit-guidelines)
   - Make small, logical commits
   - Write meaningful commit messages

---

## Coding Standards

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length**: 88 characters (Black default)
- **Indentation**: 4 spaces
- **Quotes**: Double quotes for strings
- **Imports**: Organized with isort

### Code Formatting Tools

We use the following tools (configured in `pyproject.toml`):

- **Black**: Code formatter
- **isort**: Import sorter
- **flake8**: Linter
- **mypy**: Static type checker

### Running Code Quality Tools

```bash
# Format code with Black
black apps/

# Sort imports
isort apps/

# Check with flake8
flake8 apps/

# Type checking with mypy
mypy apps/

# Or run all at once
make lint  # if Makefile is available
```

### Django Best Practices

- **Models**
  - Use descriptive model names (singular)
  - Add `__str__` methods
  - Use `Meta` class for ordering and indexes
  - Add field validators where appropriate
  - Use database constraints

- **Views**
  - Use class-based views (ViewSets for APIs)
  - Keep views thin, move logic to services or models
  - Use appropriate permissions
  - Handle exceptions gracefully

- **Serializers**
  - Use `ModelSerializer` when possible
  - Validate data in serializer methods
  - Use `read_only_fields` appropriately
  - Add custom validation methods

- **URLs**
  - Use descriptive URL patterns
  - Use routers for ViewSets
  - Group related URLs

### Code Organization

```python
# Standard library imports
import os
from typing import List, Optional

# Third-party imports
from django.db import models
from rest_framework import serializers

# Local application imports
from apps.users.models import User
from apps.categories.models import Category
```

### Naming Conventions

- **Variables**: `snake_case`
- **Functions**: `snake_case`
- **Classes**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Database tables**: `plural_snake_case`

### Documentation

- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Use type hints for function parameters and return values
- **Comments**: Explain why, not what

**Example:**

```python
def calculate_salary_range(
    min_salary: float,
    max_salary: float,
    currency: str = "USD"
) -> dict[str, float]:
    """Calculate salary range statistics.
    
    Args:
        min_salary: Minimum salary value
        max_salary: Maximum salary value
        currency: Currency code (default: USD)
    
    Returns:
        Dictionary containing min, max, and average salary
    
    Raises:
        ValueError: If min_salary is greater than max_salary
    """
    if min_salary > max_salary:
        raise ValueError("Minimum salary cannot exceed maximum salary")
    
    return {
        "min": min_salary,
        "max": max_salary,
        "avg": (min_salary + max_salary) / 2,
        "currency": currency
    }
```

---

## Commit Guidelines

### Commit Message Format

We follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, semicolons, etc.)
- `refactor`: Code refactoring (no functional changes)
- `perf`: Performance improvements
- `test`: Adding or updating tests
- `chore`: Maintenance tasks
- `ci`: CI/CD changes
- `build`: Build system changes

### Scope

Optional, but recommended. Examples:
- `users`: Changes to users app
- `jobs`: Changes to jobs app
- `api`: API-related changes
- `auth`: Authentication changes
- `db`: Database changes

### Subject

- Use imperative mood ("add" not "added")
- Don't capitalize first letter
- No period at the end
- Maximum 50 characters

### Body

- Explain what and why (not how)
- Wrap at 72 characters
- Separate from subject with blank line

### Footer

- Reference issues: `Fixes #123`, `Closes #456`
- Breaking changes: `BREAKING CHANGE: description`

### Examples

**Good commit messages:**

```
feat(jobs): add salary range filtering

Add ability to filter jobs by minimum and maximum salary.
Implements database indexes for optimal query performance.

Closes #42
```

```
fix(auth): resolve JWT token expiration issue

Fix bug where refresh tokens were expiring too early due to
incorrect timedelta calculation in settings.

Fixes #89
```

```
docs(api): update authentication endpoint documentation

Add examples for all auth endpoints and clarify error responses.
```

**Bad commit messages:**

```
fix stuff
```

```
WIP
```

```
Fixed a bug
```

---

## Pull Request Process

### Before Submitting

1. **Update Your Branch**

   ```bash
   git checkout main
   git pull upstream main
   git checkout your-feature-branch
   git rebase main
   ```

2. **Run Tests**

   ```bash
   pytest --cov=apps
   ```

3. **Check Code Quality**

   ```bash
   black apps/ --check
   isort apps/ --check-only
   flake8 apps/
   ```

4. **Update Documentation**
   - Update README if needed
   - Update API documentation
   - Add docstrings to new functions

### Submitting Pull Request

1. **Push Your Branch**

   ```bash
   git push origin your-feature-branch
   ```

2. **Create Pull Request**
   - Go to your fork on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill in the PR template

3. **PR Title**
   - Use same format as commit messages
   - `feat: add job filtering by location`

4. **PR Description**

Include:
- **What**: What changes are included
- **Why**: Why these changes are needed
- **How**: How you implemented the changes
- **Testing**: How you tested the changes
- **Screenshots**: If UI changes (for frontend)
- **Breaking Changes**: Any breaking changes
- **Related Issues**: References to related issues

**PR Template:**

```markdown
## Description
Brief description of changes.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update

## How Has This Been Tested?
- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing

## Checklist
- [ ] My code follows the style guidelines of this project
- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Related Issues
Fixes #(issue number)

## Screenshots (if applicable)
Add screenshots here.
```

### Review Process

1. **Automated Checks**
   - CI/CD pipeline runs tests
   - Code coverage is checked
   - Linting is verified

2. **Code Review**
   - At least one maintainer will review
   - Address all review comments
   - Make requested changes

3. **Approval and Merge**
   - Once approved, a maintainer will merge
   - Your PR will be squashed and merged
   - Your branch will be deleted

---

## Testing Guidelines

### Test Structure

```
tests/
├── conftest.py              # Pytest configuration and fixtures
├── factories.py             # Model factories
├── unit/
│   ├── test_models.py
│   ├── test_serializers.py
│   └── test_utils.py
└── integration/
    ├── test_auth_api.py
    ├── test_jobs_api.py
    └── test_applications_api.py
```

### Writing Tests

**Unit Tests:**

```python
import pytest
from apps.jobs.models import Job

@pytest.mark.django_db
class TestJobModel:
    def test_job_str_representation(self, job_factory):
        """Test string representation of Job model."""
        job = job_factory(title="Senior Developer")
        assert str(job) == "Senior Developer"
    
    def test_job_is_active_by_default(self, job_factory):
        """New jobs should be active by default."""
        job = job_factory()
        assert job.status == "active"
```

**Integration Tests:**

```python
import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
class TestJobAPI:
    def test_create_job_as_admin(self, admin_user, category_factory):
        """Admins can create job postings."""
        client = APIClient()
        client.force_authenticate(user=admin_user)
        category = category_factory()
        
        response = client.post('/api/jobs/', {
            'title': 'Software Engineer',
            'description': 'We are hiring...',
            'category': category.id,
            'location': 'Remote',
            'job_type': 'full-time'
        })
        
        assert response.status_code == 201
        assert response.data['title'] == 'Software Engineer'
```

### Test Coverage

- Aim for **95%+ code coverage**
- Cover edge cases and error scenarios
- Test authentication and permissions
- Test data validation

### Running Tests

```bash
# Run all tests
pytest

# Run specific test file
pytest apps/jobs/tests.py

# Run with coverage
pytest --cov=apps --cov-report=html

# Run tests in parallel
pytest -n auto

# Run only failed tests
pytest --lf
```

---

## Documentation

### Code Documentation

- Add docstrings to all classes and functions
- Use type hints
- Keep comments up to date

### API Documentation

- Document all endpoints in Swagger/OpenAPI
- Include request/response examples
- Document query parameters and filters

### README Updates

Update README when:
- Adding new features
- Changing setup instructions
- Updating dependencies
- Modifying API endpoints

---

## Community

### Getting Help

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions and general discussion
- **Stack Overflow**: Tag with `django` and `job-board-api`

### Recognition

Contributors will be recognized in:
- GitHub contributors page
- Release notes for significant contributions
- Special acknowledgment for major features

---

## License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to Job Board Backend API! 🎉
