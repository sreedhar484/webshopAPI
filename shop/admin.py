from django.contrib import admin
from .models import Product,Inventory,Order,OrderItem
# Register your models here.
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(OrderItem)