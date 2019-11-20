from django.db import models
from django.conf import settings
from datetime import timedelta, datetime
from django.utils import timezone

m_state = False


class School(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name

    class Meta:
        managed = m_state


class Department(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, blank=True, null=True)

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


class Interests(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = m_state


class Restaurant(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    cuisine = models.CharField(max_length=100, blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    borough = models.CharField(max_length=100, blank=True, null=True)
    building = models.CharField(max_length=100, blank=True, null=True)
    street = models.CharField(max_length=100, blank=True, null=True)
    zipcode = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.FloatField()
    longitude = models.FloatField()

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


class Days(models.Model):
    DAYS_OF_WEEK = (
        (0, "Monday"),
        (1, "Tuesday"),
        (2, "Wednesday"),
        (3, "Thursday"),
        (4, "Friday"),
        (5, "Saturday"),
        (6, "Sunday"),
    )
    day = models.CharField(max_length=8, choices=DAYS_OF_WEEK)

    def __str__(self):
        return self.day

    class Meta:
        managed = False


class UserRequest(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    service_type = models.CharField(max_length=100)
    time_stamp = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    cuisines = models.ManyToManyField(Cuisine, blank=True)
    interests = models.ManyToManyField(Interests, blank=True)
    # school = models.CharField(max_length=100, blank=True, null=True)
    # department = models.CharField(max_length=200, blank=True, null=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service_status = models.BooleanField(default=True)
    match_status = models.BooleanField(default=False)
    cuisines_priority = models.IntegerField(default=10)
    department_priority = models.IntegerField(default=10)
    interests_priority = models.IntegerField(default=10)
    available_date = models.DateField(null=False, blank=False, auto_now_add=False)
    days = models.ManyToManyField(Days)

    def __str__(self):
        return self.service_type

    class Meta:
        managed = True


def in_one_day():
    # next_day = timezone.now() + timedelta(days=1)
    next_day = timezone.now() + timedelta(days=1)
    new_period = next_day.replace(hour=12, minute=00)
    return new_period


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
    restaurants = models.ManyToManyField(Restaurant, blank=True)

    def __str__(self):
        return "Match for " + self.user1.username + " and " + self.user2.username


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")
    label = models.CharField(max_length=200)

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    was_published_recently.admin_order_field = "pub_date"
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently?"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Feedback(models.Model):
    id = models.IntegerField(primary_key=True)
    match = models.ForeignKey(UserRequestMatch, on_delete=models.CASCADE)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="%(class)s_user1",
    )

    choices = models.ManyToManyField(Choice, blank=True)
    comment = models.CharField(max_length=200)


# UserRequestMatch.objects.
