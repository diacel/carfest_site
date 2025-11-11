from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('profile/settings/', views.profile_settings_view, name='profile_settings'),  # 🔹 сначала settings
    path('profile/', views.my_profile_view, name='my_profile'),
    path('profile/<str:username>/', views.profile_view, name='profile'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
