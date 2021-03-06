import os
import random
import django
import datetime
from django.utils import timezone
from datetime import date

from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
service = {1: "Daily", 2: "Weekly", 3: "Monthly"}
Service_days = {"Daily": 1, "Weekly": 7, "Monthly": 30}
from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import (
    UserRequest,
    School,
    Department,
    Cuisine,
    Days_left,
    Interests,
    Days,
)  # noqa: E402


# This function generates random user requests
def generateuser(N):
    userlist = []
    i = 0
    all_users = LunchNinjaUser.objects.all()
    for user_obj in all_users:
        i += 1
        user = {}
        user["user"] = user_obj

        # school
        school_id = random.randint(1, School.objects.all().count())
        user["school"] = School.objects.get(id=school_id)

        # service type
        service_id = random.randint(1, 3)
        user["service_type"] = service[service_id]
        # user["service_type"] = "Daily"

        # department
        departments = Department.objects.filter(school=school_id)
        departments_count = departments.count()
        if departments_count == 0:
            continue
        start_id = departments.first().id
        department_index = random.randint(1, departments_count)
        # department_index = random.randint(1, 6)
        department_id = start_id + department_index - 1
        user["department"] = Department.objects.get(id=department_id)

        # cuisine
        cuisines = Cuisine.objects.all()
        p_cuisine_number = random.randint(1, 10)
        p_cuisine = random.sample(list(cuisines), p_cuisine_number)
        user["prefered cuisines"] = p_cuisine

        # interests
        interests = Interests.objects.all()
        p_interest_number = random.randint(1, 10)
        p_interests = random.sample(list(interests), p_interest_number)
        user["interests"] = p_interests

        # days
        if not user["service_type"] == "Daily":
            days = Days.objects.all()
            p_days_number = random.randint(1, 3)

            p_days = random.sample(list(days), p_days_number)
        else:
            p_days = Days.objects.all()[0]

        user["prefered days"] = p_days
        user["meet history"] = []
        user["cuisines_priority"] = random.randint(1, 10)
        user["department_priority"] = random.randint(1, 10)
        user["interests_priority"] = random.randint(1, 10)
        userlist.append(user)

    return userlist


# This function saves the generated user requests to database
def save_users(userlist):
    for user in userlist:
        today = date.today() + timedelta(days=1)
        r = UserRequest(
            user=user["user"],
            service_type=user["service_type"],
            school=user["school"],
            department=user["department"],
            time_stamp=datetime.datetime.now(tz=timezone.get_current_timezone()),
            cuisines_priority=user["cuisines_priority"],
            department_priority=user["department_priority"],
            interests_priority=user["interests_priority"],
            available_date=today,
        )
        r.save()
        for each in user["prefered cuisines"]:
            r.cuisines.add(each)
        for each in user["interests"]:
            r.interests.add(each)

        if not user["service_type"] == "Daily":
            for each in user["prefered days"]:
                r.days.add(each)

        days = Days_left(user=user["user"], days=Service_days[r.service_type])
        days.save()


if __name__ == "__main__":
    usercount = LunchNinjaUser.objects.all().count()
    userlist = generateuser(usercount)
    save_users(userlist)
