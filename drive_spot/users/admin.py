from django.contrib import admin
from .models import UserProfile, City
from django.contrib.auth.admin import UserAdmin


@admin.register(UserProfile)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Profile', {'fields': ('city','avatar','bio','car_info','rating','is_organizer','badges')}),
    )


admin.site.register(City)