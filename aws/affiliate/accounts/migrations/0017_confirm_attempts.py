# Generated by Django 2.2.11 on 2020-12-04 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0016_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='confirm',
            name='attempts',
            field=models.IntegerField(default=0),
        ),
    ]
