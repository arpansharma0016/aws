# Generated by Django 2.2.11 on 2020-11-17 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_product_product_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='product_category',
            field=models.TextField(),
        ),
    ]
