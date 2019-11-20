import os
import django
from datetime import datetime
from django.utils.timezone import get_current_timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()

from homepage.models import Question  # noqa: E402


def addquestion():
    q = Question(
        question_text="Did you show up?",
        pub_date=datetime.now(tz=get_current_timezone()),
    )
    q.label = "attendance"
    q.save()
    q.choice_set.create(choice_text="Yes!")
    q.choice_set.create(choice_text="I'd love to, but I got something emergency...")

    q1 = Question(
        question_text="How likely are you to recommend LunchNinja to another NYU community member?",
        pub_date=datetime.now(tz=get_current_timezone()),
    )
    q1.label = "experience"
    q1.save()
    q1.choice_set.create(choice_text="1")
    q1.choice_set.create(choice_text="2")
    q1.choice_set.create(choice_text="3")
    q1.choice_set.create(choice_text="4")
    q1.choice_set.create(choice_text="5")

    q2 = Question(
        question_text="How likely are you to recommend the restaurant to a friend or your peers?",
        pub_date=datetime.now(tz=get_current_timezone()),
    )
    q2.label = "restaurant"
    q2.save()
    q2.choice_set.create(choice_text="1")
    q2.choice_set.create(choice_text="2")
    q2.choice_set.create(choice_text="3")
    q2.choice_set.create(choice_text="4")
    q2.choice_set.create(choice_text="5")

    q3 = Question(
        question_text="How would you rate your experience with your lunch partner (considering punctuality and behavior/attitude, etc.)?",
        pub_date=datetime.now(tz=get_current_timezone()),
    )
    q3.label = "partner"
    q3.save()
    q3.choice_set.create(choice_text="1")
    q3.choice_set.create(choice_text="2")
    q3.choice_set.create(choice_text="3")
    q3.choice_set.create(choice_text="4")
    q3.choice_set.create(choice_text="5")


addquestion()
