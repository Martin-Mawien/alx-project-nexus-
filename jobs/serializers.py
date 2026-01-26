from rest_framework import serializers
from .models import Category, Job, Application
from accounts.serializers import UserSerializer


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """
    jobs_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'jobs_count', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_jobs_count(self, obj):
        return obj.jobs.filter(is_active=True).count()


class JobListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Job list view with optimized fields.
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    employer_name = serializers.SerializerMethodField(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'slug', 'category', 'category_name',
            'employer', 'employer_name', 'job_type', 'experience_level',
            'location', 'is_remote', 'salary_min', 'salary_max',
            'salary_currency', 'is_active', 'deadline',
            'applications_count', 'created_at'
        ]
        read_only_fields = ['id', 'created_at', 'applications_count']

    def get_employer_name(self, obj):
        return obj.employer.company_name or obj.employer.get_full_name() or obj.employer.username


class JobDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Job model with all fields.
    """
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        write_only=True
    )
    employer = UserSerializer(read_only=True)
    applications_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'slug', 'description', 'requirements',
            'responsibilities', 'category', 'category_id', 'employer',
            'job_type', 'experience_level', 'location', 'is_remote',
            'salary_min', 'salary_max', 'salary_currency', 'is_active',
            'deadline', 'applications_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'employer', 'created_at', 'updated_at', 'applications_count']

    def create(self, validated_data):
        # Set the employer from the request user
        validated_data['employer'] = self.context['request'].user
        return super().create(validated_data)


class ApplicationListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Application list view.
    """
    job_title = serializers.CharField(source='job.title', read_only=True)
    applicant_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_title', 'applicant', 'applicant_name',
            'status', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

    def get_applicant_name(self, obj):
        return obj.applicant.get_full_name() or obj.applicant.username


class ApplicationDetailSerializer(serializers.ModelSerializer):
    """
    Detailed serializer for Application model.
    """
    job = JobListSerializer(read_only=True)
    job_id = serializers.PrimaryKeyRelatedField(
        queryset=Job.objects.filter(is_active=True),
        source='job',
        write_only=True
    )
    applicant = UserSerializer(read_only=True)

    class Meta:
        model = Application
        fields = [
            'id', 'job', 'job_id', 'applicant', 'cover_letter',
            'resume_url', 'status', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'applicant', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Set the applicant from the request user
        validated_data['applicant'] = self.context['request'].user
        return super().create(validated_data)

    def validate_job_id(self, value):
        # Check if user already applied to this job
        user = self.context['request'].user
        if Application.objects.filter(job=value, applicant=user).exists():
            raise serializers.ValidationError(
                'You have already applied to this job.'
            )
        return value
