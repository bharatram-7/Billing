from django_filters import rest_framework as filters
from .models import Order


class OrderFilter(filters.FilterSet):
    min_date = filters.DateTimeFilter(field_name="date", lookup_expr='gte')
    max_date = filters.DateTimeFilter(field_name="date", lookup_expr='lte')
    user__email = filters.CharFilter()

    class Meta:
        model = Order
        fields = ['min_date', 'max_date', 'user']

