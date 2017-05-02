from django.contrib.auth.models import User
from django import forms

from .models import Event
from events.models import UserProfile


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('picture',)


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ('name', 'date',)
