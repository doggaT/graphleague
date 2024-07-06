from celery import shared_task
from celery.utils.log import get_task_logger
from api.models import Platform
from overview.models import TierList

celery_logger = get_task_logger(__name__)

tier_list = TierList()
platforms = Platform().get_all_platforms_internal_names()


@shared_task()
def run_build_tier_list():
    tier_list.build_tier_list()
