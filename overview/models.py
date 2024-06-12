import logging

import pandas as pd
import requests
from django.contrib.postgres.fields import ArrayField
from django.db import models

from api.models import RiotAPI, Platform, Ranked
from champion.models import Champion

platforms = Platform.get_all_platforms_internal_names()
riot_api = RiotAPI()

logger = logging.getLogger(__name__)


class TierList:
    objects = models.Manager()

    riot_id = models.ForeignKey(Champion, primary_key=True, on_delete=models.CASCADE)
    win_rate = models.CharField(null=False)
    pick_rate = models.CharField(null=False)
    ban_rate = models.CharField(null=False)
    region = models.CharField(null=False)
    league = models.CharField(null=False)
    synergy = ArrayField(models.CharField(null=False))

    def build_tier_list(self):
        pass
