from celery import shared_task
import time
from .models import Order
from django.conf import settings
from django.core.mail import send_mail

@shared_task(bind=True) # to allow retries
def schedule_order(self,order_id):
    try:
        time.sleep(15)
        order = Order.objects.get(order_id=order_id)
        order.status = Order.StatusChoices.CONFIRMED
        order.save()
        return f"Order {order_id} processed successfully!" 
    except Order.DoesNotExist:
        self.retry(exc=Exception(f"Order ID {order_id} not found"),countdown = 20,max_retries=3)

@shared_task(bind=True)
def send_order_confirmation_email(order_id,user_email):
    subject = 'Order Confirmation'
    message = f"Your Order with ID {order_id} has been received and processed."
    return send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,{user_email})