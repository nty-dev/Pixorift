# Generated by Django 2.1.7 on 2019-07-25 14:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Rifts', '0007_riftrating'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='riftrating',
            unique_together={('rater', 'rift')},
        ),
    ]