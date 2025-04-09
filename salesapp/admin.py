from django.contrib import admin
from salesapp.models import Order,OrderItem,User,Product
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    inlines = [
        OrderItemInline
    ]

admin.site.register(Order,OrderAdmin)
admin.site.register(User)
admin.site.register(Product)