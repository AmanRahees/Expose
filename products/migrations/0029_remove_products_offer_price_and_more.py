# Generated by Django 4.1.3 on 2022-12-01 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0028_delete_productoffer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='offer_price',
        ),
        migrations.AddField(
            model_name='productattribute',
            name='product_offer',
            field=models.IntegerField(default=0),
        ),
    ]
