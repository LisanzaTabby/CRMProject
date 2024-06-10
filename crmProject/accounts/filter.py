import django_filters
from django_filters import *
from .models import *
class OrderFilter(django_filters.FilterSet):
    # 'lte'= less than or equal to
    # 'gte' = greater than or equal to
    start_date = DateFilter(field_name='date_created', lookup_expr='gte')
    enddate = DateFilter(field_name='date_created', lookup_expr='lte')
    note = CharFilter(field_name='note', lookup_expr='icontains')

    class Meta:
        model = Order
        fields = '__all__'
        exclude = ['customer', 'date_created']