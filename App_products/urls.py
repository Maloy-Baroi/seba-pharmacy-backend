from django.urls import path
from App_products.views import *

app_name = "App_products"

urlpatterns = [
    path('products-list/', ProductsAPIView.as_view(), name="products-list"),
    path('medicine-list/', MedicinesAPIView.as_view(), name="medicine-list"),
    path('all-products-list/', AllProductsAPIView.as_view(), name="all-products-list"),
    path('medicines-info/', MedicineDetailsListCreateAPIView.as_view(), name="medicine-info"),
    path('medicines-create/', MedicineDetailsCreateAPIView.as_view(), name="medicine-create"),
    path('all-medicine-delete/', allMedicineDelete, name="all-medicine-delete"),
    path('imported-products/', ImportProductsAPIView.as_view(), name="imported-product-list"),
    path('update-product/<int:pk>/', productUpdateAPIView, name="product-update"),
    path('almost-expiry-products/', AlMostExpiryProductsAPIView.as_view(), name="almost-expiry-product-list"),
    path('expired-products/', ExpiredProductsAPIView.as_view(), name="expired-product-list"),
    path('categories/', CategoryListAPIView.as_view(), name="categories"),
    path('sub-categories/', SubCategoryListAPIView.as_view(), name="sub-categories"),
    path('brand/', BrandListAPIView.as_view(), name="brand"),
    path('all-shelf/', ShelfListAPIView.as_view(), name="all-shelf"),
    path('product-consumption-types/', ProductConsumptionTypeAPIView.as_view(), name='product_consumption_types'),
]
