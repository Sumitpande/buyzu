from django import forms
from .models import Order
class OrderCreateForm(forms.ModelForm):
    first_name = forms.CharField(
        label = 'firstname',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'first_name'}
        )
    )   

    last_name = forms.CharField(
        label = 'last name',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'last_name'}
        )
    )   
    email = forms.EmailField(
        label = 'email',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'email'}
        )
    )
    address = forms.CharField(
        label = 'address',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'address'}
        )
    )  
    city = forms.CharField(
        label = 'city',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'city'}
        )
    ) 
    postal_code = forms.CharField(
        label = 'postal code',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'postal_code'}
        )
    ) 

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'email', 'address',
        'postal_code', 'city']