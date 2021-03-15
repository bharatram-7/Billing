from django.db import models
from django.contrib.auth.models import Group
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone


class CustomUserManager(BaseUserManager):

    def create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        if not name:
            raise ValueError('Name is required')
        name = name
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save()
        if extra_fields.get('is_superuser') is True:
            user.groups.add(Group.objects.get("Admin"))
        return user

    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must be a Staff')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must not be have superuser set to True')
        return self.create_user(name, email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField('Email', unique=True)
    name = models.TextField('User name', max_length=50, blank=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Menu(models.Model):
    name = models.CharField(max_length=50, unique=True, blank=False)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'menu'
        verbose_name_plural = 'menus'
        permissions = [
            ('can_view_menus', 'Can view all menus'),
            ('can_manage_menus', 'Can create, edit, or delete menus'),
        ]

    def __str__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='items')

    class Meta:
        verbose_name = 'item'
        verbose_name_plural = 'items'
        permissions = [
            ('can_view_items', 'Can view all items'),
            ('can_manage_items', 'Can create, edit, or delete items'),
        ]

    def __str__(self):
        return self.name


class CartManager(models.Manager):
    # Need to define a function to return the total of the cart
    def total(self, user):
        cart = CartItem.objects.filter(user=user)
        sum = 0
        for cartitem in cart:
            sum += (cartitem.item.price * cartitem.quantity)
        return sum


class CartItem(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(blank=False, null=False)

    objects = CartManager()

    class Meta:
        permissions = [
            ('can_manage_carts', 'Can view, create, edit, or delete cart items'),
        ]

    def __str__(self):
        return self.user.name + str(self.id)


class Order(models.Model):
    PENDING = "P"
    DELIVERED = "D"
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (DELIVERED, 'Delivered')
    ]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())
    total = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING
    )

    class Meta:
        permissions = [
            ('can_view_orders', 'Can view his/her orders'),
            ('can_view_all_orders', 'Can view all orders'),
        ]

    def __str__(self):
        return self.status


class PurchasedItem(models.Model):
    item = models.CharField(max_length=100)
    quantity = models.PositiveSmallIntegerField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('can_view_purchased_items', 'Can view his/her purchased items'),
            ('can_view_all_purchased_items', 'Can view all purchased items'),
        ]

    def __str__(self):
        return str(self.id) + self.item















