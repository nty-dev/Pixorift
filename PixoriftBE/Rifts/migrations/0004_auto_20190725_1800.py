# Generated by Django 2.1.7 on 2019-07-25 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Rifts', '0003_auto_20190725_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rift',
            name='content',
            field=models.CharField(blank=True, max_length=1200, null=True),
        ),
    ]
