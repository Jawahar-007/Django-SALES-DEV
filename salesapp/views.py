from .models import Product,Order,OrderItem,Customer
from .serializers import ProductSerializer,OrderItemSerializer,OrderSerializer,ProductInfoSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status,generics
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from django.db.models import Max
from rest_framework.permissions import IsAuthenticated

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
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
class Product_detail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer(queryset)
    lookup_field = 'id'

class Order_list(APIView):
    def get(self,request):
        ord = Order.objects.all()
        serializer = OrderSerializer(ord,many=True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = OrderSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class Order_detail(APIView):

    def get(self,request,pk):
        ord = get_object_or_404(Order,pk=pk)
        serializer = OrderSerializer(ord)
        return Response(serializer.data)
    
    def put(self,request,pk):
        ord = get_object_or_404(Order,pk=pk)
        serializer = OrderSerializer(ord,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def prod_info_list(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products': products,
        'count': len(products),
        'max_price': products.aggregate(max_price = Max('price'))['max_price']
    })
    return Response(serializer.data)

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs =  super().get_queryset()
        return qs.filter(user=self.request.user)