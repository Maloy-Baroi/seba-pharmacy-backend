# Generated by Django 4.2 on 2023-05-03 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("App_products", "0013_medicinedetails"),
    ]

    operations = [
        migrations.AddField(
            model_name="productmodel",
            name="is_medicine",
            field=models.BooleanField(default=True),
        ),
    ]
