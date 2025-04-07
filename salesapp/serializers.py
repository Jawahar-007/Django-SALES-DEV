from rest_framework import serializers 
from .models import Product,Order,OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','prod_name','description','price','stock')

    def validate_price(self, value):
        if value <=0:
            raise serializers.ValidationError("Price entered be greater than zero")
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.prod_name')
    product_price = serializers.DecimalField(max_digits=10,decimal_places=2,source='product.price')
    class Meta:
        model = OrderItem
        fields = ('product_name','product_price','quantity','item_subtotal')

class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product','quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True)
    def create(self,validated_data):
        orderitem_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)

        for item in orderitem_data:
            OrderItem.objects.create(order=order,**item) # associate each orderItem with order created above
                                                         # and take orderitem data and split into keyword args
        return order
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
    class Meta:
        model = Order
        fields = ('order_id','user','status','items')
        extra_kwargs = {
            'user': {'read_only':True}  # set user fields as read_only
        }

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.UUIDField(read_only = True)
    items = OrderItemSerializer(many=True,read_only = True)
    total_price = serializers.SerializerMethodField(method_name='total')

    def total(self,obj):  
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)
    
    class Meta:
        model = Order
        fields = ('order_id','created_at','user','status','items','total_price')



class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many = True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()