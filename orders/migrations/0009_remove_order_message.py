# Generated by Django 4.1.3 on 2022-11-29 08:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_status_alter_orderitem_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='message',
        ),
    ]
