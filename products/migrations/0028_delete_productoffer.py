# Generated by Django 4.1.3 on 2022-12-01 17:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0027_products_offer_price_alter_products_price'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductOffer',
        ),
    ]
