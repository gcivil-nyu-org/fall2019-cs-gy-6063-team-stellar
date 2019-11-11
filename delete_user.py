import os
import django

from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import UserRequest
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()


LunchNinjaUser.objects.all().delete()
UserRequest.objects.all().delete()
