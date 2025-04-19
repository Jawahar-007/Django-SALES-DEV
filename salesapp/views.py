from .models import Product,Order,OrderItem,Customer
from .serializers import ProductSerializer,OrderItemSerializer,OrderSerializer,ProductInfoSerializer,OrderCreateSerializer
from .filters import ProductFilter,OrderFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics,viewsets
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Max
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie,vary_on_headers
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .tasks import send_order_confirmation_email
from uuid import UUID 
from .paginations import CustomPagination
from rest_framework.decorators import action


# class Product_list(APIView):
#     def get(self, request):
#         prod = Product.objects.all()
#         serializer = ProductSerializer(prod,many=True)
#         return Response(serializer.data)
    
#     def post(self, request):
#         serializer = ProductSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Product_list(generics.ListCreateAPIView):
    # queryset = Product.objects.all().order_by('created_at')[:250]
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [ 
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter, 
    ]

    search_fields = ['prod_name','description']
    ordering_fields = ['prod_name','price','stock']
    pagination_class = None
    throttle_scope = 'products'
    
    @method_decorator(cache_page(60 * 15,key_prefix='product_list'))
    def list(self,request,*args,**kwargs):# don't goto db , takes from cache
        return super().list(request,*args,**kwargs)
    
    def get_queryset(self):  # get db objects for list view from db
        import time
        time.sleep(2)
        qs = Product.objects.all().order_by('created_at')
        return qs
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]    
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
class Product_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'product_id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    throttle_scope = 'orders'
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    
    @method_decorator(cache_page(60 * 15,key_prefix='order_list'))
    @method_decorator(vary_on_headers("Authorisation")) # value changes in header from user req then create a cached response and return response only with matching header 
    def list(self,request,*args,**kwargs):# don't goto db , takes from cache
        return super().list(request,*args,**kwargs)
    
    def perform_create(self, serializer):
        order = serializer.save(user=self.request.user) # Saves
        send_order_confirmation_email(order.order_id,self.request.user.email)
 
        # task = process_order_task.delay({
        # "order_id": order.id,
        # "user_id": order.user.id,
        # "timestamp": str(order.created_at),
        #  })
        # return Response({
        # "order_id": order.id,
        # "task_id": task.id
        # })
    
    def get_serializer_class(self):
        if self.action == 'create' or self.action == 'update':
            return OrderCreateSerializer
        return super().get_serializer_class()
    
    def get_queryset(self):
        qs =  super().get_queryset()  # fetch the data of orders and get the nested data of items 
        if not self.request.user.is_staff:  # User isn't staff then user gets his data filled and mapped within user
            qs = qs.filter(user=self.request.user) 
        return qs
    
    # @action(detail=False,methods=['get'], url_path='user-orders')
    # def user_orders(self,request):
    #     orders = self.get_queryset().filter(user=request.user) # fetch the queryset data of Orders
    #     serializer = self.get_serializer(orders,many=True)     # filters for logged in users
    #     return Response(serializer.data)
# class Order_list(APIView):
#     def get(self,request):
#         ord = Order.objects.all()
#         serializer = OrderSerializer(ord,many=True)
#         return Response(serializer.data)
    
#     def post(self,request):
#         serializer = OrderSerializer(data = request.data)
#         if serializer.is_valid():
#             order = serializer.save()
#             schedule_order.delay(str(order.order_id))
#             return Response( {"message": "Order received, processing in the background.", "order_id": order.order_id},
#                 status=status.HTTP_201_CREATED)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
# class Order_detail(APIView):

#     def get(self,request,order_id):
#         try:
            
#             ord = get_object_or_404(Order,order_id=str(order_id))
#             # ord = get_object_or_404(Order,order_id=order_uuid)
#             serializer = OrderSerializer(ord)
#             return Response(serializer.data)
#         except Order.DoesNotExist:
#             return Response({"error":"Order not found"},status=status.HTTP_404_NOT_FOUND)
    
#     def put(self,request,order_id):
#         ord = get_object_or_404(Order,order_id=str(order_id))
#         serializer = OrderSerializer(ord,data=request.data)
#         if serializer.is_valid():
#             order = serializer.save()
#             schedule_order.delay(str(order.order_id))
#             return Response({"message": "Order received for Updation, processing in the background.", "order_id": order.order_id},serializer.data)
#         return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)

# class TriggerFileCreationView(APIView):
#     def get(self, request):
#         data = {
#             "products": [
#                 {"name": "Phone", "price": 599},
#                 {"name": "Laptop", "price": 999}
#             ]
#         }

#         # Send to Celery for async processing
#         generate_file_from_data.delay(data)

#         return Response({"message": "File generation task triggered."})
    
class Prod_Info_List(APIView):
    def get(self,request):
        products = Product.objects.all()
        serializer = ProductInfoSerializer({
            'products': products,
            'count': len(products),
            'max_price': products.aggregate(max_price = Max('price'))['max_price']
        })
        return Response(serializer.data)

# class UserOrderListAPIView(generics.ListAPIView):
#     queryset = Order.objects.prefetch_related('items__product')
#     serializer_class = OrderSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         qs =  super().get_queryset()
#         return qs.filter(user=self.request.user)