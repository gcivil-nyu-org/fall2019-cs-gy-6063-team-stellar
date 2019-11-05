import os
import random
import time
import django
from django.core.mail import EmailMessage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from homepage.models import UserRequest, UserRequestMatch  # noqa: E402
from user_account.models import LunchNinjaUser  # noqa: E402


# send_email() will trigger mailtrap to send out email to matched users
def send_email(user1, user2, cuisinelist):
    cuisineline = ""
    for i in range(len(cuisinelist)):
        if i == len(cuisinelist) - 1:
            cuisineline = cuisineline + cuisinelist[i].name
        else:
            cuisineline = cuisineline + cuisinelist[i].name + ","
    email_subject = "Lunch Confirmation"
    message = (
        "You got it! You will have a lunch with the user "
        + user2.username
        + "("
        + user2.email
        + ").\n"
        + "We will provide some restaurant recommandations based on both of your preferred cuisine type:\n"
        + cuisineline
    )
    to_email = user1.email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


# initiate_email() takes in matching result and call send_email() by 1 email/5 second rate
def initiate_email(match):
    for each in match:
        req1 = each[0]
        req2 = each[1]

        user1 = LunchNinjaUser.objects.get(id=req1.user_id)
        user2 = LunchNinjaUser.objects.get(id=req2.user_id)
        cuisine_set1 = set(req1.cuisines.all())
        cuisine_set2 = set(req2.cuisines.all())
        cuisinelist = list(cuisine_set1 & cuisine_set2)
        time.sleep(5)
        send_email(user1, user2, cuisinelist)
        time.sleep(5)
        send_email(user2, user1, cuisinelist)


def cuisine_filter(matchpool, available_set, req):
    # get the preferred cuisine
    cuisine_list = req.cuisines.all()
    for c in cuisine_list:
        available_set = available_set.union(c.userrequest_set.all())
    available_set = available_set.intersection(matchpool)
    return available_set


def save_matches(matchs):
    # save matches to user_request_match table
    for match in matchs:
        request_match = UserRequestMatch(user1=match[0].user, user2=match[1].user)
        request_match.save()


def match():
    match_result = []
    unmached_user_request = []
    matched_user_request = []
    matchpool = set()
    reqlist = UserRequest.objects.all()

    for req in reqlist:
        matchpool.add(req)

    # match each user
    for req in reqlist:
        if req in matchpool:
            user_id = req.user_id
            matchpool.remove(req)
            # find available users for this user(filter)
            available_set = set()
            available_set = cuisine_filter(matchpool, available_set, req)
            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                match_request = random.choice(list(available_set))
                match_user_id = match_request.user_id
                # match_user_id = random.choice(list(available_set))
                matchpool.remove(UserRequest.objects.get(user_id=match_user_id))
                # result = str(user_id) + "----" + str(match_user_id)
                result = []
                result.append(user_id)
                result.append(match_user_id)
                match_result.append(result)
                request_result = []
                request_result.append(req)
                request_result.append(match_request)
                matched_user_request.append(request_result)
            except Exception:
                unmached_user_request.append(req)
    print(match_result)
    print(matched_user_request)
    save_matches(matched_user_request)
    # initiate_email(matched_user_request)
    print(unmached_user_request)


match()
