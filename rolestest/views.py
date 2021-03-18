from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login
from django.views.generic import ListView
from .models import *
from django.contrib.auth.models import Group
from .forms import CreateUserForm, CreateStaffForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics, permissions
from .serializers import *
from .permissions import CustomDjangoModelPermissions
from django.http import HttpResponse
# Create your views here.


def home(request):
    print(request.user)
    group = request.user.groups.filter(user=request.user)[0]
    if group.name == "Customers":
        return redirect(reverse('menu'))
    return redirect(reverse('staff_orders'))


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


def createStaff(request):
    form = CreateStaffForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        role = form.cleaned_data['role']
        roles = ['Admin', 'Billing Clerk']
        if role in roles:
            group = Group.objects.get(name=role)
            user.groups.add(group)
        return HttpResponse(status=201)
    else:
        pass
    context = {
        "form": form
    }
    return render(request, 'main/adduser.html', context=context)


class ActiveMenuList(LoginRequiredMixin, ListView):
    queryset = Menu.objects.filter(active=True)
    context_object_name = 'menus'
    template_name = 'main/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.name
        return context


class Checkout(LoginRequiredMixin, ListView):
    template_name = 'main/checkout.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.name
        return context

    def get_queryset(self):
        return


class Orders(LoginRequiredMixin, ListView):
    template_name = 'main/orders.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['name'] = self.request.user.name
        return context

    def get_queryset(self):
        return


class OrderItems(LoginRequiredMixin, ListView):
    template_name = 'main/orderdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return


class StaffOrders(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/stafforders.html'

    def test_func(self):
        try:
            self.request.user.groups.get(name="Customers")
            return False
        except:
            return True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return


class UsersView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/users.html'

    def test_func(self):
        try:
            self.request.user.groups.get(name="Admin")
            return True
        except:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

    def get_queryset(self):
        return


class UserDetailsView(LoginRequiredMixin, ListView):
    template_name = 'main/userdetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        context['id'] = self.kwargs['pk']
        return context

    def get_queryset(self):
        return


# REST APIs from here


class MenuList(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Menu.objects.filter(active=True)


class ViewCartWithItem(generics.ListAPIView):
    serializer_class = ViewCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class ViewCartItem(generics.ListCreateAPIView):
    serializer_class = CreateCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        print(serializer)
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class ModifyCartItem(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateDeleteCartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            return Order.objects.filter(user=self.request.user).order_by('-id')
        else:
            return Order.objects.all()


class CreateOrderWithItems(generics.CreateAPIView):
    serializer_class = OrderWithItemsSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.all()

    def perform_create(self, serializer):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            serializer.save(user=self.request.user)
        else:
            user = CustomUser.objects.get(email="walkincustomer@cafe.co.in")
            serializer.save(user=user)


class OrderWithItemsDetail(generics.RetrieveAPIView):
    serializer_class = OrderWithItemsSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.all()


class OrderUpdate(generics.UpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.all()


class PurchasedItemList(generics.ListCreateAPIView):
    serializer_class = PurchasedItemSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return PurchasedItem.objects.all()


class UserList(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return CustomUser.objects.all()


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return CustomUser.objects.all()

