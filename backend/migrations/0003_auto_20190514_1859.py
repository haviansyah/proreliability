# Generated by Django 2.2.1 on 2019-05-14 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0002_eqdetail'),
    ]

    operations = [
        migrations.AddField(
            model_name='eqdetail',
            name='catatan',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='eqdetail',
            name='running_hour',
            field=models.IntegerField(null=True),
        ),
    ]