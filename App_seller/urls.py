from django.urls import path
from .views import *

app_name = 'App_seller'

urlpatterns = [
    path('cart/', cart_view, name='cart-view'),
    path('cart-list/', CartListAPIView.as_view(), name='cart-list'),
    path('cart-delete/', cart_delete, name='cart-delete'),
    path('single-order-view/<int:id>/', SingleOrderAPIView.as_view(), name='single-order-view'),
    path('order-list/', OrderListAPIView.as_view(), name='order-list'),
    path('order/', order_view, name='order-view'),
    path('monthly-sales/', MonthlySalesAPIView.as_view(), name='monthly-sales'),
    path('order-stats/', OrderStatsView.as_view(), name='order-stats'),
    path('sold-products/', SoldProductView.as_view(), name='sold-products'),
    path('payment-methods/', PaymentMethodView.as_view(), name='payment-methods'),
    path('stock-alerts/', StockAlertListAPIView.as_view(), name='stock-alerts'),
    path('customer-profiles/', CustomerProfileListAPIView.as_view(), name='customer-profiles'),
    path('near-expiry-products/', NearExpiryProductListView.as_view(), name='near-expiry-products'),
    path('stock-less-than-minimum-quantity/', LowStockProductAPIView.as_view(), name='stock-less-than-minimum-quantity'),
    path('purchased-products/', PurchasedProductAPIListView.as_view(), name='product-list'),
    path('customer-report/', CustomerReportListAPIView.as_view(), name='customer-report'),
    path('salesman-profile/', SalesmanProfileAPIView.as_view(), name='salesman-profile'),
    path('salesman-profile-create/', CreateSalesmanProfileAPIView.as_view(), name='salesman-profile-create'),

]
