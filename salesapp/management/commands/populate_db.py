import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import lorem_ipsum

from salesapp.models import Customer,Product,Order,OrderItem

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **options):
        # user = User.objects.filter(username='postgres').first()
        # if not user:
        #     user = User.objects.(username='postgres',email='gg')

        customer, _ = Customer.objects.get_or_create(
            name='Postgres Customer', email='postgres@example.com'
        )


        # Fetch from DB
        products = list(Product.objects.all())
        
        if not products:
            self.stdout.write(self.style.ERROR("No products found in the database."))
            return
        
        for _ in range(3):
            order = Order.objects.create(customer=customer)
            for product in random.sample(products,min(2 , len(products))):
                OrderItem.objects.create(order = order, product=product ,quantity=random.randint(1,3),price = product.price)
        self.stdout.write(self.style.SUCCESS("Successfully populated database!"))