import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphleague.settings")

app = Celery("champion")
app.conf.beat_schedule = {
    "weekly-update": {
        "task": "champion.tasks.run_champion_loader",
        "schedule": crontab(day_of_week="2", hour="10", minute="0"),
    },
}
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
