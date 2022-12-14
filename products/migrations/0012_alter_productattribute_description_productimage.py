# Generated by Django 4.1.3 on 2022-11-17 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0011_alter_products_price_alter_products_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productattribute',
            name='description',
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(max_length=256, upload_to='photos/Category')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.productattribute')),
            ],
        ),
    ]
