import logging
import requests
from django.contrib.auth.models import User
from django.db import models, IntegrityError
from api.models import RiotAPI

riot_api = RiotAPI()

logger = logging.getLogger(__name__)


class Account:
    objects = models.Manager()

    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    game_name = models.CharField(null=True)
    tag_line = models.CharField(null=True)
    summoner_id = models.CharField(primary_key=True, null=False)
    account_id = models.CharField(null=True)
    puuid = models.CharField(null=True)
    profile_icon_id = models.CharField(null=True)
    revision_date = models.CharField(null=True)
    summoner_level = models.IntegerField(null=True)

    @staticmethod
    def load_random_challenger_summoner_ids(platform, queue):
        """Get challenger summoner ids for each platform."""
        try:
            response = riot_api.fetch_challenger_league_data(platform, queue)

            challengers_summoner_ids = response.json()["entries"]
            for summoner_id in challengers_summoner_ids:
                account, created = Account.objects.get_or_create(
                    summoner_id=summoner_id,
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None
                    }
                )
                if created:
                    logger.info(f"Summoner ID {summoner_id} added")
                else:
                    logger.info(f"Summoner ID {summoner_id} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    def load_random_grandmaster_summoner_ids_by_platform(platform, queue):
        """Get grandmaster summoner ids for each platform."""
        try:
            response = riot_api.fetch_grandmaster_league_data(platform, queue)

            challengers_summoner_ids = response.json()["entries"]
            for summoner_id in challengers_summoner_ids:
                account, created = Account.objects.get_or_create(
                    summoner_id=summoner_id,
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None
                    }
                )
                if created:
                    logger.info(f"Summoner ID {summoner_id} added")
                else:
                    logger.info(f"Summoner ID {summoner_id} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    def load_random_master_summoner_ids_by_platform(platform, queue):
        """Get master summoner ids for each platform."""
        try:
            response = riot_api.fetch_master_league_data(platform, queue)

            challengers_summoner_ids = response.json()["entries"]
            for summoner_id in challengers_summoner_ids:
                account, created = Account.objects.get_or_create(
                    summoner_id=summoner_id,
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None
                    }
                )
                if created:
                    logger.info(f"Summoner ID {summoner_id} added")
                else:
                    logger.info(f"Summoner ID {summoner_id} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    def load_random_league_summoner_ids_by_platform(platform, queue, tier, division):
        """Get league summoner ids for each platform."""
        try:
            response = riot_api.fetch_league_data(platform, queue, tier, division)

            challengers_summoner_ids = response.json()["entries"]
            for summoner_id in challengers_summoner_ids:
                account, created = Account.objects.get_or_create(
                    summoner_id=summoner_id,
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None
                    }
                )
                if created:
                    logger.info(f"Summoner ID {summoner_id} added")
                else:
                    logger.info(f"Summoner ID {summoner_id} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    def load_player_ids(platform, summoner_id_list):
        """Get summoner ids to populate the database."""
        for summoner_id in summoner_id_list:
            try:
                response = riot_api.fetch_summoner_data(platform, summoner_id)
                data = response.json()

                account, created = Account.objects.get_or_create(
                    summoner_id=data["id"],
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": data["puuid"],
                        "account_id": data["accountId"],
                        "profile_icon_id": data["profileIconId"],
                        "revision_date": data["revisionDate"],
                        "summoner_level": data["summonerLevel"]
                    }
                )
                if created:
                    logger.info(f"Summoner ID {summoner_id} added")
                else:
                    logger.info(f"Summoner ID {summoner_id} already exists")

            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 429:
                    logger.error("Rate limit exceeded, retrying...")
                    raise
            except IntegrityError as e:
                logger.error(f"IntegrityError: {e}. Skipping Summoner ID {summoner_id}")
            except Exception as e:
                logger.error(f"Unexpected error: {e}. Skipping Summoner ID {summoner_id}")
