# Generated by Django 2.2.1 on 2019-05-26 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0005_assetwellness'),
    ]

    operations = [
        migrations.AddField(
            model_name='assetwellness',
            name='judegement',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='assetwellness',
            name='recomendation',
            field=models.TextField(null=True),
        ),
    ]
