# Generated by Django 4.1.3 on 2022-11-20 23:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0024_alter_productimage_product'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('address_2', models.CharField(blank=True, max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('district', models.CharField(max_length=256)),
                ('state', models.CharField(max_length=256)),
                ('pincode', models.CharField(max_length=6)),
                ('order_note', models.CharField(blank=True, max_length=100)),
                ('order_total', models.FloatField()),
                ('tax', models.FloatField()),
                ('payment_method', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(choices=[('New', 'New'), ('New', 'New'), ('New', 'New'), ('Cancelled', 'Cancelled')], default='New', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('amount_paid', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.products')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]