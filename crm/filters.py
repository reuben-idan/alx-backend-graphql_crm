import django_filters
from django_filters import rest_framework as filters
from django.db.models import Q
from .models import Customer, Product, Order


class CustomerFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    created_at_gte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='gte')
    created_at_lte = django_filters.DateTimeFilter(field_name='created_at', lookup_expr='lte')
    phone_pattern = django_filters.CharFilter(method='filter_phone_pattern')
    
    class Meta:
        model = Customer
        fields = {
            'name': ['exact', 'icontains'],
            'email': ['exact', 'icontains'],
            'phone': ['exact', 'icontains'],
            'created_at': ['gte', 'lte'],
        }
    
    def filter_phone_pattern(self, queryset, name, value):
        """Custom filter for phone number pattern matching"""
        if value:
            return queryset.filter(phone__startswith=value)
        return queryset


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    price_gte = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_lte = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    stock_gte = django_filters.NumberFilter(field_name='stock', lookup_expr='gte')
    stock_lte = django_filters.NumberFilter(field_name='stock', lookup_expr='lte')
    low_stock = django_filters.BooleanFilter(method='filter_low_stock')
    
    class Meta:
        model = Product
        fields = {
            'name': ['exact', 'icontains'],
            'price': ['exact', 'gte', 'lte'],
            'stock': ['exact', 'gte', 'lte'],
        }
    
    def filter_low_stock(self, queryset, name, value):
        """Custom filter for products with low stock"""
        if value:
            return queryset.filter(stock__lt=10)
        return queryset


class OrderFilter(django_filters.FilterSet):
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    order_date_gte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='gte')
    order_date_lte = django_filters.DateTimeFilter(field_name='order_date', lookup_expr='lte')
    customer_name = django_filters.CharFilter(field_name='customer__name', lookup_expr='icontains')
    product_name = django_filters.CharFilter(method='filter_product_name')
    product_id = django_filters.CharFilter(method='filter_product_id')
    
    class Meta:
        model = Order
        fields = {
            'total_amount': ['exact', 'gte', 'lte'],
            'order_date': ['exact', 'gte', 'lte'],
            'customer': ['exact'],
        }
    
    def filter_product_name(self, queryset, name, value):
        """Filter orders that contain products with matching name"""
        if value:
            return queryset.filter(items__product__name__icontains=value).distinct()
        return queryset
    
    def filter_product_id(self, queryset, name, value):
        """Filter orders that contain a specific product ID"""
        if value:
            return queryset.filter(items__product__id=value).distinct()
        return queryset 