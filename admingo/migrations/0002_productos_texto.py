# Generated by Django 2.0.1 on 2018-03-19 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admingo', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='texto',
            field=models.TextField(default=None, max_length=1000),
        ),
    ]
