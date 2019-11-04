from django.db import models


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
    user_id = models.IntegerField()
    days = models.IntegerField()

    def __str__(self):
        return self.days

    class Meta:
        managed = True


class UserRequest(models.Model):
    user_id = models.IntegerField()
    service_type = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add=True)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    school = models.CharField(max_length=100, blank=True, null=True)
    department = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return self.service_type

    class Meta:
        managed = True
