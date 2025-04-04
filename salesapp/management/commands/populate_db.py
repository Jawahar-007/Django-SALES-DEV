import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import lorem_ipsum
from salesapp.models import User, Customer, Product, Order, OrderItem

class Command(BaseCommand):
    help = 'Creates application data'

    def handle(self, *args, **options):
        # Get or create the superuser
        user, _ = User.objects.get_or_create(username='postgre', defaults={'password': 'test'})
        
        # Ensure a customer exists
        customer, _ = Customer.objects.get_or_create(
            name='Postgres Customer',
            email='postgres@example.com'
        )

        products = [
            Product(prod_name="Crayons", description=lorem_ipsum.paragraph(), price=Decimal('40'), stock=4),
            Product(prod_name="Coffee Machine", description=lorem_ipsum.paragraph(), price=Decimal('67000'), stock=6),
            Product(prod_name="GLUCOVITA BOLTS - Small", description=lorem_ipsum.paragraph(), price=Decimal('15'), stock=11),
            Product(prod_name="Ph-E08 Pro Camera", description=lorem_ipsum.paragraph(), price=Decimal('29510'), stock=2),
            Product(prod_name="Cotton Glove", description=lorem_ipsum.paragraph(), price=Decimal('275'), stock=4),
            Product(prod_name="Watch", description=lorem_ipsum.paragraph(), price=Decimal('500.05'), stock=0),
        ]

        # Fetch products from DB
        Product.objects.bulk_create(products)
        products = list(Product.objects.all())
        if not products:
            self.stdout.write(self.style.ERROR("No products found in the database."))
            return
        
        # Create orders
        for _ in range(3):
            order = Order.objects.create(
                user=user,
                customer=customer,
                status=Order.StatusChoices.PENDING  # Ensure all required fields are included
            )

            # Create order items
            for product in random.sample(products, min(2, len(products))):
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=random.randint(1, 3),
                    price=product.price
                )

        self.stdout.write(self.style.SUCCESS("Successfully populated database!"))
