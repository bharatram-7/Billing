from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth import login
from django.views.generic import ListView, View
from .models import *
from django.contrib.auth.models import Group
from .forms import CreateUserForm, CreateStaffForm, ItemForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from rest_framework import generics, permissions
from .serializers import *
from .permissions import CustomDjangoModelPermissions, OrderStatusPermission, OrderRatingPermission
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from .tokens import account_activation_token
from django.template.loader import render_to_string
from .filters import OrderFilter
from django_filters import rest_framework as filters

# Create your views here.


def home(request):
    print(request.user)
    if request.user.is_anonymous:
        return redirect(reverse('login'))
    group = request.user.groups.filter(user=request.user)[0]
    if group.name == "Customers":
        return redirect(reverse('menu'))

    return redirect(reverse('staff_orders'))


def activation_sent_view(request):
    return render(request, 'authentication/activation_email_sent.html')


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.user_activated = True
        user.save()
        return redirect(reverse('login'))
    else:
        return render(request, 'authentication/activation_invalid.html')


def signup(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        user.refresh_from_db()
        group = Group.objects.get(name="Customers")
        user.groups.set([group])
        user.name = form.cleaned_data.get('name')
        user.email = form.cleaned_data.get('email')
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        subject = 'Activate your account'
        message = render_to_string('authentication/activation_template.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        user.email_user(subject, message)
        return redirect('activation_email_sent')
    else:
        context = {
            "form": form
        }
        return render(request, 'authentication/signup.html', context=context)


def create_staff(request):
    form = CreateStaffForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        role = form.cleaned_data['role']
        roles = ['Admin', 'Billing Clerk']
        if role in roles:
            group = Group.objects.get(name=role)
            user.groups.set([group])
        return redirect(reverse('users'))
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
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group:
            context['group'] = group.name
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


class OrderRatingView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/orderrating.html'

    def test_func(self):
        try:
            self.request.user.groups.get(name="Customers")
            return True
        except:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class MenusView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/adminmenu.html'

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


class MenuDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'main/adminmenudetail.html'
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        context = {
            "form": form,
            "id": kwargs['pk']
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            menu_id = request.POST.get('menu')
            menu = Menu.objects.get(id=menu_id)
            form.menu = menu
            print(form.menu)
            form.save()
            return redirect('menu_detail_view', pk=menu_id)
        else:
            pass
        context = {
            "form": form,
            "id": kwargs['pk']
        }
        return render(request, self.template_name, context=context)

    def test_func(self):
        try:
            self.request.user.groups.get(name="Admin")
            return True
        except:
            return False


class ItemDetailView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'main/adminitemdetail.html'
    form_class = ItemForm

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        form = self.form_class(instance=item)
        context = {
            "form": form,
            "id": kwargs['pk'],
            "menu_id": kwargs['menu_id']
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['pk'])
        form = self.form_class(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form = form.save(commit=False)
            menu_id = request.POST.get('menu')
            menu = Menu.objects.get(id=menu_id)
            form.menu = menu
            print(form.menu)
            form.save()
            return redirect('menu_detail_view', pk=menu_id)
        else:
            pass
        context = {
            "form": form,
            "id": kwargs['pk']
        }
        return render(request, self.template_name, context=context)

    def test_func(self):
        try:
            self.request.user.groups.get(name="Admin")
            return True
        except:
            return False


class ReportsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'main/reports.html'

    def test_func(self):
        try:
            self.request.user.groups.get(name="Admin")
            return True
        except:
            return False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customers = CustomUser.objects.filter(groups__name="Customers")
        context['users'] = customers
        return context

    def get_queryset(self):
        return


# REST APIs from here


class MenuWithItemList(generics.ListAPIView):
    serializer_class = MenuWithItemsSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return Menu.objects.filter(active=True)


class MenuList(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Admin":
            return Menu.objects.all()
        else:
            return Menu.objects.none()


class MenuDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuWithItemsSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Admin":
            return Menu.objects.all()
        else:
            return Menu.objects.none()


class ItemDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ItemSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return Item.objects.all()


class ViewCartWithItem(generics.ListAPIView):
    serializer_class = ViewCartSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class ViewCartItem(generics.ListCreateAPIView):
    serializer_class = CreateCartSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class ModifyCartItem(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UpdateDeleteCartSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)


class OrderList(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_class = OrderFilter

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
        # Empty user's cart after order creation
        cart_items = CartItem.objects.filter(user=self.request.user)
        for item in cart_items:
            item.delete()


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
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions, OrderStatusPermission]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.all()


class OrderRating(generics.RetrieveUpdateAPIView):
    serializer_class = OrderRatingSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions, OrderRatingPermission]

    def get_queryset(self):
        group = self.request.user.groups.filter(user=self.request.user)[0]
        if group.name == "Customers":
            return Order.objects.filter(user=self.request.user)
        else:
            return Order.objects.none()


class PurchasedItemList(generics.ListCreateAPIView):
    serializer_class = PurchasedItemSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return PurchasedItem.objects.all()


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return CustomUser.objects.all().exclude(id=8)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, CustomDjangoModelPermissions]

    def get_queryset(self):
        return CustomUser.objects.all().exclude(id=8)

    def perform_destroy(self, instance):
        if instance.id == self.request.user.id:
            raise serializers.ValidationError("Can't delete self")
        instance.delete()

