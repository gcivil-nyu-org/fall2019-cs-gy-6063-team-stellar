import os
import time
import math
import random
import django
from django.core.mail import EmailMessage

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from homepage.models import (
    UserRequest,
    UserRequestMatch,
    Restaurant,
    School,
)  # noqa: E402
from user_account.models import LunchNinjaUser  # noqa: E402


# getDistanceFromLatLonInKm takes in two sets of latitude and longitude, return the distance
def getDistanceFromLatLonInKm(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dLat = deg2rad(lat2 - lat1)  # deg2rad below
    dLon = deg2rad(lon2 - lon1)
    a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(deg2rad(lat1)) * math.cos(
        deg2rad(lat2)
    ) * math.sin(dLon / 2) * math.sin(dLon / 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    d = R * c
    # Distance in km
    return d


# deg2rad take in degree and return radian
def deg2rad(deg):
    return deg * (math.pi / 180)


def recommend_restaurants(user1, user2, cuisinelist):
    school1 = School.objects.get(name=user1.school)
    school2 = School.objects.get(name=user2.school)
    restaurantset = set()
    for cui in cuisinelist:
        rest = Restaurant.objects.filter(cuisine=cui)
        restaurantset = restaurantset.union(set(rest))
    print("restaurantste count is")
    print(len(restaurantset))
    close_to_1 = set()
    close_to_2 = set()
    for each in restaurantset:
        if (
            getDistanceFromLatLonInKm(
                school1.latitude, school1.longitude, each.latitude, each.longitude
            )
            < 1
        ):
            close_to_1.add(each)
        else:
            if (
                getDistanceFromLatLonInKm(
                    school2.latitude, school2.longitude, each.latitude, each.longitude
                )
                < 1
            ):
                close_to_2.add(each)

    restautants_1 = {}
    restautants_2 = {}
    if len(close_to_1) != 0:
        restautants_1 = random.sample(list(close_to_1), 1)
    if len(close_to_2) != 0:
        restautants_2 = random.sample(list(close_to_2), 1)
    result = set(restautants_1).union(set(restautants_2))
    result = list(result)
    print("Recommanded restautants:")
    for r in result:
        print("Name: " + r.name + " ; cuisine: " + r.cuisine)
    return result


# send_email() will trigger mailtrap to send out email to matched users
def send_email(user1, user2, cuisinelist):
    restaurantlist = recommend_restaurants(user1, user2, cuisinelist)
    cuisineline = ""
    for i in range(len(cuisinelist)):
        if i == len(cuisinelist) - 1:
            cuisineline = cuisineline + cuisinelist[i].name
        # >>>>>>> e9c9f8b9ea94cc614df13d1faa2baf6b2a6c7be7
        else:
            cuisineline = cuisineline + cuisinelist[i].name + ","
    email_subject = "Lunch Confirmation"

    message = (
        "You got it! You will have a lunch with the user "
        + user2.first_name
        + "("
        + user2.email
        + ").\n"
        + "You have been matched based on cuisine type(s): "
        + cuisineline
        + "\n"
        + "Here are recommanded restaurants based on both of your locations and cuisines types:\n"
    )  # noqa: E501
    for each in restaurantlist:
        address = (
            "address: " + each.building + " " + each.street + ", " + each.borough + "\n"
        )
        message = message + each.name + "; " + address
    email_message = message
    to_email = user1.email
    email = EmailMessage(email_subject, email_message, to=[to_email])
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
        recommend_restaurants(user1, user2, cuisinelist)
        time.sleep(5)
        send_email(user1, user2, cuisinelist)
        time.sleep(5)
        send_email(user2, user1, cuisinelist)


def cuisine_filter(matchpool, req):
    # get the preferred cuisine
    cuisine_list = req.cuisines.all()
    available_set=set()
    for c in cuisine_list:
        available_set = available_set.union(c.userrequest_set.all())
    available_set = available_set.intersection(matchpool)
    return available_set
def dual_department_filter(matchpool, req):
    available_set = set()
    print(req.department)
    print(req.user.department)



    return available_set


def save_matches(matchs):
    # save matches to user_request_match table
    for match in matchs:
        request_match = UserRequestMatch(user1=match[0].user, user2=match[1].user)
        request_match.save()

        # if user_id in matchpool:
        #     #remove selected user
        #     matchpool.remove(user_id)

def find_match_user(available_set):

    match_request = random.choice(list(available_set))
    return match_request


def match():
    match_result = []
    unmached_user_request = []
    matched_user_request = []
    matchpool = set()
    reqlist = UserRequest.objects.all()
    # print(UserRequest.objects.filt="Computer Science"))

    for req in reqlist:
        matchpool.add(req)

    # match each user

    # Round1 dual match
    for req in reqlist:
        if req in matchpool:
            user_id = req.user_id
            matchpool.remove(req)

            # find available users for this user(filter)

            available_set_cuisine = cuisine_filter(matchpool, req)
            available_set_dual_department=dual_department_filter(matchpool, req)
            # available_set = available_set_cuisine
            available_set=available_set_cuisine.intersection(available_set_dual_department)

            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                # find match user in the available set
                match_request = find_match_user(available_set)
                matchpool.remove(UserRequest.objects.get(user_id=match_request.user_id))


                # for test can be removed
                result = []
                result.append(user_id)
                result.append(match_request.user_id)
                match_result.append(result)

                # collect match information
                request_result = []
                request_result.append(req)
                request_result.append(match_request)
                matched_user_request.append(request_result)
            except Exception:
                unmached_user_request.append(req)
    print(match_result)
    print(matched_user_request)
    # save_matches(matched_user_request)
    # initiate_email(matched_user_request)
    # print(unmached_user_request)


match()
