# Generated by Django 2.1.7 on 2019-05-27 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageRecog', '0002_playerquest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerquest',
            name='questitem',
            field=models.CharField(choices=[('airplane', 'Airplane'), ('boat', 'Boat'), ('computer_mouse', 'Computer Mouse'), ('flower', 'Flower'), ('fridge', 'Fridge'), ('house', 'House'), ('playground', 'Playground'), ('pond', 'Pond'), ('road', 'Road'), ('rubbish_bin', 'Rubbish Bin'), ('sidewalk', 'Sidewalk'), ('stop_sign', 'Stop Sign'), ('tree', 'Tree'), ('truck', 'Truck')], default='fridge', max_length=100),
        ),
    ]
