# Generated by Django 4.2.13 on 2024-05-09 19:31

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Champion',
            fields=[
                ('riot_id', models.IntegerField(primary_key=True, serialize=False)),
                ('champion_key', models.CharField()),
                ('champion_name', models.CharField()),
                ('champion_title', models.CharField()),
                ('splash_url', models.CharField()),
                ('icon_url', models.CharField()),
                ('resource', models.CharField()),
                ('attack_type', models.CharField()),
                ('adaptive_type', models.CharField()),
                ('stats', models.JSONField()),
                ('positions', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None)),
                ('roles', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None)),
                ('role_class', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(), size=None)),
                ('attr_rating', models.JSONField()),
                ('abilities', models.JSONField()),
                ('lore', models.CharField()),
                ('faction', models.CharField()),
                ('overall_play_rates', models.JSONField()),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('extra', models.CharField()),
            ],
        ),
    ]
