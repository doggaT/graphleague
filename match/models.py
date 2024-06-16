from django.db import models

from accounts.models import Accounts
from api.models import RiotAPI


class Match:
    riot_api = RiotAPI()

    def get_my_matches_by_puuid(self, user_id, queue=None):
        user_account = Accounts.objects.get(user_id_id=user_id)
        my_matches = []
        if user_account is not None:
            matches = self.riot_api.fetch_summoner_matches_data(
                user_account.region, user_account.puuid, match_type=queue, queue_id=420, count=10)
            for match_id in matches:
                response = self.riot_api.fetch_match_data(user_account.region, match_id)
                my_matches.append(response)
            return my_matches, user_account

        return None

    def get_matches_details(self, region, match_id):
        pass
