from django.contrib import admin
from django.urls import path
from . import views
from django_filters.views import FilterView
from django.views.generic import TemplateView
from .filters import ProductFilter
app_name = 'product'

urlpatterns = [
    path('', views.home, name='home'),
    path('shop/', views.ProductListView.as_view(), name='product_list'),
    # path('filter/', FilterView.as_view(filterset_class=ProductFilter,template_name='product/test.html'), name='search'),
    
    path('<int:id>/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),
    path("wishlist/",views.wishlist, name="wishList"),
    path("<int:id>/add-to-wishlist",views.addToWishlist, name="add-to-wishlist"),
    path("<int:id>/remove-from-wishlist",views.removeFromWl, name="remove-from-wishlist"),
    path('<slug:slug>/', views.ProductListView.as_view(), name='product_list_by_category'),
    # path('<str:query>/', views.search, name='search'),

    
    


    


]
