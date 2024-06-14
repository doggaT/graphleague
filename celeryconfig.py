import os
from dotenv import load_dotenv
from celery.schedules import crontab

load_dotenv()

broker_url = "redis://localhost:6379/0" # os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
result_backend = "redis://localhost:6379/0" # os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379/0")
broker_connection_retry_on_startup = True
timezone = "UTC"

beat_schedule = {
    "weekly-update": {
        "task": "champion.tasks.run_champion_loader",
        "schedule": crontab(day_of_week="2", hour="10", minute="0"),
    },
    "get-challenger-summoner-ids": {
        "task": "accounts.tasks.run_load_random_challenger_summoner_ids",
        "schedule": crontab(hour="23", minute="0"),
    },
}
