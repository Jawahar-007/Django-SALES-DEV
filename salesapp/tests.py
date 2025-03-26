from django.test import TestCase
from .models import User,Order
from django.urls import reverse
# Create your tests here.
class UserOrderTestCase(TestCase):
    def setUp(self):
        user1 = User.objects.create_user(username='user1',password='test')
        user2 = User.objects.create_user(username='user2', password='test')
        Order.objects.create(user=user1)
        Order.objects.create(user=user1)
        Order.objects.create(user=user2)
        Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_user_orders(self):
        user = User.objects.get(username='user1')
        self.client.force_login(user)
        response = self.client.get(reverse('user-orders-list'))

        assert response.status_code == 200
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders)) # In for order in orders , taking each order from response.data from API
                                                                           # evaluating response users' data assosciated with the user.id such that one user can't see others data 