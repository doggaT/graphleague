# Generated by Django 4.2.13 on 2024-07-06 15:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('overview', '0005_alter_tierlist_synergy'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tierlist',
            name='synergy',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True), blank=True, null=True, size=None),
        ),
    ]
