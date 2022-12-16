# Generated by Django 4.1.3 on 2022-12-05 02:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Brand', '0010_alter_coupon_offer_value'),
    ]

    operations = [
        migrations.CreateModel(
            name='Couponuser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('coupon_code', models.CharField(blank=True, max_length=50, null=True)),
                ('coupon_value', models.IntegerField(blank=True, null=True)),
                ('coupon_model', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Brand.coupon')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
