from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class LunchNinjaUser(AbstractUser):
    """
    Users within the Django authentication system are represented by this
    model.

    Username, password and email are required. Other fields are optional.
    """

    Phone = models.CharField(max_length=20)
    school = models.CharField(max_length=100)
    department = models.CharField(max_length=100)

    class Meta(AbstractUser.Meta):
        pass
