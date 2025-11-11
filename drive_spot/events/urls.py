from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.event_create, name='event_create'),
    path('<int:pk>/', views.event_detail, name='event_detail'),
    path('no-permission/', views.no_permission, name='no_permission'),
]