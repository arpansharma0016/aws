# Generated by Django 2.2.11 on 2020-12-03 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0014_info_order_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Confirm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.TextField()),
                ('name', models.TextField()),
                ('email', models.TextField()),
                ('password', models.TextField()),
                ('otp', models.TextField()),
            ],
        ),
    ]