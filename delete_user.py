import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import UserRequest  # noqa: E402


LunchNinjaUser.objects.all().delete()
UserRequest.objects.all().delete()
