import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

broker_url = os.environ.get("CELERY_BROKER_URL")
result_backend = os.environ.get("CELERY_BROKER_URL")
broker_connection_retry_on_startup = True
timezone = "UTC"

beat_schedule = {
    "weekly-champion-update": {
        "task": "champion.tasks.run_champion_loader",
        "schedule": crontab(day_of_week="2", hour="10", minute="0"),
    },
    "get-challenger-summoner-ids": {
        "task": "accounts.tasks.run_load_random_challenger_summoner_ids",
        "schedule": crontab(hour="13", minute="0"),
    },
    "get-grandmaster-summoner-ids": {
        "task": "accounts.tasks.run_load_random_grandmaster_summoner_ids",
        "schedule": crontab(hour="13", minute="0"),
    },
    "get-master-summoner-ids": {
        "task": "accounts.tasks.run_load_random_master_summoner_ids",
        "schedule": crontab(hour="13", minute="0"),
    },
}
