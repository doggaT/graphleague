from __future__ import absolute_import, unicode_literals
import os
from dotenv import load_dotenv
from celery import Celery
from celeryconfig import broker_url, result_backend
from django.conf import settings

load_dotenv()


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphleague.settings")

app = Celery("graphleague", broker=broker_url, backend=result_backend)
app.config_from_object(settings, namespace="celeryconfig")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
