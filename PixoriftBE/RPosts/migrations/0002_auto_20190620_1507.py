# Generated by Django 2.1.7 on 2019-06-20 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('RPosts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pixopost',
            name='date_posted',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
