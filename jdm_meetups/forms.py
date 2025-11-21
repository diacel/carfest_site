from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from .models import CustomUser, Meetup, CarPhoto, City

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город",
        required=True,
        label="Город"
    )
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'nickname', 'city', 'password1', 'password2')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input-field'})
        
        self.fields['username'].help_text = 'Обязательное поле. Только буквы, цифры и @/./+/-/_'
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = 'Для подтверждения введите тот же пароль'

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже используется')
        return email

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if CustomUser.objects.filter(nickname=nickname).exists():
            raise ValidationError('Этот никнейм уже занят')
        return nickname

class CustomUserChangeForm(UserChangeForm):
    password = None
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город",
        required=True,
        label="Город"
    )
    
    class Meta:
        model = CustomUser
        fields = ('nickname', 'real_name', 'bio', 'city', 'avatar')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'input-field'})

class MeetupForm(forms.ModelForm):
    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        empty_label="Выберите город",
        required=True,
        label="Город"
    )
    
    class Meta:
        model = Meetup
        fields = ('title', 'description', 'meetup_type', 'location', 'city', 'date_time', 'image')
        widgets = {
            'date_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'input-field'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'input-field'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field != 'description':
                self.fields[field].widget.attrs.update({'class': 'input-field'})

class CarPhotoForm(forms.ModelForm):
    class Meta:
        model = CarPhoto
        fields = ('photo',)
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['photo'].widget.attrs.update({'class': 'input-field'})