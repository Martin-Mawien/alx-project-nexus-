from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model with role-based authentication.
    """
    class Role(models.TextChoices):
        EMPLOYER = 'EMPLOYER', 'Employer'
        JOB_SEEKER = 'JOB_SEEKER', 'Job Seeker'
        ADMIN = 'ADMIN', 'Admin'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.JOB_SEEKER,
        help_text='User role for access control'
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Company name for employers'
    )
    phone_number = models.CharField(
        max_length=20,
        blank=True,
        null=True
    )
    bio = models.TextField(
        blank=True,
        null=True,
        help_text='User biography or description'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_employer(self):
        return self.role == self.Role.EMPLOYER

    @property
    def is_job_seeker(self):
        return self.role == self.Role.JOB_SEEKER

    @property
    def is_admin_user(self):
        return self.role == self.Role.ADMIN or self.is_superuser

