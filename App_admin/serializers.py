from rest_framework import serializers
from App_admin.models import *
from App_login.serializers import UserSerializers


class ShopManagerProfileSerializer(serializers.ModelSerializer):
    user = UserSerializers(read_only=True)
    NID_front_photo = serializers.ImageField()
    NID_back_photo = serializers.ImageField()
    photo = serializers.ImageField()

    class Meta:
        model = ShopManagerProfile
        fields = ('id', 'user', 'employee_id', 'nid', 'NID_front_photo', 'NID_back_photo',
                  'photo', 'permanent_address', 'present_address', 'emergency_contact',
                  'status', 'joining_date')

        extra_kwargs = {
            'employee_id': {'read_only': True},
        }


class TotalProfitByDaySerializer(serializers.Serializer):
    date = serializers.DateField()
    total_profit = serializers.DecimalField(max_digits=10, decimal_places=2)


class MonthlyProfitSerializer(serializers.Serializer):
    month = serializers.DateField(format='%Y-%m')
    total_profit = serializers.DecimalField(max_digits=10, decimal_places=2)

