# Generated by Django 4.2.13 on 2024-07-06 15:49

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tierlist',
            name='platform',
        ),
        migrations.AlterField(
            model_name='tierlist',
            name='synergy',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(default=[]), size=None),
        ),
    ]
