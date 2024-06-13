from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celeryconfig import broker_url, result_backend

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "graphleague.settings")

app = Celery("graphleague", broker=broker_url, backend=result_backend)
app.config_from_object("celeryconfig")
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
