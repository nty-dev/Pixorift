# Generated by Django 2.2.1 on 2019-05-28 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ImageRecog', '0003_auto_20190527_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playerquest',
            name='questitem',
            field=models.CharField(choices=[('airplane', 'Airplane'), ('boat', 'Boat'), ('computer_mouse', 'Computer Mouse'), ('flower', 'Flower'), ('fridge', 'Fridge'), ('house', 'House'), ('playground', 'Playground'), ('pond', 'Pond'), ('road', 'Road'), ('rubbish_bin', 'Rubbish Bin'), ('sidewalk', 'Sidewalk'), ('stop_sign', 'Stop Sign'), ('tree', 'Tree'), ('truck', 'Truck')], default='road', max_length=100),
        ),
    ]
