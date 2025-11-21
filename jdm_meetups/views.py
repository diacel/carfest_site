from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import CustomUser, Meetup, CarPhoto, City
from .forms import CustomUserChangeForm, MeetupForm, CarPhotoForm, CustomUserCreationForm

def home(request):
    now = timezone.now()
    
    if request.user.is_authenticated and request.user.city:
        user_city = request.user.city
        upcoming_meetups = Meetup.objects.filter(
            date_time__gte=now, 
            city=user_city
        ).order_by('date_time')
        past_meetups = Meetup.objects.filter(
            date_time__lt=now, 
            city=user_city
        ).order_by('-date_time')
        
        messages.info(request, f'Показываем тусовки вашего города: {user_city.name}')
    else:
        upcoming_meetups = Meetup.objects.filter(date_time__gte=now).order_by('date_time')
        past_meetups = Meetup.objects.filter(date_time__lt=now).order_by('-date_time')
        
        if request.user.is_authenticated and not request.user.city:
            messages.warning(request, 'Выберите город в настройках профиля, чтобы видеть тусовки рядом с вами!')
    
    return render(request, 'home.html', {
        'upcoming_meetups': upcoming_meetups,
        'past_meetups': past_meetups,
        'show_all_cities': not (request.user.is_authenticated and request.user.city)
    })

def meetup_detail(request, pk):
    meetup = get_object_or_404(Meetup, pk=pk)
    
    if request.user.is_authenticated and request.user.city and meetup.city != request.user.city:
        messages.warning(request, f'Это мероприятие проходит в {meetup.city.name}, а ваш город - {request.user.city.name}')
    
    return render(request, 'meetup_detail.html', {'meetup': meetup})

def profile_view(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_meetups = Meetup.objects.filter(organizer=user) if user.is_organizer else None
    return render(request, 'profile.html', {
        'profile_user': user,
        'user_meetups': user_meetups
    })

def register_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.nickname}! Ваш аккаунт успешно создан.')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'register.html', {'form': form})

def custom_logout(request):
    if request.user.is_authenticated:
        messages.info(request, f'До свидания, {request.user.nickname}! Возвращайтесь снова!')
    logout(request)
    return redirect('home')

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен!')
            return redirect('profile', username=request.user.username)
    else:
        form = CustomUserChangeForm(instance=request.user)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def create_meetup(request):
    if not request.user.is_organizer:
        messages.error(request, 'Только организаторы могут создавать мероприятия!')
        return redirect('home')
    
    if request.method == 'POST':
        form = MeetupForm(request.POST, request.FILES)
        if form.is_valid():
            meetup = form.save(commit=False)
            meetup.organizer = request.user
            meetup.save()
            messages.success(request, 'Тусовка создана!')
            return redirect('meetup_detail', pk=meetup.pk)
    else:
        form = MeetupForm()
    
    return render(request, 'create_meetup.html', {'form': form})

@login_required
def add_car_photo(request):
    if request.method == 'POST':
        form = CarPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            car_photo = form.save(commit=False)
            car_photo.user = request.user
            car_photo.save()
            messages.success(request, 'Фото добавлено в галерею!')
            return redirect('profile', username=request.user.username)
    else:
        form = CarPhotoForm()
    
    return render(request, 'add_car_photo.html', {'form': form})

@login_required
def toggle_city_filter(request):
    """Переключение между показом всех городов и только своего города"""
    show_all = request.GET.get('show_all', 'false') == 'true'
    
    if show_all:
        messages.info(request, 'Показываем тусовки из всех городов')
    else:
        messages.info(request, f'Показываем тусовки вашего города: {request.user.city.name}')
    
    request.session['show_all_cities'] = show_all
    
    return redirect('home')