import os
import math
import random
import django
from django.utils import timezone
from datetime import timedelta

api_key = "K5_zpUoEf7tPJvKRp6e8UrGB5lLzW6Ik5iFZ4E9xn6PnqafYRSHFGac6QOfdLLw67bj66fDkaZEXXNiHMm65nujAFr3SBNu7PcupsYc8_gXI59fsGkH__Z04L-3IXXYx"
headers = {"Authorization": "Bearer %s" % api_key}
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from homepage.models import (
    UserRequest,
    UserRequestMatch,
    Restaurant,
    School,
    Days_left,
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
        rest = Restaurant.objects.filter(cuisine=cui).order_by("score")
        restaurantset = restaurantset.union(set(rest))
    close_to_1 = []
    close_to_2 = []
    for each in restaurantset:
        if (
            getDistanceFromLatLonInKm(
                school1.latitude, school1.longitude, each.latitude, each.longitude
            )
            < 2
        ):
            close_to_1.append(each)
        else:
            if (
                getDistanceFromLatLonInKm(
                    school2.latitude, school2.longitude, each.latitude, each.longitude
                )
                < 2
            ):
                close_to_2.append(each)

    restautants_1 = {}
    restautants_2 = {}
    if len(close_to_1) >= 5:
        try:
            restautants_1 = random.sample(close_to_1, 5)
        except Exception:
            restautants_1 = random.sample(close_to_1, len(close_to_1))
        # restautants_1 = random.sample(list(close_to_1), 1)
    if len(close_to_2) >= 5:
        try:
            restautants_2 = random.sample(close_to_2, 5)
        except Exception:
            restautants_2 = random.sample(close_to_2, len(close_to_2))
    return restautants_1, restautants_2


def cuisine_filter(matchpool, req):
    # get the preferred cuisine
    cuisine_list = req.cuisines.all()
    available_set = set()
    for c in cuisine_list:
        available_set = available_set.union(c.userrequest_set.all())
    available_set = available_set.intersection(matchpool)

    return available_set


def dual_department_filter(matchpool, req):
    available_set_A = set()
    A_users = LunchNinjaUser.objects.filter(department=req.department)
    for each in A_users:
        ur = UserRequest.objects.filter(user_id=each.id)
        available_set_A = available_set_A.union(set(ur))

    B = UserRequest.objects.filter(department=req.user.department)
    M_A_B = available_set_A.intersection(set(B))
    available_set = M_A_B
    available_set = available_set.intersection(matchpool)
    return available_set


def single_department_filter(matchpool, req):
    available_set = set()
    users = LunchNinjaUser.objects.filter(department=req.department)
    for each in users:
        ur = UserRequest.objects.filter(user_id=each.id)
        available_set = available_set.union(set(ur))
    available_set = available_set.intersection(matchpool)
    return available_set


def same_department_filter(matchpool, req):
    available_set = set()
    users = LunchNinjaUser.objects.filter(department=req.user.department)

    for each in users:
        ur = UserRequest.objects.filter(user_id=each.id)
        available_set = available_set.union(set(ur))
    available_set = available_set.intersection(matchpool)
    return available_set

def day_before():
    next_day = timezone.now() - timedelta(days=random.randint(1,10))
    new_period = next_day.replace(hour=12, minute=00)
    return new_period

def save_matches(matches):
    # save matches to user_request_match table
    for match in matches:
        user1 = match[0].user
        user2 = match[1].user
        ur1 = UserRequest.objects.get(user_id=user1.id)
        ur2 = UserRequest.objects.get(user_id=user2.id)

        user1Cuisines = ur1.cuisines.all()
        user2Cuisines = ur2.cuisines.all()

        commonCuisines = list(user1Cuisines & user2Cuisines)
        restaurants1, restaurants2 = recommend_restaurants(user1, user2, commonCuisines)
        request_match = UserRequestMatch(user1=user1, user2=user2, match_time=day_before())
        request_match.save()
        for r in restaurants1:
            request_match.restaurants.add(r)
        for r in restaurants2:
            request_match.restaurants.add(r)

        # if user_id in matchpool:
        #     #remove selected user
        #     matchpool.remove(user_id)


def find_match_user(available_set):

    match_request = random.choice(list(available_set))
    return match_request


def get_matchpool():
    matchpool = set()
    reqlist = []
    days_entry = Days_left.objects.filter(days=1)
    # print(UserRequest.objects.filt="Computer Science"))
    for day in days_entry:
        user = day.user
        matchpool.add(UserRequest.objects.get(user_id=user.id))
        reqlist.append(UserRequest.objects.get(user_id=user.id))
    return matchpool, reqlist


def match():
    match_result1 = []
    match_result2 = []
    match_result3 = []
    match_result4 = []

    matched_user_request_1 = []
    matched_user_request_2 = []
    matched_user_request_3 = []
    matched_user_request_4 = []
    matchpool, reqlist = get_matchpool()
    print("matchpool is")
    print(matchpool)
    # match each user
    # Round1 dual match
    Round1 = matchpool
    unmatched_user = []
    for req in reqlist:
        if req in Round1:
            user_id = req.user_id
            Round1.remove(req)

            # find available users for this user(filter)

            available_set_cuisine = cuisine_filter(Round1, req)

            available_set_dual_department = dual_department_filter(Round1, req)

            # available_set = available_set_cuisine
            available_set = available_set_cuisine.intersection(
                available_set_dual_department
            )

            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                # find match user in the available set
                match_request = find_match_user(available_set)
                Round1.remove(UserRequest.objects.get(user_id=match_request.user_id))

                # for test can be removed
                result1 = []
                result1.append(user_id)
                result1.append(match_request.user_id)
                match_result1.append(result1)

                # collect match information
                request_result_1 = []
                request_result_1.append(req)
                request_result_1.append(match_request)
                matched_user_request_1.append(request_result_1)
            except Exception:
                unmatched_user.append(req)
    # Round2 part match
    Round2 = set(unmatched_user)
    unmatched_user = []
    i = 0
    for req in reqlist:
        i += 1
        if req in Round2:
            user_id = req.user_id
            Round2.remove(req)
            # find available users for this user(filter)
            available_set_cuisine = cuisine_filter(Round2, req)
            available_set_single_department = single_department_filter(Round2, req)
            # available_set = available_set_cuisine
            available_set = available_set_cuisine.intersection(
                available_set_single_department
            )

            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                # find match user in the available set
                match_request = find_match_user(available_set)
                Round2.remove(UserRequest.objects.get(user_id=match_request.user_id))

                # for test can be removed
                result2 = []
                result2.append(user_id)
                result2.append(match_request.user_id)
                match_result2.append(result2)

                # collect match information
                request_result_2 = []
                request_result_2.append(req)
                request_result_2.append(match_request)
                matched_user_request_2.append(request_result_2)
            except Exception:
                unmatched_user.append(req)
                Round2.add(req)

    # Round3 part match
    Round3 = set(unmatched_user)
    unmatched_user = []
    for req in reqlist:
        if req in Round3:
            user_id = req.user_id
            Round3.remove(req)
            # find available users for this user(filter)
            available_set_cuisine = cuisine_filter(Round3, req)

            available_set_same_department = same_department_filter(Round3, req)
            # available_set = available_set_cuisine
            available_set = available_set_cuisine.intersection(
                available_set_same_department
            )

            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                # find match user in the available set
                match_request = find_match_user(available_set)
                Round3.remove(UserRequest.objects.get(user_id=match_request.user_id))

                # for test can be removed
                result3 = []
                result3.append(user_id)
                result3.append(match_request.user_id)
                match_result3.append(result3)

                # collect match information
                request_result_3 = []
                request_result_3.append(req)
                request_result_3.append(match_request)
                matched_user_request_3.append(request_result_3)
            except Exception:
                unmatched_user.append(req)
    print(unmatched_user)

    # Round4 cuisine match
    Round4 = set(unmatched_user)
    unmatched_user = []
    for req in reqlist:
        if req in Round4:
            user_id = req.user_id
            Round4.remove(req)
            # find available users for this user(filter)
            available_set_cuisine = cuisine_filter(Round4, req)
            available_set = available_set_cuisine

            # available_set = matched_user_filter(matchpool, available_set, user)

            # pick a user from the available users
            try:
                # find match user in the available set
                match_request = find_match_user(available_set)
                Round4.remove(UserRequest.objects.get(user_id=match_request.user_id))

                # for test can be removed
                result4 = []
                result4.append(user_id)
                result4.append(match_request.user_id)
                match_result4.append(result4)

                # collect match information
                request_result_4 = []
                request_result_4.append(req)
                request_result_4.append(match_request)
                matched_user_request_4.append(request_result_4)
            except Exception:
                unmatched_user.append(req)
    print(unmatched_user)

    print(match_result1)
    print(matched_user_request_1)
    print(match_result2)
    print(matched_user_request_2)
    print(match_result3)
    print(matched_user_request_3)
    print(match_result4)
    print(matched_user_request_4)
    save_matches(
        matched_user_request_1
        + matched_user_request_2
        + matched_user_request_3
        + matched_user_request_4
    )


match()
