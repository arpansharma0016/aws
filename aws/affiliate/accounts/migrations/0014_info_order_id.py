# Generated by Django 2.1 on 2020-11-29 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_auto_20201127_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='order_id',
            field=models.TextField(null=True),
        ),
    ]
