# Generated by Django 4.1.3 on 2022-12-12 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0008_category_category_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_offer',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
