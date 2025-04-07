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
from rest_framework.permissions import IsAuthenticated,IsAdminUser,AllowAny
from .tasks import schedule_order
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
    queryset = Product.objects.all().order_by('created_at')[:250]
    serializer_class = ProductSerializer
    filterset_class = ProductFilter
    filter_backends = [ 
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
        
    ]

    search_fields = ['prod_name','description']
    ordering_fields = ['prod_name','price','stock']
    pagination_class = CustomPagination
    
    def get_permissions(self):
        self.permission_classes = [AllowAny]    
        if self.request.method == 'POST':
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()
    
class Product_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_url_kwarg = 'id'

    def get_permissions(self):
        self.permission_classes = [AllowAny]
        if self.request.method in ['PUT','PATCH','DELETE']:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [AllowAny]
    pagination_class = None
    filterset_class = OrderFilter
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter]
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user) # Saves
    
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