from rest_framework import serializers
from .models import Category, SubCategory, Brand, Shelf, ProductModel, ProductConsumptionTypeModel, MedicineDetails
import re


# Category Serializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


# SubCategory Serializer
class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'


# Brand Serializer
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


# Shelf Serializer
class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = '__all__'


class ProductConsumptionTypeModelSerializers(serializers.ModelSerializer):
    class Meta:
        model = ProductConsumptionTypeModel
        fields = ['type_name']


# ProductModel Serializer
class ProductModelSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='get_category')
    sub_category = serializers.CharField(source='get_sub_category')
    brand = serializers.CharField(source='get_brand')
    shelf = serializers.CharField(source='get_shelf')
    type = serializers.CharField(source='get_consumption_type')

    class Meta:
        model = ProductModel
        fields = '__all__'

    def create(self, validated_data):
        category_name = validated_data.pop('get_category')
        sub_category_name = validated_data.pop('get_sub_category')
        brand_name = validated_data.pop('get_brand')
        shelf_number = validated_data.pop('get_shelf')
        consump_type = validated_data.pop('get_consumption_type')

        print(shelf_number)

        shelf_pattern = r"Shelf:\s+(\d+)"
        row_pattern = r"Row:\s+(\d+)"
        column_pattern = r"Column:\s+(\d+)"

        shelf_no = re.search(shelf_pattern, shelf_number).group(1)
        row_no = re.search(row_pattern, shelf_number).group(1)
        column_no = re.search(column_pattern, shelf_number).group(1)

        print(f"Shelf number: {shelf_no}")
        print(f"Row number: {row_no}")
        print(f"Column number: {column_no}")

        category = Category.objects.get(name=category_name)
        sub_category = SubCategory.objects.get(name=sub_category_name)
        brand = Brand.objects.get(name=brand_name)
        shelf = Shelf.objects.get(number=shelf_no, row=row_no, column=column_no)
        type = ProductConsumptionTypeModel.objects.get(type_name=consump_type)

        product_model = ProductModel.objects.create(
            category=category,
            sub_category=sub_category,
            brand=brand,
            shelf=shelf,
            type=type,
            **validated_data
        )

        return product_model

    def update(self, instance, validated_data):
        shelf_data = validated_data.pop('shelf', None)

        if shelf_data:
            shelf = Shelf.objects.create(**shelf_data)
            instance.shelf = shelf

        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()
        return instance


class MedicineDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineDetails
        fields = '__all__'
