from django.contrib.postgres.fields import ArrayField
from django.db import models


class TierList:
    objects = models.Manager()

    riot_id = models.IntegerField(primary_key=True)
    champion_key = models.CharField(null=False)
    champion_name = models.CharField(null=False)
    win_rate = models.CharField(null=False)
    pick_rate = models.CharField(null=False)
    ban_rate = models.CharField(null=False)
    region = models.CharField(null=False)
    synergy = ArrayField(models.CharField(null=False))
