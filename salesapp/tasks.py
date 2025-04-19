from celery import shared_task
import time,os,json
from .models import Order
from datetime import datetime
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_order_confirmation_email(order_id,user_email):
    subject = 'Order Confirmation'
    message = f"Your Order with ID {order_id} has been received and processed."
    return send_mail(subject,message,settings.DEFAULT_FROM_EMAIL,{user_email})