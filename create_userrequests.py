import os
import random
import django


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()

from user_account.models import LunchNinjaUser

service = {1: "Daily", 2: "Weekly", 3: "Monthly"}
from homepage.models import UserRequest, School, Department, Cuisine


# This function generates random user requests
def generateuser(N):
    userlist = []

    all_users = LunchNinjaUser.objects.all()
    for user_obj in all_users:
        user = {}
        user["user"] = user_obj
        # school
        school_id = random.randint(0, School.objects.all().count() - 1)
        user["school"] = School.objects.filter(id=school_id)

        service_id = random.randint(1, 3)
        user["service_type"] = service[service_id]

        # department
        departments = Department.objects.filter(school=school_id)
        departments_count = departments.count()
        if departments_count == 0:
            continue
        start_id = departments[0].id
        department_id = random.randint(0, departments_count)
        user["department"] = Department.objects.filter(
            id=(start_id + department_id - 1)
        )

        # cuisine
        cuisines = Cuisine.objects.all()
        p_cuisine_number = random.randint(1, Cuisine.objects.all().count() - 1)
        p_cuisine = random.sample(list(cuisines), p_cuisine_number)
        user["prefered cuisines"] = p_cuisine

        user["meet history"] = []
        userlist.append(user)
    return userlist


# This function saves the generated user requests to database
def save_users(userlist):
    for user in userlist:
        r = UserRequest(
            user=user["user"],
            service_type=user["service_type"],
            school=user["school"][0].name,
            department=user["department"][0].name,
        )
        r.save()
        for each in user["prefered cuisines"]:
            r.cuisines.add(each)


if __name__ == "__main__":
    userlist = generateuser(20)
    import pdb; pdb.set_trace()
    save_users(userlist)
