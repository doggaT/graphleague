import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
timezone = "UTC"

beat_schedule = {
    "weekly-update": {
        "task": "champion.tasks.run_champion_loader",
        "schedule": crontab(day_of_week="2", hour="10", minute="0"),
    },
    "get-challenger-summoner-ids": {
        "task": "accounts.tasks.run_load_random_challenger_summoner_ids",
        "schedule": crontab(hour="7", minute="0"),
    },
}
