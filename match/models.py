from django.db import models

from api.models import RiotAPI


class Match:
    riot_api = RiotAPI()

    def get_matches_by_puuid(self, region, puuid):
        self.riot_api.fetch_summoner_matches_data(region, puuid)
