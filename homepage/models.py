from django.db import models

class School(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    # id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'school'
        
class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    school = models.IntegerField(blank=True, null=True)
    # id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'department'

class Restaurant(models.Model):
    # id = models.IntegerField(blank=True, null=True)
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

    class Meta:
        managed = False
        db_table = 'restaurant'

# class ServiceType(models.Model):
#     name = models.CharField(max_length=100, blank=True, null=True)
#     # id = models.IntegerField(blank=True, null=True)
#     description = models.CharField(max_length=100, blank=True, null=True)
#     # cuisine = models.CharField(max_length=100, blank=True, null=True)
#
#     class Meta:
#         managed = False
#         db_table = 'service_type'


class UserRequest(models.Model):
    user_id = models.IntegerField()
    service_type = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add = True)
    exp_time = models.DateField(auto_now=False, auto_now_add=False)
    cuisine = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'userrequest'

class ServiceType(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    # id = models.IntegerField(blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    # cuisine = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'service_type'