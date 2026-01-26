from django.core.management.base import BaseCommand
from django.utils.text import slugify
from django.contrib.auth import get_user_model
from jobs.models import Category, Job, Application
from datetime import datetime, timedelta

User = get_user_model()


class Command(BaseCommand):
    help = 'Seeds the database with sample data for testing'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@jobboard.com',
                password='admin123',
                role=User.Role.ADMIN,
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write(self.style.SUCCESS('✓ Created admin user'))
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write('✓ Admin user already exists')

        # Create employer users
        employers_data = [
            {
                'username': 'techcorp',
                'email': 'hr@techcorp.com',
                'password': 'employer123',
                'company_name': 'TechCorp Inc',
                'first_name': 'John',
                'last_name': 'Smith',
                'phone_number': '+1-555-0101',
                'bio': 'Leading technology company focused on innovative solutions.'
            },
            {
                'username': 'innovate',
                'email': 'jobs@innovate.com',
                'password': 'employer123',
                'company_name': 'Innovate Labs',
                'first_name': 'Jane',
                'last_name': 'Doe',
                'phone_number': '+1-555-0102',
                'bio': 'Startup focused on cutting-edge AI and ML solutions.'
            },
        ]

        employers = []
        for emp_data in employers_data:
            if not User.objects.filter(username=emp_data['username']).exists():
                employer = User.objects.create_user(
                    username=emp_data['username'],
                    email=emp_data['email'],
                    password=emp_data['password'],
                    role=User.Role.EMPLOYER,
                    company_name=emp_data['company_name'],
                    first_name=emp_data['first_name'],
                    last_name=emp_data['last_name'],
                    phone_number=emp_data['phone_number'],
                    bio=emp_data['bio']
                )
                employers.append(employer)
                self.stdout.write(self.style.SUCCESS(f'✓ Created employer: {employer.username}'))
            else:
                employer = User.objects.get(username=emp_data['username'])
                employers.append(employer)
                self.stdout.write(f'✓ Employer {employer.username} already exists')

        # Create job seeker users
        job_seekers_data = [
            {
                'username': 'jdoe',
                'email': 'jdoe@email.com',
                'password': 'seeker123',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone_number': '+1-555-0201',
                'bio': 'Experienced software developer looking for new opportunities.'
            },
            {
                'username': 'asmith',
                'email': 'asmith@email.com',
                'password': 'seeker123',
                'first_name': 'Alice',
                'last_name': 'Smith',
                'phone_number': '+1-555-0202',
                'bio': 'Recent graduate with a passion for web development.'
            },
        ]

        job_seekers = []
        for seeker_data in job_seekers_data:
            if not User.objects.filter(username=seeker_data['username']).exists():
                seeker = User.objects.create_user(
                    username=seeker_data['username'],
                    email=seeker_data['email'],
                    password=seeker_data['password'],
                    role=User.Role.JOB_SEEKER,
                    first_name=seeker_data['first_name'],
                    last_name=seeker_data['last_name'],
                    phone_number=seeker_data['phone_number'],
                    bio=seeker_data['bio']
                )
                job_seekers.append(seeker)
                self.stdout.write(self.style.SUCCESS(f'✓ Created job seeker: {seeker.username}'))
            else:
                seeker = User.objects.get(username=seeker_data['username'])
                job_seekers.append(seeker)
                self.stdout.write(f'✓ Job seeker {seeker.username} already exists')

        # Create categories
        categories_data = [
            {'name': 'Software Development', 'description': 'Jobs related to software development and programming'},
            {'name': 'Data Science', 'description': 'Data analysis, machine learning, and AI positions'},
            {'name': 'Design', 'description': 'UI/UX design and graphic design positions'},
            {'name': 'Marketing', 'description': 'Digital marketing and content creation roles'},
            {'name': 'Sales', 'description': 'Sales and business development positions'},
        ]

        categories = []
        for cat_data in categories_data:
            slug = slugify(cat_data['name'])
            category, created = Category.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': cat_data['name'],
                    'description': cat_data['description']
                }
            )
            categories.append(category)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created category: {category.name}'))
            else:
                self.stdout.write(f'✓ Category {category.name} already exists')

        # Create jobs
        jobs_data = [
            {
                'title': 'Senior Python Developer',
                'description': 'We are looking for an experienced Python developer to join our backend team.',
                'requirements': '5+ years of Python experience, Django expertise, REST API development',
                'responsibilities': 'Design and implement backend services, mentor junior developers',
                'category': categories[0],
                'employer': employers[0],
                'job_type': Job.JobType.FULL_TIME,
                'experience_level': Job.ExperienceLevel.SENIOR,
                'location': 'San Francisco, CA',
                'is_remote': True,
                'salary_min': 120000,
                'salary_max': 160000,
                'deadline': datetime.now() + timedelta(days=30)
            },
            {
                'title': 'Frontend React Developer',
                'description': 'Join our frontend team to build amazing user interfaces.',
                'requirements': '3+ years React experience, TypeScript, modern CSS',
                'responsibilities': 'Build responsive web applications, work with designers',
                'category': categories[0],
                'employer': employers[1],
                'job_type': Job.JobType.FULL_TIME,
                'experience_level': Job.ExperienceLevel.INTERMEDIATE,
                'location': 'New York, NY',
                'is_remote': False,
                'salary_min': 90000,
                'salary_max': 130000,
                'deadline': datetime.now() + timedelta(days=45)
            },
            {
                'title': 'Data Scientist',
                'description': 'Analyze data and build ML models for our products.',
                'requirements': 'PhD or Masters in related field, Python, ML frameworks',
                'responsibilities': 'Develop ML models, analyze data trends, collaborate with engineers',
                'category': categories[1],
                'employer': employers[0],
                'job_type': Job.JobType.FULL_TIME,
                'experience_level': Job.ExperienceLevel.SENIOR,
                'location': 'Remote',
                'is_remote': True,
                'salary_min': 130000,
                'salary_max': 180000,
                'deadline': datetime.now() + timedelta(days=60)
            },
            {
                'title': 'UX Designer',
                'description': 'Design beautiful and intuitive user experiences.',
                'requirements': '2+ years UX design, Figma, user research',
                'responsibilities': 'Create wireframes, conduct user research, collaborate with developers',
                'category': categories[2],
                'employer': employers[1],
                'job_type': Job.JobType.CONTRACT,
                'experience_level': Job.ExperienceLevel.INTERMEDIATE,
                'location': 'Los Angeles, CA',
                'is_remote': False,
                'salary_min': 80000,
                'salary_max': 110000,
                'deadline': datetime.now() + timedelta(days=20)
            },
        ]

        jobs = []
        for job_data in jobs_data:
            slug = slugify(job_data['title']) + '-' + slugify(job_data['employer'].company_name)
            job, created = Job.objects.get_or_create(
                slug=slug,
                defaults=job_data
            )
            jobs.append(job)
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Created job: {job.title}'))
            else:
                self.stdout.write(f'✓ Job {job.title} already exists')

        # Create applications
        if job_seekers and jobs:
            applications_data = [
                {
                    'job': jobs[0],
                    'applicant': job_seekers[0],
                    'cover_letter': 'I am very interested in this position and believe my experience aligns well with your requirements.',
                    'resume_url': 'https://example.com/resume1.pdf',
                    'status': Application.Status.PENDING
                },
                {
                    'job': jobs[1],
                    'applicant': job_seekers[1],
                    'cover_letter': 'As a passionate frontend developer, I would love to join your team.',
                    'resume_url': 'https://example.com/resume2.pdf',
                    'status': Application.Status.REVIEWING
                },
                {
                    'job': jobs[0],
                    'applicant': job_seekers[1],
                    'cover_letter': 'I have extensive Python experience and would be a great fit for this role.',
                    'resume_url': 'https://example.com/resume3.pdf',
                    'status': Application.Status.SHORTLISTED
                },
            ]

            for app_data in applications_data:
                application, created = Application.objects.get_or_create(
                    job=app_data['job'],
                    applicant=app_data['applicant'],
                    defaults={
                        'cover_letter': app_data['cover_letter'],
                        'resume_url': app_data['resume_url'],
                        'status': app_data['status']
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'✓ Created application: {application.applicant.username} -> {application.job.title}'))
                else:
                    self.stdout.write(f'✓ Application already exists')

        self.stdout.write(self.style.SUCCESS('\n✓ Database seeding completed successfully!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('  Admin: username=admin, password=admin123')
        self.stdout.write('  Employer: username=techcorp, password=employer123')
        self.stdout.write('  Employer: username=innovate, password=employer123')
        self.stdout.write('  Job Seeker: username=jdoe, password=seeker123')
        self.stdout.write('  Job Seeker: username=asmith, password=seeker123')
