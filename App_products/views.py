import json
from datetime import datetime, timedelta
import re

from django.shortcuts import render
from rest_framework import generics, status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from django.views.decorators.cache import cache_page

from App_products.models import *
from App_products.serializers import *
from App_seller.models import *
import json


# Create your views here.
class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 3


class MedicinesAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(expiry_date__lte=datetime.today()).filter(is_medicine=True).order_by(
            'expiry_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ProductsAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(expiry_date__lte=datetime.today()).filter(is_medicine=False).order_by(
            'expiry_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsAPIView2(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer
    pagination_class = LargeResultsSetPagination

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(expiry_date__lte=datetime.today()).filter(is_medicine=False).order_by(
            'expiry_date')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AllProductsAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().exclude(expiry_date__lte=datetime.today()).order_by('expiry_date')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ImportProductsAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(imported=True).exclude(expiry_date__lte=datetime.today().date())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([permissions.IsAuthenticated])
def productUpdateAPIView(request, pk):
    try:
        product_object = ProductModel.objects.get(pk=pk)
    except product_object.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        shelf_number = request.data['shelf']
        shelf_pattern = r"Shelf:\s+(\d+)"
        row_pattern = r"Row:\s+(\d+)"
        column_pattern = r"Column:\s+(\d+)"

        shelf_no = re.search(shelf_pattern, shelf_number).group(1)
        row_no = re.search(row_pattern, shelf_number).group(1)
        column_no = re.search(column_pattern, shelf_number).group(1)

        my_shelf = Shelf.objects.get(number=shelf_no, row=row_no, column=column_no)
        product_object.shelf = my_shelf
    except:
        pass

    product_object.bought_price = request.data['bought_price']
    product_object.minimum_selling_price = request.data['minimum_selling_price']
    product_object.quantity = request.data['quantity']
    product_object.minimum_alert_quantity = request.data['minimum_alert_quantity']
    product_object.expiry_date = request.data['expiry_date']

    product_object.save()

    if int(product_object.quantity) > int(product_object.minimum_alert_quantity):
        stoct_alart = StockAlertModel.objects.filter(product=product_object)
        if stoct_alart.exists():
            stoct_alart[0].delete()

    return Response({
        'success': f"`{product_object.name}` is successfully updated",
    }, status=status.HTTP_200_OK)


class AlMostExpiryProductsAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get(self, request, *args, **kwargs):
        today = datetime.today().date()
        ten_days_later = today + timedelta(days=15)
        queryset = self.get_queryset().filter(expiry_date__range=[today, ten_days_later])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ExpiredProductsAPIView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated, ]
    queryset = ProductModel.objects.all()
    serializer_class = ProductModelSerializer

    def get(self, request, *args, **kwargs):
        today = datetime.today().date()
        queryset = self.get_queryset().filter(expiry_date__lt=today)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class SubCategoryListAPIView(generics.ListAPIView):
    queryset = SubCategory.objects.all()
    serializer_class = SubCategorySerializer
    permission_classes = [permissions.IsAuthenticated]


class BrandListAPIView(generics.ListAPIView):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [permissions.IsAuthenticated]


class ShelfListAPIView(generics.ListAPIView):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductConsumptionTypeAPIView(generics.ListCreateAPIView):
    queryset = ProductConsumptionTypeModel.objects.all()
    serializer_class = ProductConsumptionTypeModelSerializers
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        name = request.data['type_name']
        serializer = ProductConsumptionTypeModelSerializers(data={'type_name': name})

        if serializer.is_valid():
            serializer.save()
            return Response({"success": "Successfully saved", "data": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineDetailsCreateAPIView(generics.CreateAPIView):
    serializer_class = MedicineDetailsSerializer


class MedicineDetailsListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = MedicineDetailsSerializer
    queryset = MedicineDetails.objects.all()

    def post(self, request, *args, **kwargs):
        medicine_name = request.data.get('medicine_name', '').lower().strip()
        words = medicine_name.split()

        matching_medicines = []
        num_matching_medicines = 0

        for word in words:
            if num_matching_medicines >= 20:
                break

            # Get the matching medicines for the current word
            medicines = MedicineDetails.objects.filter(product_name__istartswith=word)[:20]

            # Add the matching medicines to the list
            matching_medicines.extend(medicines)
            num_matching_medicines += len(medicines)

        serializer = self.serializer_class(matching_medicines[:20], many=True)
        return Response(serializer.data)


# from difflib import SequenceMatcher
#
# class MedicineDetailsListCreateAPIView(generics.ListCreateAPIView):
#     serializer_class = MedicineDetailsSerializer
#     queryset = MedicineDetails.objects.all()
#
#     def post(self, request, *args, **kwargs):
#         medicine_name = request.data['medicine_name']
#         medicines = MedicineDetails.objects.all()
#         similar_medicines = []
#         for medicine in medicines:
#             similarity_score = SequenceMatcher(None, medicine_name, medicine.product_name).ratio()
#             similar_medicines.append((medicine, similarity_score))
#         similar_medicines = sorted(similar_medicines, key=lambda x: x[1], reverse=True)
#         similar_medicines = [m[0] for m in similar_medicines][:20]
#         serializer = MedicineDetailsSerializer(similar_medicines, many=True)
#         return Response(serializer.data)


class MedicineDetailsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicineDetailsSerializer
    queryset = MedicineDetails.objects.all()


@api_view(['DELETE'])
def allMedicineDelete(request):
    query = MedicineDetails.objects.all()
    for i in query:
        i.delete()
    return Response({"success": "Successfully Deleted!!!"})
