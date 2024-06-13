from celery.schedules import crontab

broker_url = "redis://:password@hostname:port/0"
result_backend = "rpc://"
timezone = "UTC"

beat_schedule = {
    "weekly-update": {
        "task": "champion.tasks.run_champion_loader",
        "schedule": crontab(day_of_week="2", hour="10", minute="0"),
    },
    "get-challenger-summoner-ids": {
        "task": "accounts.tasks.run_load_random_challenger_summoner_ids",
        "schedule": crontab(hour="10", minute="0"),
    },
}
