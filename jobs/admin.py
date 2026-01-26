from django.contrib import admin
from .models import Category, Job, Application


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for Category model.
    """
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    """
    Admin configuration for Job model.
    """
    list_display = ['title', 'category', 'employer', 'job_type', 'location', 'is_active', 'created_at']
    list_filter = ['job_type', 'experience_level', 'is_active', 'is_remote', 'category', 'created_at']
    search_fields = ['title', 'description', 'location', 'employer__username', 'employer__company_name']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_at', 'updated_at', 'applications_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'employer')
        }),
        ('Job Details', {
            'fields': ('description', 'requirements', 'responsibilities', 'job_type', 'experience_level')
        }),
        ('Location & Remote', {
            'fields': ('location', 'is_remote')
        }),
        ('Salary Information', {
            'fields': ('salary_min', 'salary_max', 'salary_currency')
        }),
        ('Status', {
            'fields': ('is_active', 'deadline')
        }),
        ('Statistics', {
            'fields': ('applications_count', 'created_at', 'updated_at'),
        }),
    )


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    """
    Admin configuration for Application model.
    """
    list_display = ['applicant', 'job', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['applicant__username', 'job__title', 'cover_letter']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Application Info', {
            'fields': ('job', 'applicant', 'status')
        }),
        ('Application Details', {
            'fields': ('cover_letter', 'resume_url')
        }),
        ('Employer Notes', {
            'fields': ('notes',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
        }),
    )

