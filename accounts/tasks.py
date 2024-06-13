from celery import shared_task
from celery.utils.log import get_task_logger
from api.models import Platform, Ranked
from models import Account

logger = get_task_logger(__name__)
account = Account()
platforms = Platform().get_all_platforms_internal_names()


@shared_task
def run_load_random_challenger_summoner_ids():
    for platform in platforms:
        account.load_random_challenger_summoner_ids(platform, Ranked.SOLO_5x5)
        logger.info("Running run_load_random_challenger_summoner_ids")
