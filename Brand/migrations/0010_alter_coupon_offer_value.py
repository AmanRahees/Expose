# Generated by Django 4.1.3 on 2022-12-02 00:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0009_alter_coupon_offer_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='offer_value',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(20)]),
        ),
    ]
