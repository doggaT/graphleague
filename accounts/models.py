import logging
import requests
from celery.utils.log import get_task_logger
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, IntegrityError, transaction
from api.models import RiotAPI

riot_api = RiotAPI()

logger = logging.getLogger(__name__)
celery_logger = get_task_logger(__name__)


class Accounts(models.Model):
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
    region = models.CharField(null=True)
    platform = models.CharField(null=True)

    class Meta:
        unique_together = ("summoner_id", "platform")

    @staticmethod
    @transaction.atomic
    def load_random_challenger_summoner_ids(platform, queue):
        """Get challenger summoner ids for each platform."""
        try:
            response = riot_api.fetch_challenger_league_data(platform, queue)
            challengers_summoner_ids = response["entries"]
            for summoner_id in challengers_summoner_ids:
                print()
                account, created = Accounts.objects.get_or_create(
                    summoner_id=summoner_id["summonerId"],
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None,
                        "region": None,
                        "platform": platform
                    }
                )
                if created:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} added")
                else:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                celery_logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    @transaction.atomic
    def load_random_grandmaster_summoner_ids(platform, queue):
        """Get grandmaster summoner ids for each platform."""
        try:
            response = riot_api.fetch_grandmaster_league_data(platform, queue)

            challengers_summoner_ids = response["entries"]
            for summoner_id in challengers_summoner_ids:
                account, created = Accounts.objects.get_or_create(
                    summoner_id=summoner_id["summonerId"],
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None,
                        "region": None,
                        "platform": platform
                    }
                )
                if created:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} added")
                else:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                celery_logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    @transaction.atomic
    def load_random_master_summoner_ids(platform, queue):
        """Get master summoner ids for each platform."""
        try:
            response = riot_api.fetch_master_league_data(platform, queue)

            challengers_summoner_ids = response["entries"]
            for summoner_id in challengers_summoner_ids:
                account, created = Accounts.objects.get_or_create(
                    summoner_id=summoner_id["summonerId"],
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None,
                        "region": None,
                        "platform": platform
                    }
                )
                if created:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} added")
                else:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                celery_logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    @transaction.atomic
    def load_random_league_summoner_ids(platform, queue, tier, division):
        """Get league summoner ids for each platform."""
        try:
            challengers_summoner_ids = riot_api.fetch_league_data(platform, queue, tier, division)

            for summoner_id in challengers_summoner_ids:
                account, created = Accounts.objects.get_or_create(
                    summoner_id=summoner_id["summonerId"],
                    defaults={
                        "user_id": None,
                        "game_name": None,
                        "tag_line": None,
                        "puuid": None,
                        "account_id": None,
                        "profile_icon_id": None,
                        "revision_date": None,
                        "summoner_level": None,
                        "region": None,
                        "platform": platform
                    }
                )
                if created:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} added")
                else:
                    celery_logger.info(f"Summoner ID {summoner_id['summonerId']} already exists")
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                celery_logger.error(f"Rate limit exceeded, retrying...")
                raise

    @staticmethod
    @transaction.atomic
    def load_player_ids():
        """Get summoner ids to populate the database."""

        rows = Accounts.objects.filter(account_id__isnull=True)[:1000]

        API_TO_DB_MAP = {
            "puuid": "puuid",
            "accountId": "account_id",
            "profileIconId": "profile_icon_id",
            "revisionDate": "revision_date",
            "summonerLevel": "summoner_level"
        }

        try:
            for row in rows:
                celery_logger.info(row.platform)
                response = riot_api.fetch_summoner_data(row.platform, row.summoner_id)
                for api_field, db_field in API_TO_DB_MAP.items():
                    if api_field in response:
                        value = response[api_field]
                        logger.info(f"Saving {db_field}: {value} to {row.summoner_id}")
                        setattr(row, db_field, value)

                row.save()

        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                celery_logger.error("Rate limit exceeded, retrying...")
                raise

        except IntegrityError as e:
            celery_logger.error(f"IntegrityError: {e}. Skipping Summoner ID {row.summoner_id}")
        except Exception as e:
            celery_logger.error(f"Unexpected error: {e}. Skipping Summoner ID {row.summoner_id}")

    @staticmethod
    def get_game_name_tag_line_by_user_id(user_id):
        try:
            user_account = Accounts.objects.get(user_id_id=user_id)
            return user_account
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def add_or_update_game_name_tag_line(user_id, region, game_name, tag_line):

        try:
            response = riot_api.fetch_account_data_by_riot_id(region, game_name, tag_line)

            obj, created = Accounts.objects.update_or_create(
                user_id_id=user_id,
                defaults={
                    "puuid": response["puuid"],
                    "game_name": response["gameName"],
                    "tag_line": response["tagLine"],
                    "region": region
                }
            )
            if created:
                return "Successfully updated"
            else:
                return "Please make sure that all the information is correct and try again"
        except ObjectDoesNotExist:
            return None
