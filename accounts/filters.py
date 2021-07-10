import django_filters
from django_filters import DateFilter, CharFilter, NumberFilter,AllValuesFilter
from django.template.defaultfilters import stringfilter
from django import template
from .models import *


class OrderFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte',label='from')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte',label='to')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer','quantity','date_created']


class CustomerFilter(django_filters.FilterSet):
    customer = AllValuesFilter(field_name="name",label='Customer')

    class Meta:
        model = Customer
        fields = []


class ProductFilter(django_filters.FilterSet):
    start_price = NumberFilter(field_name="price", lookup_expr='gte', label='  Min. Price')
    end_price = NumberFilter(field_name="price", lookup_expr='lte', label='  Max. Price')

    class Meta:
        model = Product
        fields = ['brand','category']


