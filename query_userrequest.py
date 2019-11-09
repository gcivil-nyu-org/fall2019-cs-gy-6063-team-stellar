import os
import django
from django.db.models import Q

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from user_account.models import LunchNinjaUser  # noqa: E402
from homepage.models import UserRequest  # noqa: E402


my_filter_qs = Q()
B = UserRequest.objects.filter(department="Mathematics")
A = LunchNinjaUser.objects.filter(department="Ctr for Urban Sci and Progress")

my_filter_qs = Q()
for creator in list(A):
    my_filter_qs = my_filter_qs | Q(user=creator)
M_A_B = B.filter(my_filter_qs)
print(M_A_B)
