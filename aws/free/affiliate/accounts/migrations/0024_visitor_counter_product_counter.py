# Generated by Django 2.2.11 on 2021-06-17 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0023_auto_20210614_1146'),
    ]

    operations = [
        migrations.AddField(
            model_name='visitor_counter',
            name='product_counter',
            field=models.IntegerField(default=0),
        ),
    ]
