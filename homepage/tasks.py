# from background_task import background


# from django.utils import timezone

# import os

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)


# @background(schedule=timezone.localtime(timezone.now()).replace(hour=10, minute=36))
# def run_matching():
#     run(["python", "match.py"], shell=False, stdout=PIPE)

# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from subprocess import run, PIPE


@task(ignore_result=True)
def run_matching_algorithm():
    run(["python", "match.py"], shell=False, stdout=PIPE)

# @background(schedule=timezone.localtime(timezone.now()).replace(hour=0, minute=1))
# def run_matching():
    
@task(ignore_result=True)
def send_match_feedback():
    run(["python", "feedback.py"], shell=False, stdout=PIPE)
