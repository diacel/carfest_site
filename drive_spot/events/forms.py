from django import forms
from .models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['title','description','city','category','date','location','cover_image','max_participants','is_public']