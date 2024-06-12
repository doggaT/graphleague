from celery import shared_task


@shared_task
def run_load_random_challenger_summoner_ids():
    print("Hello")
