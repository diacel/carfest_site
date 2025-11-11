from django.db import models
from django.utils import timezone
from users.models import UserProfile, City


class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=60, unique=True)


def __str__(self):
    return self.name


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    organizer = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='organized_events')
    date = models.DateTimeField()
    location = models.CharField(max_length=255, blank=True)
    cover_image = models.ImageField(upload_to='event_covers/', null=True, blank=True)
    max_participants = models.PositiveIntegerField(null=True, blank=True)
    participants = models.ManyToManyField(UserProfile, related_name='events_participated', blank=True)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"{self.title} — {self.city}"


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


def __str__(self):
    return f"Comment by {self.user} on {self.event}"