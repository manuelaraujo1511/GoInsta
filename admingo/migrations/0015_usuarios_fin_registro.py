# Generated by Django 2.0.5 on 2018-06-10 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admingo', '0014_auto_20180510_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarios',
            name='fin_registro',
            field=models.IntegerField(default=0),
        ),
    ]
