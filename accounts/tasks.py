from celery import shared_task
from celery.utils.log import get_task_logger
from accounts.models import Accounts
from api.models import Platform, Ranked

logger = get_task_logger(__name__)
account = Accounts()
platforms = Platform().get_all_platforms_internal_names()


@shared_task
def run_load_random_challenger_summoner_ids():
    for platform in platforms:
        account.load_random_challenger_summoner_ids(platform, Ranked.SOLO_5x5)


@shared_task
def run_load_random_grandmaster_summoner_ids():
    for platform in platforms:
        account.load_random_grandmaster_summoner_ids(platform, Ranked.SOLO_5x5)


@shared_task
def run_load_random_master_summoner_ids():
    for platform in platforms:
        account.load_random_master_summoner_ids(platform, Ranked.SOLO_5x5)
