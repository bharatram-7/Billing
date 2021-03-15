from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from .models import *
from django.contrib.auth.models import Group
from .forms import CreateUserForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics, permissions
from .serializers import MenuSerializer
# Create your views here.


def home(request):
    return redirect(reverse('menu_list'))


def signup(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        group = Group.objects.get(name="Customers")
        user.groups.add(group)
        username = form.cleaned_data.get('email')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        login(request, user)
        return redirect(reverse('menu_list'))
    else:
        pass
    context = {
        "form": form
    }
    return render(request, 'authentication/signup.html', context=context)


class ActiveMenuList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    queryset = Menu.objects.filter(active=True)
    context_object_name = 'menus'
    template_name = 'main/menu.html'

    def test_func(self):
        try:
            self.request.user.groups.get(name="Customers")
            return True
        except:
            return False


class MenuList(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Menu.objects.filter(active=True)




