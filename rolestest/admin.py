from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django.contrib.auth.models import Group

# Register your models here.


class CustomUserAdmin(UserAdmin):
    add_fieldsets = (None, {'fields': ('email', 'name', 'password1', 'password2')}),
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password', 'user_activated')}),
    )
    ordering = ('email',)
    search_fields = ('email',)


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Menu)
admin.site.register(Item)
admin.site.register(CartItem)
admin.site.register(PurchasedItem)
admin.site.register(Order)
