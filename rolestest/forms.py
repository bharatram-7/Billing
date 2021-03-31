from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from .models import CustomUser, Item
from django import forms


class CreateUserFormOld(UserCreationForm):
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


class CreateCustomerForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
        attrs={'label': 'Your Name'}
    ))

    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'text-input',
               'label': 'Your Email Address'}
    ))

    class Meta:
        model = CustomUser
        fields = ['name', 'email']


class CreateStaffForm(forms.ModelForm):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Billing Clerk', 'Billing Clerk')
    ]
    name = forms.CharField(widget=forms.TextInput(
        attrs={'label': 'Name'}
    ))
    email = forms.EmailField(widget=forms.TextInput(
        attrs={'class': 'text-input',
               'label': 'Email Address'}
    ))
    role = forms.ChoiceField(choices=ROLE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'role']


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = CustomUser


class ItemForm(forms.ModelForm):

    price = forms.DecimalField(max_value=100000, min_value=0, max_digits=8, decimal_places=2)

    class Meta:
        model = Item
        exclude = ['menu']
