from django import forms
from .models import Order, ShippingAddress
from django_countries.fields import CountryField

STATE_CHOICES = [
    ('MH', 'Maharashtra'),
    ('Goa', 'Goa'),
    ('UP', 'Uttar Pradesh'),
    ('MP', 'Madhya Pradesh'),
    
]
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
    mobile = forms.CharField(
        label = 'Mobile No.',
        max_length = 1000,
        required = True,
        widget = forms.TextInput(
            attrs = {'class': 'form-control', 'name': 'mobile'}
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
    state = forms.ChoiceField(
        label = 'State',
        
        choices = STATE_CHOICES,
        required = True,
        widget = forms.Select(
            attrs = {'class': 'form-select', 'name': 'state'}
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
        fields = ['first_name', 'last_name', 'email','mobile', 'address',
        'postal_code', 'city','state']


class AddressForm(forms.Form):
    
    shipping_address = forms.ModelChoiceField(queryset=ShippingAddress.objects.all(),widget=forms.RadioSelect,required = True)
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(AddressForm, self).__init__(*args, **kwargs)

        if user:
            self.fields['shipping_address'].queryset = ShippingAddress.objects.filter(user=user)
