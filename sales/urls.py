"""
URL configuration for sales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include,path
from salesapp.views import Product_list,Product_detail,Order_list,Order_detail
from salesapp import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('products/',Product_list.as_view(),name='product-list'),
    path('products/<int:pk>/',Product_detail.as_view(),name='product-detail'),
    path('orders/',Order_list.as_view(),name='order-list'),
    path('order/<int:pk>/',Order_detail.as_view(),name='order-detail'),
    path('products/info/',views.prod_info_list,name='product-info-list'),
    path('user-orders/',views.UserOrderListAPIView.as_view(),name='user-orders-list')
]
