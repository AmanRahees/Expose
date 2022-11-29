# Generated by Django 4.1.3 on 2022-11-17 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0018_alter_products_product_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='product_name',
            field=models.ForeignKey(blank=True, null=True,  on_delete=django.db.models.deletion.CASCADE, related_name='product', to='products.productattribute'),
        ),
    ]
