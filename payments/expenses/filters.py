import django_filters
from .models import Expense

class ExpenseFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name='amount', lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    category = django_filters.ChoiceFilter(choices=Expense.CATEGORY_CHOICES)
    
    class Meta:
        model = Expense
        fields = ['user', 'category']