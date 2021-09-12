# Generated by Django 2.2.11 on 2021-01-10 07:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0021_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='info',
            name='on_trial',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='info',
            name='trial',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='info',
            name='trial_done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='info',
            name='trial_end',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='info',
            name='trial_start',
            field=models.TextField(blank=True, null=True),
        ),
    ]
