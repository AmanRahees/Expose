# Generated by Django 4.1.3 on 2022-12-10 23:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Brand', '0013_remove_brand_brand_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponuser',
            name='coupon_model',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cpnrrelate', to='Brand.coupon'),
        ),
    ]
