from celery import shared_task
import time
from .models import Order

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