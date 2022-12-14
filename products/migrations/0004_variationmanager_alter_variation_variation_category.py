# Generated by Django 4.1.3 on 2022-11-13 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_alter_variation_variation_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='VariationManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('memory', 'memory'), ('color', 'color')], max_length=200),
        ),
    ]
