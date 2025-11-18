from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, City

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)
    car_info = forms.CharField(required=False)

    class Meta(UserCreationForm.Meta):
        model = UserProfile
        fields = [
            "username", "email", "password1", "password2",
            "city", "avatar", "bio", "car_info"
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['city'].queryset = City.objects.all()
        self.fields['city'].empty_label = "Выберите город"
        
# 🔹 форма для редактирования профиля
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'bio', 'car_info', 'city']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напиши что-то о себе...'}),
            'car_info': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Информация о машине'}),
        }
