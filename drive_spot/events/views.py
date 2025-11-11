from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Event
from .forms import EventForm


def index(request):
    if request.user.is_authenticated and hasattr(request.user,'city') and request.user.city:
        events = Event.objects.filter(city=request.user.city).order_by('date')
    else:
        events = Event.objects.all().order_by('date')
    return render(request,'index.html',{'events':events})


@login_required
def event_create(request):
    if not request.user.is_organizer:
        return redirect('no_permission')
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
    if form.is_valid():
        event = form.save(commit=False)
        event.organizer = request.user
        event.save()
        form.save_m2m()
        return redirect('event_detail', pk=event.pk)
    else:
        form = EventForm(initial={'city': request.user.city})
    return render(request,'events/event_form.html',{'form':form})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    return render(request,'events/event_detail.html',{'event':event})




def no_permission(request):
    return render(request,'no_permission.html')