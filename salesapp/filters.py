import django_filters
from .models import Product
from rest_framework import filters

class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = {
            'prod_name': ['iexact','icontains'],
            'price': ['exact','lt','gt','range'],
            'stock': ['exact','lt','gt','range']
        }
