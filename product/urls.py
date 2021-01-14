
from django.contrib import admin
from django.urls import path
from . import views

app_name = 'product'

urlpatterns = [
    path('', views.product_list, name='product_list'),


    
    
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),

    path('<slug:category_slug>/', views.product_list,
    name='product_list_by_category'),


    path("wishlist",views.wishlist, name="wishlist"),
    path("wishlist/add/<int:id>",views.addToWishlist, name="addToWishlist"),
    path("wishlist/remove/<int:id>",views.removeFromWl, name="removeFromWl"),


    


]
