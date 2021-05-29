from django import forms
from . models import COLORS_CHOICES, CONDITION_CHOICES, SIZE_CHOICES

SORT_CHOICES = [
    (0,'Price: High to Low'),
    (1,'Price: Low to High'),
]
class FilterForm(forms.Form):
    condition = forms.MultipleChoiceField(
                required=False,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                choices=CONDITION_CHOICES,
            )
    price_min = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'label':'MIN'}), required=False)
    price_max = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control', 'label':'MAX'}), required=False)
    size = forms.MultipleChoiceField(
                required=False,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                choices=SIZE_CHOICES,
            )
    color = forms.MultipleChoiceField(
                required=False,
                widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
                choices=COLORS_CHOICES,
            )

class Search(forms.Form):
    Sort_by = forms.ChoiceField(choices=SORT_CHOICES, widget=forms.Select(attrs={'onchange': 'submit();', 'class':'form-select'}))   

    