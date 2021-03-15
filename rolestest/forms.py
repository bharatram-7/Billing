from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser
from django import forms


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'text-input',
               'label': 'Your Email Address'}
    ))

    name = forms.CharField(widget=forms.TextInput(
        attrs={'label': 'Your Name'}
    ))

    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'text-input',
               'label': 'Create Password'}
    ))

    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'text-input',
               'label': 'Re-enter Password'}
    ))

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password1', 'password2']


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser