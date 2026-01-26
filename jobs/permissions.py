from rest_framework import permissions


class IsEmployerOrReadOnly(permissions.BasePermission):
    """
    Permission class that allows only employers to create/edit jobs.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_employer


class IsJobOwnerOrReadOnly(permissions.BasePermission):
    """
    Permission class that allows only job owner to edit their jobs.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.employer == request.user


class IsApplicationOwnerOrJobOwner(permissions.BasePermission):
    """
    Permission that allows applicants to view/edit their applications,
    and employers to view applications for their jobs.
    """
    def has_object_permission(self, request, view, obj):
        # Applicant can view/edit their own application
        if obj.applicant == request.user:
            # Applicants cannot change status or notes
            if request.method in ['PUT', 'PATCH']:
                # Check if they're trying to modify protected fields
                protected_fields = {'status', 'notes'}
                if any(field in request.data for field in protected_fields):
                    return False
            return True
        
        # Employer can view/edit applications for their jobs
        if obj.job.employer == request.user:
            return True
        
        return False


class IsJobSeekerForApplication(permissions.BasePermission):
    """
    Permission that allows only job seekers to create applications.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated and request.user.is_job_seeker
        return request.user.is_authenticated
