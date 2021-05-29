import django_filters
from django import forms
from .models import Product
# from django_filters import models
from .models import COLORS_CHOICES, CONDITION_CHOICES, SIZE_CHOICES

class ProductFilter(django_filters.FilterSet):
    color = django_filters.MultipleChoiceFilter(choices=COLORS_CHOICES ,field_name='color', widget=forms.CheckboxSelectMultiple, lookup_expr='in')
    condition = django_filters.MultipleChoiceFilter(choices=CONDITION_CHOICES ,field_name='condition',widget=forms.CheckboxSelectMultiple, lookup_expr='in')
    size = django_filters.MultipleChoiceFilter(choices=SIZE_CHOICES ,field_name='size',widget=forms.CheckboxSelectMultiple, lookup_expr='in')
    # price = django_filters.NumberFilter()
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lt')
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gt')

    class Meta:
        model = Product
        fields = ['price','condition', 'color', 'size', ]
        # filter_overrides = {
        #     models.DecimalField: {
        #         'filter_class': django_filters.MultipleChoiceFilter,
        #         # 'extra': lambda f: {
        #         #     'lookup_expr': 'in',
        #         # },
        #     },
            
        #  }