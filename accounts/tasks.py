from celery import shared_task
from celery.utils.log import get_task_logger
from accounts.models import Accounts
from api.models import Platform, Ranked, Tier, Division


celery_logger = get_task_logger(__name__)

account = Accounts()
platforms = Platform().get_all_platforms_internal_names()


@shared_task(bind=True)
def run_load_random_challenger_summoner_ids():
    for platform in platforms:
        account.load_random_challenger_summoner_ids(platform, Ranked.SOLO_5x5)


@shared_task(bind=True)
def run_load_random_grandmaster_summoner_ids():
    for platform in platforms:
        account.load_random_grandmaster_summoner_ids(platform, Ranked.SOLO_5x5)


@shared_task(bind=True)
def run_load_random_master_summoner_ids():
    for platform in platforms:
        account.load_random_master_summoner_ids(platform, Ranked.SOLO_5x5)


@shared_task(bind=True)
def run_load_random_diamond_one_summoner_ids():
    for platform in platforms:
        account.load_random_league_summoner_ids(platform, Ranked.SOLO_5x5, Tier.DIAMOND, Division.ONE)


@shared_task(bind=True)
def run_load_random_diamond_two_summoner_ids():
    for platform in platforms:
        account.load_random_league_summoner_ids(platform, Ranked.SOLO_5x5, Tier.DIAMOND, Division.TWO)


@shared_task(bind=True)
def run_load_random_diamond_three_summoner_ids():
    for platform in platforms:
        account.load_random_league_summoner_ids(platform, Ranked.SOLO_5x5, Tier.DIAMOND, Division.THREE)


@shared_task(bind=True)
def run_load_random_diamond_four_summoner_ids():
    for platform in platforms:
        account.load_random_league_summoner_ids(platform, Ranked.SOLO_5x5, Tier.DIAMOND, Division.FOUR)


@shared_task(bind=True)
def run_load_player_ids():
    account.load_player_ids()
