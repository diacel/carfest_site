from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm

User = get_user_model()

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('index')
        else:
            messages.error(request, 'Ошибка при регистрации. Проверь введённые данные.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, f'Добро пожаловать, {request.user.username}!')
            return redirect('index')
        messages.error(request, 'Неверное имя пользователя или пароль.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из аккаунта.')
    return redirect('index')


@login_required
def profile_view(request, username):
    user_profile = get_object_or_404(User, username=username)
    return render(request, 'users/profile.html', {'user_profile': user_profile})


@login_required
def my_profile_view(request):
    return redirect('profile', username=request.user.username)


# 🔹 Настройки профиля (редактирование)
@login_required
def profile_settings_view(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile', username=user.username)
        else:
            messages.error(request, 'Ошибка при обновлении профиля.')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'users/profile_settings.html', {'form': form})
