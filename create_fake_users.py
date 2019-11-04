import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','lunchNinja.settings')

import django
django.setup()


from homepage.models import UserRequest

def create_fake_users():
    for i in range(10):
        usr = UserRequest(user_id=i,service_type="Daily")
        usr.save()
        print(i)

if __name__ == "__main__":
    create_fake_users()