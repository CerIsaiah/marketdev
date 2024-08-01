# api/management/commands/create_fake_users.py

from django.core.management.base import BaseCommand
from api.models import User
from django.db import transaction
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Creates fake users for testing'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of users to be created')

    @transaction.atomic
    def handle(self, *args, **kwargs):
        total = kwargs['total']
        faker = Faker()

        # Predefined list of skills
        all_skills = [
            "Python", "JavaScript", "React", "Django", "Node.js", "SEO", 
            "Content Marketing", "Social Media Marketing", "Data Analysis",
            "UI/UX Design", "Project Management", "Digital Marketing"
        ]

        # Subscription status options
        subscription_statuses = ['Free', 'Basic', 'Premium', 'Enterprise']

        for _ in range(total):
            username = faker.user_name()
            while User.objects.filter(username=username).exists():
                username = faker.user_name()
            
            user = User.objects.create(
                username=username,
                email=faker.email(),
                name=faker.name(),
                is_developer=random.choice([True, False, None]),
                is_marketer=random.choice([True, False]),
                skills=random.sample(all_skills, random.randint(2, 5)),
                bio=faker.text(max_nb_chars=200),
                featured=random.choice([True, False]),
                profile_views=random.randint(0, 1000),
                subscription_status=random.choice(subscription_statuses)
            )
            user.set_password("testpass123")  # Set a common password for all test users
            
            user.save()

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} fake users'))