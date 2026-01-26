from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count, Prefetch
from .models import Category, Job, Application
from .serializers import (
    CategorySerializer, JobListSerializer, JobDetailSerializer,
    ApplicationListSerializer, ApplicationDetailSerializer
)
from .permissions import (
    IsEmployerOrReadOnly, IsJobOwnerOrReadOnly,
    IsApplicationOwnerOrJobOwner, IsJobSeekerForApplication
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category model with optimized queries.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    lookup_field = 'slug'

    def get_queryset(self):
        # Optimize with prefetch of active jobs
        return Category.objects.prefetch_related(
            Prefetch('jobs', queryset=Job.objects.filter(is_active=True))
        )

    @action(detail=True, methods=['get'])
    def jobs(self, request, slug=None):
        """
        Get all jobs in a category.
        """
        category = self.get_object()
        jobs = category.jobs.filter(is_active=True).select_related(
            'employer', 'category'
        ).annotate(
            applications_count=Count('applications')
        )
        
        serializer = JobListSerializer(jobs, many=True)
        return Response(serializer.data)


class JobViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Job model with optimized queries and filtering.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, IsEmployerOrReadOnly, IsJobOwnerOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'experience_level', 'is_remote', 'is_active', 'category']
    search_fields = ['title', 'description', 'location', 'requirements']
    ordering_fields = ['created_at', 'title', 'deadline']
    lookup_field = 'slug'

    def get_queryset(self):
        # Optimize with select_related and prefetch_related
        queryset = Job.objects.select_related(
            'employer', 'category'
        ).prefetch_related(
            'applications'
        ).annotate(
            applications_count=Count('applications')
        )
        
        # Filter by employer if requested
        employer_id = self.request.query_params.get('employer', None)
        if employer_id:
            queryset = queryset.filter(employer_id=employer_id)
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return JobListSerializer
        return JobDetailSerializer

    @action(detail=True, methods=['get'])
    def applications(self, request, slug=None):
        """
        Get all applications for a job (only accessible by job owner).
        """
        job = self.get_object()
        
        # Only job owner can see applications
        if job.employer != request.user:
            return Response(
                {'error': 'You do not have permission to view these applications.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        applications = job.applications.select_related('applicant').all()
        serializer = ApplicationListSerializer(applications, many=True)
        return Response(serializer.data)


class ApplicationViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Application model with role-based access control.
    """
    permission_classes = [IsJobSeekerForApplication, IsApplicationOwnerOrJobOwner]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'job']
    ordering_fields = ['created_at', 'status']

    def get_queryset(self):
        # Optimize with select_related
        queryset = Application.objects.select_related(
            'job', 'job__category', 'job__employer', 'applicant'
        )
        
        # Job seekers see only their own applications
        if self.request.user.is_job_seeker:
            queryset = queryset.filter(applicant=self.request.user)
        # Employers see applications for their jobs
        elif self.request.user.is_employer:
            queryset = queryset.filter(job__employer=self.request.user)
        # Admins see all
        elif self.request.user.is_admin_user:
            pass
        else:
            queryset = queryset.none()
        
        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return ApplicationListSerializer
        return ApplicationDetailSerializer

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """
        Update application status (only accessible by job owner).
        """
        application = self.get_object()
        
        # Only job owner can update status
        if application.job.employer != request.user:
            return Response(
                {'error': 'You do not have permission to update this application.'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        new_status = request.data.get('status')
        if new_status not in dict(Application.Status.choices):
            return Response(
                {'error': 'Invalid status value.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        application.status = new_status
        application.notes = request.data.get('notes', application.notes)
        application.save()
        
        serializer = ApplicationDetailSerializer(application)
        return Response(serializer.data)

