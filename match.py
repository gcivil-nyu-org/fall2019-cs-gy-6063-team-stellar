import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()

from homepage.models import UserRequest, Cuisine
from user_account.models import LunchNinjaUser
import random
import time
from django.core.mail import EmailMessage



# send_email() will trigger mailtrap to send out email to matched users
def send_email(user1, user2):
    email_subject = "Lunch Confirmation"
    message = (
        "You got it! You will have a lunch with the user "
        + user2.username
        + "("
        + user2.email
        + ")."
    )
    to_email = user1.email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


# initiate_email() takes in matching result and call send_email() by 1 email/5 second rate
def initiate_email(match):
    for each in match:
        print(each[0])
        print(each[1])
        user1 = LunchNinjaUser.objects.get(id=each[0])
        user2 = LunchNinjaUser.objects.get(id=each[1])
        time.sleep(5)
        send_email(user1, user2)
        time.sleep(5)
        send_email(user2, user1)


def create_cuisine_table(cuisine_list, reqlist):
    cuisine_table = {}
    for cuisine in cuisine_list:
        cuisine_table[cuisine] = []
    for req in reqlist:
        real_p_cuisine_list = req.cuisines.all()
        for c in real_p_cuisine_list:
            cuisine_table[c].append(req.user_id)

    return cuisine_table


cuisine_list = Cuisine.objects.all()
reqlist = UserRequest.objects.all()
cuisine_table = create_cuisine_table(cuisine_list, reqlist)


def cuisine_filter(matchpool, available_set, req):
    # get the preferred cuisine
    cuisine_list = req.cuisines.all()
    for c in cuisine_list:
        available_set = available_set.union(set(cuisine_table[c]))
    available_set = available_set.intersection(matchpool)
    return available_set


# def matched_user_filter(matchpool,available_set,user):
#     user_meet_history = user['meet_history']
#     # remove met users
#     if not len(user_meet_history) == 0:
#         for u in user_meet_history:
#             available_set.remove(u[0])
#     return available_set


def match(reqlist, cuisine_table):
    match_result = []
    unmached_user_list = []
    matched_user_list = []
    matchpool = set()

    for req in reqlist:
        matchpool.add(req.user_id)

    # match each user
    for req in reqlist:
        user_id = req.user_id

        if user_id in matchpool:
            # remove selected user
            matchpool.remove(user_id)

            # find available users for this user(filter)
            available_set = set()
            available_set = cuisine_filter(matchpool, available_set, req)
            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                match_user_id = random.choice(list(available_set))
                match_user = UserRequest.objects.filter(user_id=match_user_id)
                matchpool.remove(match_user_id)
                # result = str(user_id) + "----" + str(match_user_id)
                result = []
                result.append(user_id)
                result.append(match_user_id)
                match_result.append(result)
                matched_user_list.append(req)
                matched_user_list.append(match_user)
            except Exception:
                unmached_user_list.append(req)
    print(match_result)
    initiate_email(match_result)
    print(matched_user_list)
    print(unmached_user_list)


match(reqlist, cuisine_table)
