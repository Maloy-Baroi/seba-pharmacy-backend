import json
from datetime import datetime, timedelta
import re

from dateutil.relativedelta import relativedelta
from django.db.models.functions import TruncMonth
from django.utils.timezone import now
from django.shortcuts import render
from django.contrib.auth.models import Group
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView

from App_admin.models import ShopManagerProfile
from App_admin.serializers import ShopManagerProfileSerializer, TotalProfitByDaySerializer, MonthlyProfitSerializer
from App_login.serializers import UserSerializers
from App_products.models import *
from App_products.serializers import *
from App_seller.models import *
from App_seller.serializers import OrderSerializer, SalesmanProfileSerializer
from django.db.models import Sum
from django.utils import timezone


# Create your views here.
class ShopManagerProfileAPIView(generics.CreateAPIView, generics.RetrieveAPIView):
    queryset = ShopManagerProfile.objects.all()
    serializer_class = ShopManagerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            profile = ShopManagerProfile.objects.get(user=request.user)
            serializer = self.serializer_class(profile)
            return Response(serializer.data)
        except ShopManagerProfile.DoesNotExist:
            return Response({'error': 'Profile not found.'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        try:
            profile = ShopManagerProfile.objects.get(user=request.user)
            serializer = self.serializer_class(profile, data=request.data)
        except ShopManagerProfile.DoesNotExist:
            serializer = self.serializer_class(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.serializer_class(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def customer_seller_order_count(request):
    orders = OrderModel.objects.all().count()
    customer = CustomerProfile.objects.all().count()
    users = CustomUser.objects.all()
    seller_group = Group.objects.get(name='seller')

    # Filter the queryset to get the seller group's users
    seller_group_users = users.filter(groups=seller_group)

    print(seller_group_users)

    return Response({
        "totalOrders": orders,
        "totalCustomers": customer,
        "totalSellers": len(seller_group_users),
    }, status=status.HTTP_302_FOUND)


class SellerListAPIView(generics.ListAPIView):
    serializer_class = UserSerializers
    queryset = CustomUser.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        seller_group = Group.objects.get(name='seller')

        # Filter the queryset to get the seller group's users
        seller_group_users = queryset.filter(groups=seller_group)

        return Response(seller_group_users.values(), status=status.HTTP_200_OK)


class OrderListAPIViewForManager(generics.ListAPIView):
    queryset = OrderModel.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(['GET'])
def total_profit_by_day_in_month(request, year, month):
    start_date = timezone.datetime(int(year), int(month), 1)
    end_date = start_date.replace(day=1, month=start_date.month + 1) - timezone.timedelta(days=1)
    orders = OrderModel.objects.filter(created_at__range=(start_date, end_date))

    # aggregate total profit by day
    total_profit_by_day = orders.annotate(date=timezone.functions.TruncDay('created_at')) \
        .values('date') \
        .annotate(total_profit=Sum('total_price') - Sum('items__product__bought_price') * Sum('items__quantity')) \
        .order_by('date')

    # format response
    data = []
    for profit_by_day in total_profit_by_day:
        date = profit_by_day['date'].date()
        serializer = TotalProfitByDaySerializer(data={
            'date': date,
            'total_profit': profit_by_day['total_profit']
        })
        serializer.is_valid()
        data.append(serializer.data)

    return Response(data)


class MonthlyProfitViewAPIView(APIView):
    def get(self, request, format=None):
        six_months_ago = now() - relativedelta(months=6)
        orders = OrderModel.objects.filter(created_at__gte=six_months_ago)
        monthly_profits = orders.annotate(month=TruncMonth('created_at')).values('month').annotate(total_profit=Sum('total_price') - Sum('items__quantity' * 'items__product__bought_price')).order_by('-month')
        serializer = MonthlyProfitSerializer(monthly_profits, many=True)
        return Response(serializer.data)


class ShelfListCreateAPIView(generics.ListCreateAPIView):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer


class CreateBrandAPIView(generics.CreateAPIView):
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class SubCategoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer


class CreateCategoryView(generics.CreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
