# Generated by Django 4.2 on 2023-04-25 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App_products", "0009_category_pharmacology_alter_productmodel_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productmodel",
            name="barcode_id",
            field=models.CharField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
