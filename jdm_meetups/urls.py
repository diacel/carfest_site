from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('meetup/<int:pk>/', views.meetup_detail, name='meetup_detail'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
    
    path('register/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),
    
    path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('create-meetup/', views.create_meetup, name='create_meetup'),
    path('add-car-photo/', views.add_car_photo, name='add_car_photo'),
    
    path('toggle-city-filter/', views.toggle_city_filter, name='toggle_city_filter'),
]