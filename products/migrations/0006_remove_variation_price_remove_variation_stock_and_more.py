# Generated by Django 4.1.3 on 2022-11-14 06:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_delete_variationmanager'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='variation',
            name='price',
        ),
        migrations.RemoveField(
            model_name='variation',
            name='stock',
        ),
        migrations.AddField(
            model_name='products',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='products',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
