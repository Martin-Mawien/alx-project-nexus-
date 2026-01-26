## Description

<!-- Provide a brief description of the changes in this PR -->

## Type of Change

Please delete options that are not relevant:

- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Test updates
- [ ] CI/CD updates
- [ ] Dependency updates

## Related Issues

<!-- Link to related issues using #issue_number -->

Fixes #(issue)
Closes #(issue)
Related to #(issue)

## Changes Made

<!-- Provide a detailed list of changes -->

- Change 1
- Change 2
- Change 3

## API Changes (if applicable)

### New Endpoints

- `GET /api/new-endpoint/` - Description
- `POST /api/new-endpoint/` - Description

### Modified Endpoints

- `GET /api/jobs/` - Added new query parameter `filter_by`

### Deprecated/Removed Endpoints

- `DELETE /api/old-endpoint/` - Deprecated, use `/api/new-endpoint/` instead

## Database Changes (if applicable)

- [ ] New migrations added
- [ ] Migrations tested locally
- [ ] Data migration required
- [ ] No database changes

**Migration commands:**
```bash
python manage.py makemigrations
python manage.py migrate
```

## How Has This Been Tested?

<!-- Describe the tests you ran to verify your changes -->

- [ ] Unit tests
- [ ] Integration tests
- [ ] Manual testing
- [ ] Test coverage increased/maintained

**Test Configuration:**
- Python version: 3.10
- Django version: 4.2
- Database: PostgreSQL 14

**Test commands:**
```bash
pytest apps/specific_app/tests.py -v
pytest --cov=apps --cov-report=term
```

## Screenshots (if applicable)

<!-- Add screenshots for UI changes or API responses -->

**Before:**
<!-- Screenshot before changes -->

**After:**
<!-- Screenshot after changes -->

## API Response Examples (if applicable)

**Request:**
```http
GET /api/jobs/?filter_by=active HTTP/1.1
Authorization: Bearer <token>
```

**Response:**
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "title": "Backend Developer"
    }
  ]
}
```

## Checklist

### Code Quality

- [ ] My code follows the style guidelines of this project (PEP 8)
- [ ] Code is formatted with Black
- [ ] Imports are sorted with isort
- [ ] Linting passes with flake8
- [ ] Type hints added where applicable
- [ ] No new warnings introduced

### Testing

- [ ] I have performed a self-review of my own code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Test coverage is maintained or improved

### Documentation

- [ ] I have made corresponding changes to the documentation
- [ ] Updated README.md if needed
- [ ] Updated API documentation
- [ ] Added docstrings to new functions/classes
- [ ] Updated CHANGELOG.md

### Security

- [ ] No sensitive data exposed
- [ ] No new security vulnerabilities introduced
- [ ] Authentication/authorization properly implemented
- [ ] Input validation added
- [ ] SQL injection prevention verified

### Performance

- [ ] Database queries optimized
- [ ] No N+1 query problems introduced
- [ ] Appropriate indexes added
- [ ] Caching implemented where beneficial

### Deployment

- [ ] Environment variables documented in .env.example
- [ ] Database migrations are reversible
- [ ] No breaking changes to existing API (or documented)
- [ ] Ready for production deployment

## Breaking Changes

<!-- If this PR introduces breaking changes, describe them and migration path -->

**Changes:**
- Change 1: Description and migration steps

**Migration Guide:**
```bash
# Step 1: Update dependencies
pip install -r requirements.txt

# Step 2: Run migrations
python manage.py migrate

# Step 3: Update API calls
# OLD: GET /api/v1/jobs
# NEW: GET /api/v2/jobs
```

## Dependencies

<!-- List any new dependencies or dependency updates -->

- Added: `package-name==version` - Reason
- Updated: `package-name` from `old-version` to `new-version` - Reason
- Removed: `package-name` - Reason

## Rollback Plan

<!-- Describe how to rollback this change if issues occur in production -->

1. Revert the merge commit: `git revert -m 1 <commit-hash>`
2. Run reverse migrations: `python manage.py migrate app_name <previous_migration>`
3. Redeploy previous version

## Additional Notes

<!-- Any additional information that reviewers should know -->

## Post-Merge Tasks

<!-- Tasks to be completed after merging -->

- [ ] Update production environment variables
- [ ] Run database migrations in production
- [ ] Monitor error logs for 24 hours
- [ ] Update external documentation
- [ ] Notify team of changes

---

**By submitting this pull request, I confirm that my contribution is made under the terms of the MIT License.**
