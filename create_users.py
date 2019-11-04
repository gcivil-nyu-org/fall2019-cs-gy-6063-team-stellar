import os
import random
import django
import string

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402

from user_account.models import LunchNinjaUser

# This function generates random password
def random_password_generator():
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    size = 8
    return "".join(random.choice(chars) for x in range(size, 20))


# This function generates random users and save them to database
def generateuser(N):
    for user_id in range(1, N + 1):
        un = "ut" + str(user_id)
        pw = random_password_generator()
        useremail = un + "@nyu.edu"
        print(useremail)
        user = LunchNinjaUser(username=un, password=pw, email=useremail, is_active=True)
        user.save()


if __name__ == "__main__":
    generateuser(20)
