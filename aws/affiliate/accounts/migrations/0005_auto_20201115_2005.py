# Generated by Django 2.2.11 on 2020-11-15 14:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_counter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='counter',
            name='counter',
            field=models.IntegerField(default=0),
        ),
    ]
