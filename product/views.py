from django.shortcuts import render
from .models import *
from cart.forms import *
# from .recommender import Recommender
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.db.models import Q
from .forms import FilterForm, Search
from django.views.generic.edit import FormMixin
from .filters import ProductFilter

def home(request):
    categories = Category.objects.all()

    return render(request, 'product/home.html', {'categories': categories})
class ProductListView(ListView, FormMixin):
    form_class = FilterForm
    model = Product
    template_name = 'product/productList.html'
    context_object_name = 'products'
    # filterset_class = ProductFilter

    
    # paginate_by = 100  # if pagination is desired

    def get(self, request, *args, **kwargs):
        # self.get_context_data(**kwargs)
        self.get_queryset(self, *args, **kwargs)

        return super().get(request, *args, **kwargs)

    def get_queryset(self, *args, **kwargs):
        
        slug = self.kwargs.get('slug','')
        qs = product_filter(self.request)
        attr = self.request.GET
           
        if 'Sort_by' in attr.keys():
            if attr['Sort_by'] == '0':
                print(len(qs.order_by('-price')))
                qs = qs.order_by('-price')
            else:
                print(len(qs.order_by('price')))
                qs =  qs.order_by('price')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            return qs.filter(category=category)
            # return  Product.objects.filter(category=category)
        elif qs:

            return qs
        

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categories = Category.objects.all()
        slug = self.kwargs.get('slug','')
        if slug:
            category = get_object_or_404(Category, slug=slug)
            context['category'] = category
        
        context['categories'] = categories
        if self.request.user.is_authenticated:

            wishlist = Product.objects.my_wishlist(self.request.user).values('id')
            wlist = [int(w['id']) for w in wishlist]
            context['wishlist'] = wlist
        context['form'] = FilterForm()
        context['sort_form'] = Search()
        if self.request.method == 'GET':
            attr = self.request.GET
           
            if 'Sort_by' in attr.keys():
                context['sort_form'] = Search(self.request.GET or None)
                # if attr['Sort_by'] == '0':
                #     context['products'] = self.get_queryset().order_by('-price')
                # else:
                #     context['products'] = self.get_queryset().order_by('price')
            # context['attr'] = attr
            context['form'] = FilterForm(self.request.GET or None)
        
        return context

def product_filter(request):
    f = ProductFilter(request.GET, queryset=Product.objects.all())
    
        
    return f.qs
   
class ProductDetailView(DetailView):

    model = Product
    template_name = "product/detail.html"
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart_product_form'] =  CartAddProductForm()
        product=context['product']
        # r = Recommender()
        products=Product.objects.filter(category=product.category,available=True)
        # recommended_products = r.suggest_products_for([product], 4)
        recommended_products = []
        context['recommended_products'] =  recommended_products
        context['products'] =  products
        
        return context




@login_required
def wishlist(request):

    wl = Product.objects.my_wishlist(request.user)
    wishlist = Product.objects.my_wishlist(request.user).values('id')
    wlist = [int(w['id']) for w in wishlist]
  
    return render(request, "product/wishlist.html", {
        # 'count':Wishlist.objects.filter(watchuser = request.user).values('product').count(),
        'products':wl,
        'wishlist':wlist,
        

    })

from django.core.mail import send_mail
from django.conf import settings
@login_required
def addToWishlist(request,id):
    items  = Wishlist() 

    items.product = Product.objects.get(id = id)
    items.watchuser = request.user
    items.save()
    # subject = 'Thank you for registering to our site'
    # message = ' it  means a world to us '
    # email_from = settings.EMAIL_HOST_USER
    # recipient_list = ['2018bit051@sggs.ac.in',]
    # send_mail( subject, message, email_from, recipient_list )
    
    
    return HttpResponseRedirect(reverse("product:wishList"))

    

@login_required
def removeFromWl(request,id):
    p=Product.objects.get(id=id)
    l = Wishlist.objects.get(product = p)
    l.delete()
 

    return HttpResponseRedirect(reverse("product:product_list"))
    
def search(request, query=None):
    q = Q(category__icontains=query) | Q(name__icontains=query) | Q(subtitle__icontains=query) | Q(slug__icontains=query) | Q(price__icontains=query) 
    products = Product.objects.filter(q)
    return HttpResponseRedirect(reverse("product:product_list"))