# Generated by Django 4.0 on 2022-08-22 11:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='registration_token',
            new_name='security_token',
        ),
    ]