# Generated by Django 2.1.7 on 2019-06-21 07:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserInfo', '0004_auto_20190430_2322'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
