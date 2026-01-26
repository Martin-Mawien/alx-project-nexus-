from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Category(models.Model):
    """
    Job category model for organizing job postings.
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Category name'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text='URL-friendly version of the name'
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text='Category description'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Job posting model with comprehensive job details.
    """
    class JobType(models.TextChoices):
        FULL_TIME = 'FULL_TIME', 'Full Time'
        PART_TIME = 'PART_TIME', 'Part Time'
        CONTRACT = 'CONTRACT', 'Contract'
        INTERNSHIP = 'INTERNSHIP', 'Internship'
        TEMPORARY = 'TEMPORARY', 'Temporary'

    class ExperienceLevel(models.TextChoices):
        ENTRY = 'ENTRY', 'Entry Level'
        INTERMEDIATE = 'INTERMEDIATE', 'Intermediate'
        SENIOR = 'SENIOR', 'Senior'
        EXECUTIVE = 'EXECUTIVE', 'Executive'

    title = models.CharField(
        max_length=255,
        help_text='Job title'
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text='URL-friendly version of the title'
    )
    description = models.TextField(
        help_text='Detailed job description'
    )
    requirements = models.TextField(
        help_text='Job requirements and qualifications'
    )
    responsibilities = models.TextField(
        blank=True,
        null=True,
        help_text='Job responsibilities'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='jobs',
        help_text='Job category'
    )
    employer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posted_jobs',
        limit_choices_to={'role': 'EMPLOYER'},
        help_text='Employer who posted the job'
    )
    job_type = models.CharField(
        max_length=20,
        choices=JobType.choices,
        default=JobType.FULL_TIME,
        help_text='Type of employment'
    )
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ENTRY,
        help_text='Required experience level'
    )
    location = models.CharField(
        max_length=255,
        help_text='Job location'
    )
    is_remote = models.BooleanField(
        default=False,
        help_text='Whether the job is remote'
    )
    salary_min = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Minimum salary'
    )
    salary_max = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
        help_text='Maximum salary'
    )
    salary_currency = models.CharField(
        max_length=3,
        default='USD',
        help_text='Salary currency code (e.g., USD, EUR)'
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Whether the job posting is active'
    )
    deadline = models.DateTimeField(
        blank=True,
        null=True,
        help_text='Application deadline'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Job'
        verbose_name_plural = 'Jobs'
        indexes = [
            models.Index(fields=['category', '-created_at']),
            models.Index(fields=['employer', '-created_at']),
            models.Index(fields=['is_active', '-created_at']),
        ]

    def __str__(self):
        return f"{self.title} - {self.employer.company_name or self.employer.username}"

    @property
    def applications_count(self):
        if hasattr(self, '_applications_count'):
            return self._applications_count
        return self.applications.count()


class Application(models.Model):
    """
    Job application model linking job seekers to jobs.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        REVIEWING = 'REVIEWING', 'Reviewing'
        SHORTLISTED = 'SHORTLISTED', 'Shortlisted'
        REJECTED = 'REJECTED', 'Rejected'
        ACCEPTED = 'ACCEPTED', 'Accepted'

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications',
        help_text='Job being applied to'
    )
    applicant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='applications',
        limit_choices_to={'role': 'JOB_SEEKER'},
        help_text='Job seeker applying for the job'
    )
    cover_letter = models.TextField(
        help_text='Cover letter from the applicant'
    )
    resume_url = models.URLField(
        blank=True,
        null=True,
        help_text='URL to applicant resume'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        help_text='Application status'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        help_text='Internal notes from employer'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Application'
        verbose_name_plural = 'Applications'
        unique_together = ['job', 'applicant']
        indexes = [
            models.Index(fields=['job', '-created_at']),
            models.Index(fields=['applicant', '-created_at']),
            models.Index(fields=['status', '-created_at']),
        ]

    def __str__(self):
        return f"{self.applicant.username} - {self.job.title} ({self.get_status_display()})"

