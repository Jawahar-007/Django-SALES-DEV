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
from salesapp.views import Product_list,Product_detail,Prod_Info_List,OrderViewSet
from salesapp import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView,SpectacularRedocView,SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),

    path('products/',Product_list.as_view(),name='product-list'),
    path('products/<int:product_id>/',Product_detail.as_view(),name='product-detail'),
    # path('orders/',Order_list.as_view(),name='order-list'),
    # path('order/<uuid:order_id>/',Order_detail.as_view(),name='order-detail'),
    path('products/info/',Prod_Info_List.as_view(),name='product-info-list'),
    # path('user-orders/',views.UserOrderListAPIView.as_view(),name='user-orders-list'),
    path('trigger-file/', views.TriggerFileCreationView.as_view(), name='trigger-file'),

    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/schema/',SpectacularAPIView.as_view(),name='schema'),
    #Optional UI: 
    path('api/schema/swagger-ui/',SpectacularSwaggerView.as_view(url_name='schema'),name='swagger-ui'),
    path('api/schema/redoc/',SpectacularRedocView.as_view(url_name='schema'),name='redoc'),
]

router = DefaultRouter()
router.register('orders',views.OrderViewSet)
urlpatterns+= router.urls