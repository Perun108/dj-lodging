# Generated by Django 4.0 on 2022-11-27 22:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookings', '0004_booking_reference_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='booking',
            options={'ordering': ('-created',)},
        ),
    ]