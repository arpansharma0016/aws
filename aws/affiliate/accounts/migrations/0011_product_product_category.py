# Generated by Django 2.2.11 on 2020-11-17 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_remove_product_product_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='product_category',
            field=models.TextField(blank=True),
        ),
    ]