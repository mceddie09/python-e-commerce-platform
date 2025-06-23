from django.contrib import admin
from .models import User, Product, VendorInfo, BuyerInfo, Order, OrderItem, Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Product)
admin.site.register(VendorInfo)
admin.site.register(BuyerInfo)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
