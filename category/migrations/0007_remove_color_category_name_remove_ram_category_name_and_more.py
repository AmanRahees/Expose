# Generated by Django 4.1.3 on 2022-11-18 14:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0006_color_color_code_color_slug_ram_slug_size_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='color',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='ram',
            name='category_name',
        ),
        migrations.RemoveField(
            model_name='size',
            name='category_name',
        ),
    ]