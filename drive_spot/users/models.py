from django.db import models
from django.contrib.auth.models import AbstractUser


class City(models.Model):
    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=160, unique=True)


    def __str__(self):
        return self.name


class UserProfile(AbstractUser):
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
    car_info = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0)
    is_organizer = models.BooleanField(default=False)
    badges = models.JSONField(default=list, blank=True) # простая структура для бейджей


def __str__(self):
    return self.username