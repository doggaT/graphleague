from celery import shared_task
from api.models import RiotAPI


@shared_task()
def run_calculate_tier_list(apps, schema_editor):
    pass
