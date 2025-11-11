from django.contrib import admin
from .models import Event, Category, Comment


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title','city','category','organizer','date','is_public')
    list_filter = ('city','category')
    search_fields = ('title','description')


admin.site.register(Category)
admin.site.register(Comment)