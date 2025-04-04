import django_filters
from .models import Product,Order
from rest_framework import filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'prod_name': ['iexact','icontains'],
            'price': ['exact','lt','gt','range'],
            'stock': ['exact','lt','gt','range']
        }

class OrderFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at__date')
    class Meta:
        model = Order
        fields = {
            'status': ['iexact'],
            'created_at': ['lt','gt','exact']
        }