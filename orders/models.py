from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon
# Create your models here.
from product.models import Product
from django.contrib.auth.models import User
import decimal


STATE_CHOICES = [
    ('MH', 'Maharashtra'),
    ('Goa', 'Goa'),
    ('UP', 'Uttar Pradesh'),
    ('MP', 'Madhya Pradesh'),
    
]

# from cities.models import BaseCountry


# class CustomCountryModel(BaseCountry, models.Model):
#     more_data = models.TextField()

#     class Meta(BaseCountry.Meta):
#         pass
from django_countries.fields import CountryField
class ShippingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=50,blank=True,null=True)
    last_name = models.CharField(max_length=50,blank=True,null=True)
    mobile = models.CharField(max_length=250,blank=True,null=True)
    postal_code = models.CharField(max_length=20,blank=True,null=True)
    address = models.CharField(max_length=250 ,blank=True,null=True)
    city = models.CharField(max_length=100 ,blank=True,null=True)
    state = models.CharField(max_length=250,choices=STATE_CHOICES,blank=True,null=True)
    country = CountryField()
    default = models.BooleanField(default=False)

    def is_default(self):
        return self.default
    
    def __str__(self):
        return '{} {}\n{}, {}, {} ({})'.format(self.first_name,self.last_name,self.address,self.city,self.country.name,self.postal_code)

class Order(models.Model):
    user =  models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    mobile = models.CharField(max_length=250,blank=True,null=True)
    
    state = models.CharField(max_length=250,choices=STATE_CHOICES,blank=True,null=True)
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    braintree_id = models.CharField(max_length=150, blank=True)
    coupon = models.ForeignKey(Coupon,
            related_name='orders',
            null=True,
            blank=True,
            on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0,
    validators=[MinValueValidator(0),
                MaxValueValidator(100)])
    class Meta:
        ordering = ('-created',)
    def __str__(self):
        return f'Order {self.id}'
    def get_total_cost(self):
        total_cost = sum(item.get_cost() for item in self.items.all())
        return total_cost - total_cost * (self.discount / decimal.Decimal(100))

class OrderItem(models.Model):
    # user =  models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)

    order = models.ForeignKey(Order,
            related_name='items',
            on_delete=models.CASCADE)
    product = models.ForeignKey(Product,
            related_name='order_items',
            on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.id)
    def get_cost(self):
        return self.price * self.quantity