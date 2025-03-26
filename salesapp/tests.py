from django.test import TestCase
from .models import User,Order
from django.urls import reverse
# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1',password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1,total_amount = '33.60')
        Order.objects.create(user=user1,total_amount = '22.86')
        Order.objects.create(user=user2,total_amount = '41.39')
        Order.objects.create(user=user2,total_amount = '19.55')

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders-list'))

        assert response.status_code()
        data = response.json()
        print(data)
        