# Generated by Django 4.1.3 on 2022-12-03 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0029_remove_products_offer_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productattribute',
            name='product_offer',
        ),
        migrations.AddField(
            model_name='products',
            name='product_offer',
            field=models.IntegerField(default=0),
        ),
    ]
