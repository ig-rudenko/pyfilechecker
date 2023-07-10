import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pyfilechecker.settings")
app = Celery("pyfilechecker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
