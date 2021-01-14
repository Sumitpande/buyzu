from celery import Celery, shared_task
from django.core.mail import send_mail
from celery.decorators import task
from .models import Order
from django.conf import settings
@task
def order_created(order_id):
    """
    Task to send an e-mail notification when an order is
    successfully created.
    """
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['2018bit051@sggs.ac.in',]
    send_mail( subject, message, email_from, recipient_list )
    order = Order.objects.get(id=order_id)
    print("----------",order_id)
    subject =   f'Order no. {order.id}'
    message =   f'Dear {order.first_name},\n\n' \
                f'You have successfully placed an order.' \
                f'Your order ID is {order.id}.'
    mail_sent = send_mail(subject,
                message,
                settings.EMAIL_HOST_USER,
                ['2018bit051@sggs.ac.in',])
    return mail_sent