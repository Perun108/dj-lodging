# Generated by Django 4.0 on 2022-10-02 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lodgings', '0004_review'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lodging',
            old_name='type',
            new_name='kind',
        ),
    ]
