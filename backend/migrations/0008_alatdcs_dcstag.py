# Generated by Django 2.2.1 on 2019-06-03 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0007_auto_20190526_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='AlatDCS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nama', models.CharField(max_length=200)),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.Unit')),
            ],
        ),
        migrations.CreateModel(
            name='DcsTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('left', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('top', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('AlatDCS', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='backend.AlatDCS')),
            ],
        ),
    ]