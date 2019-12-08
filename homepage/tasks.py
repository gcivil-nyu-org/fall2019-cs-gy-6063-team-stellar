from background_task import background

from subprocess import run, PIPE
from django.utils import timezone

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", __file__)


@background(schedule=timezone.localtime(timezone.now()).replace(hour=0, minute=1))
def run_matching():
    run(["python", "match.py"], shell=False, stdout=PIPE)
