# Generated by Django 4.1.3 on 2022-11-14 04:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_variationmanager_alter_variation_variation_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='VariationManager',
        ),
    ]