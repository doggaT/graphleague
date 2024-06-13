web: gunicorn graphleague.wsgi:application
worker: celery -A graphleague.celery_app worker --loglevel=info
beat: celery -A graphleague.celery_app beat --loglevel=info
flower: celery -A graphleague.celery_app flower --port=5555