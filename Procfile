web: gunicorn your_project.wsgi:application
worker: celery -A graphleague.celery_app worker --loglevel=info
beat: celery -A graphleague.celery_app beat --loglevel=info