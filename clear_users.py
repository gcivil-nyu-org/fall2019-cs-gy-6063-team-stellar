import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402



if __name__ == "__main__":
    LunchNinjaUser.objects.clear()
