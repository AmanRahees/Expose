# Generated by Django 4.1.3 on 2022-12-15 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0032_remove_products_product_offer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='size',
        ),
    ]
