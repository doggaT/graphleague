from celery import shared_task
from champion.models import Champion


@shared_task
def run_champion_loader():
    Champion.champion_loader()
