# Generated by Django 2.2.1 on 2019-06-03 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0009_auto_20190604_0616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='alatdcs',
            old_name='nama',
            new_name='name',
        ),
    ]
