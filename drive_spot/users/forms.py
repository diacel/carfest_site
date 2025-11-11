from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'city', 'avatar', 'bio', 'car_info']

# 🔹 форма для редактирования профиля
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'car_info', 'city']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напиши что-то о себе...'}),
            'car_info': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Информация о машине'}),
        }
