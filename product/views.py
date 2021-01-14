from django.shortcuts import render
from .models import *
from cart.forms import *
from .recommender import Recommender
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

# Create your views here.
def product_list(request, category_slug=None):

    if request.user.is_authenticated:
        l = Wishlist.objects.filter(watchuser = request.user).values('product')
        x = [d['product'] for d in l if 'product' in d]
        print(x)
        count = Wishlist.objects.filter(watchuser = request.user).values('product').count()
    else:
        x=[]

    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        print(category,"ss")
        products = products.filter(category=category)

    return render(request,
            'product/productList.html',
            {   'category': category,
                'categories': categories,
                'products': products,
                'wlist':x ,
                })

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
                id=id,
                slug=slug,
                available=True)
    cart_product_form = CartAddProductForm()
    r = Recommender()
    recommended_products = r.suggest_products_for([product], 4)
    return render(request,
        'product/detail.html',
        {'product': product,
        'cart_product_form': cart_product_form ,
        'recommended_products': recommended_products
        })







@login_required
def wishlist(request):

    wl = Wishlist.objects.filter(watchuser = request.user)
    print(wl)
    print(Wishlist.objects.filter(watchuser = request.user).values('product').count())


    return render(request, "product/wishlist.html", {
        'count':Wishlist.objects.filter(watchuser = request.user).values('product').count(),
        'products':wl,
        
        

    })

from django.core.mail import send_mail
from django.conf import settings
@login_required
def addToWishlist(request,id):
    items  = Wishlist() 

    items.product = Product(id = id)
    items.watchuser = request.user
    items.save()
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['2018bit051@sggs.ac.in',]
    send_mail( subject, message, email_from, recipient_list )
    
    
    return HttpResponseRedirect(reverse("product:wishlist"))

    

@login_required
def removeFromWl(request,id):
    l = Wishlist(id = id)
    l.delete()
 

    return HttpResponseRedirect(reverse("product:product_list"))
    
