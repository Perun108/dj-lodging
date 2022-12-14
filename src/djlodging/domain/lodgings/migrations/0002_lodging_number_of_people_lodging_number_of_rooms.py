# Generated by Django 4.0 on 2022-08-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lodgings', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lodging',
            name='number_of_people',
            field=models.PositiveSmallIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='lodging',
            name='number_of_rooms',
            field=models.PositiveSmallIntegerField(default=1),
        ),
    ]
