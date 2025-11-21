from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Meetup, CarPhoto, City

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('name', 'region')
    list_filter = ('region',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'nickname', 'email', 'city', 'is_organizer', 'is_staff')
    list_filter = ('is_organizer', 'is_staff', 'city')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {
            'fields': ('nickname', 'real_name', 'bio', 'city', 'avatar', 'is_organizer')
        }),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Дополнительная информация', {
            'fields': ('nickname', 'email', 'city', 'is_organizer')
        }),
    )

@admin.register(Meetup)
class MeetupAdmin(admin.ModelAdmin):
    list_display = ('title', 'meetup_type', 'city', 'organizer', 'date_time', 'is_upcoming')
    list_filter = ('meetup_type', 'city', 'date_time')
    search_fields = ('title', 'description', 'organizer__username')
    date_hierarchy = 'date_time'

@admin.register(CarPhoto)
class CarPhotoAdmin(admin.ModelAdmin):
    list_display = ('user', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('user__username', 'user__nickname')