# Generated by Django 4.1.3 on 2022-11-16 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_cartitem_cart_remove_cartitem_cart_product_and_more'),
        ('products', '0008_productattribute'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Variation',
        ),
    ]