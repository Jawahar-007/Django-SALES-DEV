from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User,Order,Product
from django.urls import reverse
from rest_framework import status
# Create your tests here.
class UserOrderTestCase(APITestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin',password='admintest')
        self.normal_user = User.objects.create_user(username='user', password='test')
        self.product = Product.objects.create(
            name= "Test Product",
            description = "Test Description",
            price = 9.89,
            stock = 10
        )
        self.url = reverse('product-detail',kwargs={'product_id': self.product.pk})
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
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED) # Due to is_authenticated permission make sure
                                                    # endpoint remains block off for unauthenticated users 