# Generated by Django 4.1.3 on 2022-11-16 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_remove_products_product_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='products',
            name='stock',
            field=models.IntegerField(default=1),
        ),
    ]