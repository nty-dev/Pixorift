# Generated by Django 2.1.7 on 2019-06-20 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RPosts', '0002_auto_20190620_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pixopost',
            name='images',
            field=models.ManyToManyField(blank=True, null=True, to='RPosts.ImageDataBank'),
        ),
    ]