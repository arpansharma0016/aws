# Generated by Django 2.2.11 on 2020-11-15 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_info'),
    ]

    operations = [
        migrations.CreateModel(
            name='counter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('counter', models.TextField()),
                ('username', models.TextField()),
            ],
        ),
    ]