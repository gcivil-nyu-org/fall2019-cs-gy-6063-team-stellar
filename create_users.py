import os
import random
import django

from faker import Faker

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import Department, School  # noqa: E402


# This function generates random users and save them to database
def generateuser(N):
    fake = Faker()
    for user_id in range(1, N + 1):

        un = "ut" + str(user_id)
        useremail = un + "@nyu.edu"
        password = "Stellar123!"
        print(useremail)

        # school
        school_id = random.randint(1, School.objects.all().count() - 1)
        school = School.objects.filter(id=school_id)[0].name

        # department
        departments = Department.objects.filter(school=school_id)
        departments_count = departments.count()
        if departments_count == 0:
            continue
        start_id = departments.first().id
        department_index = random.randint(1, departments_count)
        department_id = start_id + department_index - 1
        department = Department.objects.filter(id=department_id)[0].name

        first_name = fake.first_name()
        last_name = fake.last_name()

        user = LunchNinjaUser(
            username=un,
            email=useremail,
            school=school,
            department=department,
            first_name=first_name,
            last_name=last_name,
            is_active=True,
        )
        user.set_password(password)
        user.save()


if __name__ == "__main__":
    generateuser(20)
