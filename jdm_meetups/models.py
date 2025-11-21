from django.contrib.auth.models import AbstractUser
from django.db import models

class City(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название города')
    region = models.CharField(max_length=100, blank=True, verbose_name='Регион')
    
    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    is_organizer = models.BooleanField(default=False, verbose_name='Организатор')
    nickname = models.CharField(max_length=50, unique=True, verbose_name='Никнейм')
    real_name = models.CharField(max_length=100, blank=True, verbose_name='Настоящее имя')
    bio = models.TextField(max_length=500, blank=True, verbose_name='О себе')
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='Аватар')
    
    def __str__(self):
        return self.nickname
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class CarPhoto(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='car_photos')
    photo = models.ImageField(upload_to='car_photos/', verbose_name='Фото машины')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    def __str__(self):
        return f"Фото машины {self.user.nickname}"
    
    class Meta:
        verbose_name = 'Фото машины'
        verbose_name_plural = 'Фото машин'

class Meetup(models.Model):
    MEETUP_TYPES = [
        ('drift', 'Дрифт'),
        ('jdm', '🇯JDM встреча'),
        ('show', 'Автошоу'),
        ('race', 'Гонки'),
        ('other', 'Другое'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    organizer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'is_organizer': True}, verbose_name='Организатор')
    meetup_type = models.CharField(max_length=20, choices=MEETUP_TYPES, verbose_name='Тип тусовки')
    location = models.CharField(max_length=200, verbose_name='Место проведения')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='Город')
    date_time = models.DateTimeField(verbose_name='Дата и время')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    image = models.ImageField(upload_to='meetup_images/', blank=True, null=True, verbose_name='Изображение')
    
    def is_upcoming(self):
        from django.utils import timezone
        return self.date_time > timezone.now()
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Тусовка'
        verbose_name_plural = 'Тусовки'
        ordering = ['-date_time']