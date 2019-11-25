from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
# from celery.task.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")


app = Celery("lunchNinja")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.timezone = "UTC"
app.conf.enable_utc = True
app.conf.update(
    BROKER_URL=os.environ["REDIS_URL"], CELERY_RESULT_BACKEND=os.environ["REDIS_URL"]
)
# amqp://pcsrozek:Mgc_X5...@crane.rmq.cloudamqp.com/pcsrozek


# Schedule periodic tasks.
app.conf.beat_schedule = {
    # Run matching algorithm
    # "run_matching_algorithm": {
    #     "task": "homepage.tasks.run_matching_algorithm",
    #     # "schedule": crontab(minute=0, hour=15),
    #     "schedule": crontab(minute = '*/1'),
    # },
    # "send_match_feedback": {
    #     "task": "homepage.tasks.send_match_feedback",
    #     "schedule": crontab(minute=5, hour=15),
    # },
}

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print("Request: {0!r}".format(self.request))
