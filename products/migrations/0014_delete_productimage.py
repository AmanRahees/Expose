# Generated by Django 4.1.3 on 2022-11-17 00:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0013_rename_image_productimage_images_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProductImage',
        ),
    ]
