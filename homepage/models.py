from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone

m_state = False


class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    school = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = m_state


class School(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = m_state


class Restaurant(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    cuisine = models.CharField(max_length=100, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    borough = models.CharField(max_length=100, blank=True, null=True)
    building = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100, blank=True, null=True)
    longitude = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = m_state


class Cuisine(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = m_state


class Days_left(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    days = models.IntegerField()

    def __str__(self):
        return self.days

    class Meta:
        managed = True


class UserRequest(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    service_type = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)
    service_status = models.BooleanField(default=True)
    match_status = models.BooleanField(default=False)

    def __str__(self):
        return self.service_type

    class Meta:
        managed = True


def in_one_day():
    return timezone.now() + timedelta(days=1)


class UserRequestMatch(models.Model):
    user1 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user1",
    )
    user2 = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user2",
    )
    match_time = models.DateTimeField(default=in_one_day)

    def __str__(self):
        import pdb

        pdb.set_trace()
        return "Match for " + self.user1.username + " and " + self.user2.username
