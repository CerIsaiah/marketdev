#api/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    name = models.CharField(max_length=255, blank=True)
    is_developer = models.BooleanField(null=True)
    is_marketer = models.BooleanField(default=False)
    skills = models.JSONField(default=list)
    bio = models.TextField(blank=True)
    featured = models.BooleanField(default=False)
    profile_views = models.IntegerField(default=0)
    subscription_status = models.CharField(max_length=50, default='Free')
    bookmarked_users = models.ManyToManyField('self', symmetrical=False, related_name='bookmarked_by')

    def __str__(self):
        return self.username

class Connection(models.Model):
    user = models.ForeignKey(User, related_name='connections', on_delete=models.CASCADE)
    connected_with = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  # Allow null for existing rows
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'connected_with')

class Project(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    owner = models.ForeignKey(User, related_name='projects', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Keep existing field name instead of 'timestamp'

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"

