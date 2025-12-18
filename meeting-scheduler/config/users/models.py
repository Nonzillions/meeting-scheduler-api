# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

TIMEZONE_CHOICES = [
    ('America/New_York', 'Eastern Time'),
    ('America/Chicago', 'Central Time'),
    ('America/Denver', 'Mountain Time'),
    ('America/Los_Angeles', 'Pacific Time'),
    ('Europe/London', 'UK Time'),
    ('UTC', 'UTC'),
]

class User(AbstractUser):
    timezone = models.CharField(
        max_length=50,
        choices=TIMEZONE_CHOICES,
        default='UTC'
    )
    working_hours_start = models.TimeField(default='09:00:00')
    working_hours_end = models.TimeField(default='17:00:00')
    
    # Add these related_name attributes
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',  # Add this
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',  # Add this
        related_query_name='custom_user',
    )
    
    def __str__(self):
        return self.username