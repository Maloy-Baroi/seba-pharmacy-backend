from django.contrib import admin
from App_products.models import *

# Register your models here.
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Shelf)
admin.site.register(Brand)
admin.site.register(ProductModel)
admin.site.register(ProductConsumptionTypeModel)
admin.site.register(MedicineDetails)
