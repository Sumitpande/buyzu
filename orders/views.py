from django.shortcuts import render,redirect

# Create your views here.
from .models import OrderItem
from .forms import *
from cart.cart import Cart
from django.urls import reverse
from .tasks import order_created

from coupons.forms import CouponApplyForm
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from .models import Order
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
# import weasyprint
# @staff_member_required
# def admin_order_pdf(request, order_id):
#     order = get_object_or_404(Order, id=order_id)
#     html = render_to_string('orders/order/pdf.html',
#     {'order': order})
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = f'filename=order_{order.id}.pdf'
#     weasyprint.HTML(string=html).write_pdf(response,
#     stylesheets=[weasyprint.CSS(
#     settings.STATIC_ROOT + 'css/pdf.css')])
#     return response
@login_required
@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request,
    'orders/detail.html',
    {'order': order})


@login_required
def order_create(request):
    cart = Cart(request)
    addrs = ShippingAddress.objects.filter(user=request.user)
    addrs_form = AddressForm(user=request.user)
    if request.method == 'POST':
        print(request.POST)
        if 'shipping_address' in request.POST:
            form = AddressForm(request.POST)
            
        else:
            form = OrderCreateForm(request.POST)
        if form.is_valid():
            
            if 'shipping_address' in request.POST:
                
                aid = int(request.POST['shipping_address'])
                
                ship_addr = ShippingAddress.objects.get(id=aid)
                order = Order(
                    first_name=ship_addr.first_name,
                    last_name=ship_addr.last_name,
                    mobile=ship_addr.mobile,
                    email=ship_addr.user.email,
                    state=ship_addr.state,
                    address=ship_addr.address,
                    postal_code=ship_addr.postal_code,
                    city=ship_addr.city,
            
                )
            else:
                order = form.save(commit=False)
                
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity'])
            # clear the cart
            cart.clear()
            # launch asynchronous task
            
            order_created.delay(order.id)
            # set the order in the session
            request.session['order_id'] = order.id
            # redirect for payment
            
            return redirect(reverse('payment:process'))

            return render(request,
                'orders/created.html',
                {'order': order})
    else:
        form = OrderCreateForm()
        # coupon_apply_form = CouponApplyForm()

    return render(request,
        'orders/create.html',
        {'cart': cart,
         'form': form,
        #  'coupon_apply_form':coupon_apply_form,
         'addrs':addrs,
         'addrs_form':addrs_form,
         })

from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from django.views.generic import ListView

class OrderListView(ListView):
    model = Order

    def get_queryset(self):
        queryset = Order.objects.filter(user=self.request.user)

        return queryset


class ShippingAddressListView(ListView):
    model = ShippingAddress

    def get_queryset(self):
        queryset = ShippingAddress.objects.filter(user=self.request.user)
        return queryset

class ShippingAddressCreateView(CreateView):
    model = ShippingAddress
    fields = ['first_name', 'last_name', 'mobile', 'postal_code', 'address', 'city', 'state', 'country' ,'default']
    success_url = reverse_lazy('orders:address')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class ShippingAddressUpdateView(UpdateView):
    model = ShippingAddress
    fields = ['first_name', 'last_name', 'mobile', 'postal_code', 'address', 'city', 'state', 'country','default',]
    success_url = reverse_lazy('orders:address')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class ShippingAddressDeleteView(DeleteView):
    model = ShippingAddress
    success_url = reverse_lazy('orders:address')