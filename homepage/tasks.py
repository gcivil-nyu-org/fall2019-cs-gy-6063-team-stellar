# from background_task import background


# from django.utils import timezone

# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)


# @background(schedule=timezone.localtime(timezone.now()).replace(hour=10, minute=36))
# def run_matching():
#     run(["python", "match.py"], shell=False, stdout=PIPE)

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery import task, shared_task
from subprocess import run, PIPE

# @periodic_task(run_every=(crontab(minute="*/4")), name="run_every_1_minutes", ignore_result=True)

@periodic_task(run_every=(crontab(minute=0, hour=18)), name="run_every_1_minutes", ignore_result=True)
def add():
    run(["python", "match.py"], shell=False, stdout=PIPE)
