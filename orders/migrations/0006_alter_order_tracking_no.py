# Generated by Django 4.1.3 on 2022-11-22 01:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_alter_order_tracking_no'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='tracking_no',
            field=models.CharField(max_length=150, null=True),
        ),
    ]