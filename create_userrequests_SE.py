import os
import random
import django
import datetime
from django.utils import timezone

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
service = {1: "Daily", 2: "Weekly", 3: "Monthly"}
Service_days = {"Daily": 1, "Weekly": 7, "Monthly": 30}
from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import UserRequest, Cuisine, Days_left, Interests  # noqa: E402


# This function generates random user requests
def generateuser(N):
    userlist = []
    i = 0
    all_users = LunchNinjaUser.objects.all()
    for user_obj in all_users:
        i += 1
        user = {}
        user["user"] = user_obj
        user["school"] = "Tandon School of Engineering"

        # service type
        service_id = random.randint(1, 3)
        user["service_type"] = service[service_id]

        # department
        user["department"] = "Computer Science"

        # cuisine
        cuisines = Cuisine.objects.all()
        p_cuisine_number = random.randint(4, 10)
        p_cuisine = random.sample(list(cuisines), p_cuisine_number)
        user["prefered cuisines"] = p_cuisine

        interests = Interests.objects.all()
        p_interest_number = random.randint(2, 10)
        p_interests = random.sample(list(interests), p_interest_number)
        user["interests"] = p_interests

        user["meet history"] = []
        user["cuisines_priority"] = random.randint(1, 10)
        user["department_priority"] = random.randint(1, 10)
        user["interests_priority"] = random.randint(1, 10)
        userlist.append(user)

    return userlist


# This function saves the generated user requests to database
def save_users(userlist):
    for user in userlist:
        r = UserRequest(
            user=user["user"],
            # service_type=user["service_type"],
            service_type="Daily",
            school=user["school"],
            department=user["department"],
            time_stamp=datetime.datetime.now(tz=timezone.get_current_timezone()),
            cuisines_priority=user["cuisines_priority"],
            department_priority=user["department_priority"],
            interests_priority=user["interests_priority"],
        )
        r.save()
        for each in user["prefered cuisines"]:
            r.cuisines.add(each)
        for each in user["interests"]:
            r.interests.add(each)
        days = Days_left(user=user["user"], days=Service_days[r.service_type])
        days.save()


if __name__ == "__main__":
    usercount = LunchNinjaUser.objects.all().count()
    userlist = generateuser(usercount)
    save_users(userlist)
