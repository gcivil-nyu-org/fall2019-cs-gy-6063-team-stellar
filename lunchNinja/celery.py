from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.task.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")

app = Celery("lunchNinja")

if "REDIS_URL" in os.environ:
    redis_url = os.environ["REDIS_URL"]
else:
    redis_url = "/"

app.conf.update(BROKER_URL=redis_url, CELERY_RESULT_BACKEND=redis_url)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = "UTC"
app.conf.enable_utc = True

# Schedule periodic tasks.
app.conf.beat_schedule = {
    # Run matching algorithm
    "run_matching_algorithm": {
        "task": "homepage.tasks.run_matching_algorithm",
        # "schedule": crontab(minute=0, hour=19),
    "schedule": crontab(minute="*/1"),
    },
    # Send feedback forms
    "send_match_feedback": {
        "task": "homepage.tasks.send_match_feedback",
        "schedule": crontab(minute=0, hour=14),
    },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
