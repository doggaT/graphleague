from celery import shared_task
from champion.models import Champion


@shared_task
def run_champion_loader(apps, schema_editor):
    Champion.champion_loader()

    champion_model = apps.get_model("champion", "Champion")
    champions = Champion.champion_loader()

    for champion in champions:
        champion_model.objects.update_or_create(defaults=champion, **champion)
