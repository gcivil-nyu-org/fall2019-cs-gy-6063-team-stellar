# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import task
from subprocess import run, PIPE


@task(ignore_result=True)
def run_matching_algorithm():
    run(["python", "match.py"], shell=False, stdout=PIPE)


@task(ignore_result=True)
def send_match_feedback():
    run(["python", "feedback.py"], shell=False, stdout=PIPE)
