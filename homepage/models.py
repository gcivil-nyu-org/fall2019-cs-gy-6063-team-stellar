from django.db import models
# Create your models here.

class UserRequest(models.Model):
    user_id = models.IntegerField()
    service_type = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(auto_now_add = True)
    exp_time = models.DateField(auto_now=False, auto_now_add=False)
    cuisine = models.CharField(max_length=100)

