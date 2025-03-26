from django.test import TestCase
from .models import User,Order
from django.urls import reverse
from rest_framework import status
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

        assert response.status_code == status.HTTP_200_OK
        orders = response.json()
        self.assertTrue(all(order['user'] == user.id for order in orders)) # In for order in orders , taking each order from response.data from API
                                                                           # evaluating response users' data assosciated with the user.id such that one user can't see others data 

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user-orders-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) # Due to is_authenticated permission make sure
                                                    # endpoint remains block off for unauthenticated users 