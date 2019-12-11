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
    count_start = LunchNinjaUser.objects.all().count() + 1
    count_end = count_start + N
    for user_id in range(count_start, count_end):
        un = "ut" + str(user_id)
        useremail = un + "@nyu.edu"
        print(useremail)
        password = "Stellar123!"

        # school
        school_id = random.randint(1, School.objects.all().count())
        # school_id = random.randint(2, 2)
        school = School.objects.filter(id=school_id)[0].name

        # department
        departments = Department.objects.filter(school=school_id)
        departments_count = departments.count()
        if departments_count == 0:
            continue
        start_id = departments.first().id
        department_index = random.randint(1, departments_count)
        # department_index = random.randint(1, 6)
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
    user = LunchNinjaUser(
        username="yh3244",
        email="yh3244@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Yixin",
        last_name="Hu",
        is_active=True,
    )
    user.set_password("Stellar123!")
    user.save()
    user1 = LunchNinjaUser(
        username="up293",
        email="up293@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Utkarsh",
        last_name="Prakash",
        is_active=True,
    )
    user1.set_password("Stellar123!")
    user1.save()
    user2 = LunchNinjaUser(
        username="xh1255",
        email="xh1255@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Xinchi",
        last_name="Huang",
        is_active=True,
    )
    user2.set_password("Stellar123!")
    user2.save()
    user3 = LunchNinjaUser(
        username="bv640",
        email="bv640@nyu.edu",
        school="Tandon School of Engineering",
        department="Computer Science",
        first_name="Bhaskar",
        last_name="V",
        is_active=True,
    )
    user3.set_password("Stellar123!")
    user3.save()
    user3 = LunchNinjaUser(
        username="yz1281",
        email="yz1281@nyu.edu",
        school="Tisch School of the Arts",
        department="Photography & Imaging",
        first_name="Tianyang",
        last_name="Zhu",
        is_active=True,
    )
    user3.set_password("Stellar123!")
    user3.save()
    # generateuser(20)
