from django.urls import path
from . import views
app_name = 'orders'

urlpatterns = [
    path('create/', views.order_create, name='order_create'),
    # path('orders/', views.orders, name='orders'),
    path('admin/order/<int:order_id>/', views.admin_order_detail,
            name='admin_order_detail'),
    # path('admin/order/<int:order_id>/pdf/',
    #         views.admin_order_pdf,
    #         name='admin_order_pdf'),
    path('list/', views.OrderListView.as_view(), name='orders'),
    path('address/', views.ShippingAddressListView.as_view(), name='address'),
    path('address/add/', views.ShippingAddressCreateView.as_view(), name='address-add'),
    path('address/<int:pk>/', views.ShippingAddressUpdateView.as_view(), name='address-update'),
    path('address/<int:pk>/delete/',views.ShippingAddressDeleteView.as_view(), name='address-delete'),

]