from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from .models import CustomUser, Item
from django import forms


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'text-input',
               'label': 'Your Email Address'}
    ))

    name = forms.CharField(widget=forms.TextInput(
        attrs={'label': 'Your Name'}
    ))

    class Meta:
        model = CustomUser
        fields = ['email', 'name']


class CreateStaffForm(CreateUserForm):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Billing Clerk', 'Billing Clerk')
    ]

    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'password1', 'password2', 'role']


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser


class ItemForm(forms.ModelForm):

    class Meta:
        model = Item
        exclude = ['menu']



