from django.db.models import Q
from accounts.models import Accounts
from api.models import RiotAPI, RegionToPlatform


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

    def get_matches_by_puuid(self, platform="euw1", queue=None):
        platform_not_null = Q(platform=platform)
        puuid_not_null = Q(puuid__isnull=False)
        user_account = Accounts.objects.filter(platform_not_null and puuid_not_null)[::50]
        summoner_matches = []

        for account in user_account:
            region = RegionToPlatform.get_region(account.platform)
            matches = self.riot_api.fetch_summoner_matches_data(region, account.puuid, match_type=queue,
                                                                queue_id=420, count=10)
            for match_id in matches:
                response = self.riot_api.fetch_match_data(region, match_id)
                summoner_matches.append(response)
        return summoner_matches

    # def get_matches_details(self, region, match_id):
    #     response = self.riot_api.fetch_match_data(user_account.region, match_id)
    #     return summoner_matches
