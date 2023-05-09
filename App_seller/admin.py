from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SalesmanProfile)
admin.site.register(CustomerProfile)
admin.site.register(CartItemModel)
admin.site.register(OrderModel)
admin.site.register(StockAlertModel)
