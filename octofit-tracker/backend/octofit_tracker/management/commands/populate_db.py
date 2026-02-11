from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from octofit_tracker import settings
from django.conf import settings as django_settings

from django.db import connection

# Define models for teams, activities, leaderboard, and workouts
from django.db import models as dj_models

class Team(dj_models.Model):
    name = dj_models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(dj_models.Model):
    user_email = dj_models.EmailField()
    activity_type = dj_models.CharField(max_length=100)
    duration = dj_models.IntegerField()  # in minutes
    class Meta:
        app_label = 'octofit_tracker'

class Workout(dj_models.Model):
    name = dj_models.CharField(max_length=100)
    description = dj_models.TextField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(dj_models.Model):
    user_email = dj_models.EmailField()
    points = dj_models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Delete all data
        User.objects.all().delete()
        Team.objects.all().delete()
        Activity.objects.all().delete()
        Workout.objects.all().delete()
        Leaderboard.objects.all().delete()

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users (super heroes)
        users = [
            {'email': 'tony@marvel.com', 'username': 'IronMan', 'team': marvel},
            {'email': 'steve@marvel.com', 'username': 'CaptainAmerica', 'team': marvel},
            {'email': 'bruce@marvel.com', 'username': 'Hulk', 'team': marvel},
            {'email': 'clark@dc.com', 'username': 'Superman', 'team': dc},
            {'email': 'bruce@dc.com', 'username': 'Batman', 'team': dc},
            {'email': 'diana@dc.com', 'username': 'WonderWoman', 'team': dc},
        ]
        user_objs = []
        for u in users:
            user = User.objects.create_user(email=u['email'], username=u['username'], password='password123')
            user_objs.append(user)

        # Create activities
        Activity.objects.create(user_email='tony@marvel.com', activity_type='Running', duration=30)
        Activity.objects.create(user_email='steve@marvel.com', activity_type='Cycling', duration=45)
        Activity.objects.create(user_email='clark@dc.com', activity_type='Swimming', duration=60)

        # Create workouts
        Workout.objects.create(name='Full Body', description='A full body workout for all heroes.')
        Workout.objects.create(name='Strength', description='Strength training for super heroes.')

        # Create leaderboard
        Leaderboard.objects.create(user_email='tony@marvel.com', points=100)
        Leaderboard.objects.create(user_email='clark@dc.com', points=120)
        Leaderboard.objects.create(user_email='diana@dc.com', points=90)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
