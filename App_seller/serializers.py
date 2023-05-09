from rest_framework import serializers
from App_seller.models import *
from App_login.serializers import UserSerializers


class SalesmanProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesmanProfile
        fields = ['employee_id', 'nid', 'photo', 'NID_front_photo', 'NID_back_photo', 'permanent_address',
                  'present_address', 'salary', 'personal_contact', 'emergency_contact', 'is_active', 'joining_date']

        extra_kwargs = {
            "employee_id": {"read_only": True},
            "salary": {"read_only": True},
        }

    def create(self, validated_data):
        user = self.context['request'].user
        profile = SalesmanProfile(user=user, **validated_data)
        profile.save()
        return profile


class CustomerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerProfile
        fields = [
            'id',
            'name',
            'phone_number',
            'get_total_price',
            'get_total_order',
        ]

        extra_kwargs = {
            'get_total_price': {'read_only': True},
            'get_total_order': {'read_only': True}
        }


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItemModel
        fields = ['id',
                  'seller',
                  'product',
                  'quantity',
                  'created_at',
                  'updated_at',
                  'sold',
                  'get_total',
                  'get_total_purchased_price',
                  'get_product_name',
                  'get_product_strength',
                  'get_total_quantity',
                  ]

        extra_kwargs = {
            'get_total': {'read_only': True},
            'get_total_purchased_price': {'read_only': True},
            'get_product_name': {'read_only': True},
            'get_product_strength': {'read_only': True},
            'get_total_quantity': {'read_only': True}
        }


class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = OrderModel
        fields = [
            "id",
            "seller",
            "customer",
            "items",
            "total_price",
            "discount",
            "payment_method",
            "created_at",
            "updated_at",
            "get_customer_name",
            "get_customer_phone",
            "get_seller_name",
            "get_total_profit"
        ]

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = OrderModel.objects.create(**validated_data)

        for item_data in items_data:
            CartItemModel.objects.create(order=order, **item_data)

        return order


class MonthlySalesSerializer(serializers.Serializer):
    month = serializers.CharField()
    total_sell = serializers.DecimalField(max_digits=10, decimal_places=2)


class PaymentMethodSerializer(serializers.Serializer):
    payment_method = serializers.CharField()
    total_orders = serializers.IntegerField()


class SoldProductSerializer(serializers.Serializer):
    product_name = serializers.CharField()
    total_amount_sold = serializers.DecimalField(max_digits=10, decimal_places=2)


class OrderStatsSerializer(serializers.Serializer):
    month = serializers.CharField()
    no_of_sales = serializers.IntegerField()


class StockAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockAlertModel
        fields = '__all__'
