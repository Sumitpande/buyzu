from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200,
            db_index=True)
    # sub = models.CharField(max_length=200,
    #         db_index=True)
    slug = models.SlugField(max_length=200,
            unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_list_by_category',
                        args=[self.slug])

# class SubCategory(models.Model):
#     name = models.CharField(max_length=200,
#             db_index=True)
    
#     slug = models.SlugField(max_length=200,
#             unique=True)

#     class Meta:
#         ordering = ('name',)
#         verbose_name = 'subcategory'
#         verbose_name_plural = 'subcategories'
#     def __str__(self):
#         return self.name

#     def get_absolute_url(self):
#         return reverse('product:product_list_by_category',
#                         args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category,
        related_name='products',
        on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    subtitle = models.CharField(max_length=200,blank=True,null=True)
    slug = models.SlugField(max_length=200, db_index=True)
    # image = models.ImageField(upload_to='products/%Y/%m/%d',
    #     blank=True)
    image1 = models.URLField(max_length=200,blank=True,null=True)
    image2 = models.URLField(max_length=200,blank=True,null=True)
    image3 = models.URLField(max_length=200,blank=True,null=True)
    image4 = models.URLField(max_length=200,blank=True,null=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product:product_detail',
                        args=[self.id, self.slug])



class Wishlist(models.Model):
    product = models.ForeignKey(Product,
        related_name='products',
        on_delete=models.CASCADE)
    watchuser  =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="wuser")