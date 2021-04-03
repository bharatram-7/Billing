from rest_framework import permissions
import copy


class CustomDjangoModelPermissions(permissions.DjangoModelPermissions):
    def __init__(self):
        self.perms_map = copy.deepcopy(self.perms_map)
        self.perms_map['GET'] = ['%(app_label)s.view_%(model_name)s']


class OrderStatusPermission(permissions.BasePermission):
    message = "Customers are not allowed to modify orders"

    def has_permission(self, request, view):
        group = request.user.groups.filter(user=request.user)[0]
        if group.name == "Customers":
            return False
        else:
            return True


class OrderRatingPermission(permissions.BasePermission):
    message = "Rating is only for customers"

    def has_permission(self, request, view):
        group = request.user.groups.filter(user=request.user)[0]
        if group.name == "Customers":
            return True
        else:
            return False


class AdminPermission(permissions.BasePermission):
    message = "You're not allowed to access this endpoint"

    def has_permission(self, request, view):
        group = request.user.groups.filter(user=request.user)[0]
        if group.name == "Admin":
            return True
        else:
            return False


