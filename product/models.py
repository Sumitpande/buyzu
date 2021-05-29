from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.
BROWN, YELLOW, BLACK, PINK, GREY, BLUE = range(6)
NEW, USED, COLLECTIBLE, RENEWED = range(4)
SMALL, MEDIUM, LARGE, EXTRA_LARGE, DOUBLE_LARGE = range(5)
COLORS_CHOICES = [
    (BROWN, 'Brown'),
    (YELLOW, 'Yellow'),
    (BLACK, 'Black'),
    (PINK, 'Pink'),
    (GREY, 'Grey'),
    (BLUE, 'Blue'),
]
CONDITION_CHOICES = [
    
    (NEW, 'NEW'),
    (USED, 'USED'),
    (COLLECTIBLE, 'COLLECTIBLE'),
    (RENEWED, 'RENEWED'),
]
SIZE_CHOICES = [
    (SMALL, 'S'),
    (MEDIUM, 'M'),
    (LARGE, 'L'),
    (EXTRA_LARGE, 'XL'),
    (DOUBLE_LARGE, 'XXL'),
]
class Category(models.Model):
    name = models.CharField(max_length=200,
            db_index=True)
    img = models.URLField(max_length=200,blank=True,null=True)
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


class ProductManager(models.Manager):

    def my_wishlist(self, user):
        query = self.filter(myWishList__watchuser=user)
        # query = query.select_related("root", "author", "lastedit_user")
        # query = query.prefetch_related("tag_set")
        return query

    
    

class Product(models.Model):
    objects = ProductManager()

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
    size = models.IntegerField(choices=SIZE_CHOICES,  blank=True,null=True)
    condition = models.IntegerField(choices=CONDITION_CHOICES,  blank=True,null=True)
    color = models.IntegerField(choices=COLORS_CHOICES, blank=True,null=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        index_together = (('id', 'slug'),)
    def __str__(self):
        return self.name

    # def is_wishlisted(self):
    #     # query = self.objects.my_wishlist(self.request.user)
    #     wlist = Product.objects.filter(myWishList__watchuser=self.request.user)
    #     obj = Product.objects.get(id=self.id)
    #     if obj in wlist:
    #         return True
    #     else:
    #         return False

    def get_absolute_url(self):
        return reverse('product:product_detail',
                        args=[self.id, self.slug])
    
    



class Wishlist(models.Model):
    product = models.ForeignKey(Product,
        related_name='myWishList',
        on_delete=models.CASCADE)
    watchuser  =  models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="wuser")
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)