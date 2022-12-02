# Generated by Django 4.1.3 on 2022-12-01 18:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0005_alter_brand_brand_offer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=50, unique=True)),
                ('discount', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)])),
                ('min_value', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('valid_from', models.DateTimeField(auto_now_add=True)),
                ('valid_at', models.DateField()),
                ('active', models.BooleanField(default=False)),
            ],
        ),
    ]
