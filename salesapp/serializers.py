from rest_framework import serializers 
from .models import Product,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','prod_name','description','price','stock',)

    def validate_price(self, value):
        if value <=0:
            raise serializers.ValidationError("Price entered be greater than zero")
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True,read_only = True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self,obj):  
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = ['order_id','created_at','user','customer','status','items','total_price']

class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many = True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()