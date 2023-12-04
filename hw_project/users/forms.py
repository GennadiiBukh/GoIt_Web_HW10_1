# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']


class AddAuthorForm(forms.Form):
    name = forms.CharField(label='Author Name')


