import os
import math
import random
import django
from django.core.mail import EmailMessage
import numpy as np
import datetime
import requests
import json
from email.mime.base import MIMEBase


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
        rest = Restaurant.objects.filter(cuisine=cui)
        restaurantset = restaurantset.union(set(rest))
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


def send_invitations(userRequest, userMatch):
    # Send email to matched users

    user1Email = userRequest[0].user.email
    user2Email = userRequest[1].user.email
    match_time = userMatch.match_time

    user1Cuisines = userRequest[0].cuisines.all()
    user2Cuisines = userRequest[1].cuisines.all()

    commonCuisines = list(user1Cuisines & user2Cuisines)

    resturants = recommend_restaurants(
        userRequest[0].user, userRequest[1].user, commonCuisines
    )

    CRLF = "\r\n"
    organizer = "ORGANIZER;CN=organiser:mailto:teamstellarse" + CRLF + " @gmail.com"

    dur = datetime.timedelta(hours=1)

    dtend = match_time + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = match_time.strftime("%Y%m%dT%H%M%S")
    dtend = dtend.strftime("%Y%m%dT%H%M%S")
    message = (
        "You got it! You have been matched with a NYU member. "
        + "\n"
        + "\n"
        + "Your match was based on your preferred department and cuisine type(s): "
        + " ".join(str(cuisine) for cuisine in commonCuisines)
        + "\n"
        + "\n"
        + "Here are recommanded restaurants based on both of your locations and cuisines types:\n"
    )  # noqa: E501

    for resturant in resturants:
        url = "https://api.yelp.com/v3/businesses/search"

        # In the dictionary, term can take values like food, cafes or businesses like McDonalds
        params = {
            "term": resturant.name.capitalize(),
            "location": resturant.building
            + " "
            + resturant.street
            + ", "
            + resturant.borough,
        }  # noqa: E501
        req = requests.get(url, params=params, headers=headers)

        # proceed only if the status code is 200
        # print('The status code is {}'.format(req.status_code))
        yelp_result = json.loads(req.text)

        address = (
            "address: "
            + resturant.building
            + " "
            + resturant.street
            + ", "
            + resturant.borough
            + "\n"
        )
        yelp_link = (
            "Yelp link for this restaurant is "
            + yelp_result["businesses"][0]["url"]
            + "\n"
        )
        message = message + resturant.name + "; " + address + yelp_link

    attendees = [user1Email, user2Email]
    # attendees = ["utkarshprakash21@gmail.com", "monsieurutkarsh@gmail.com"]

    description = "DESCRIPTION: test invitation from pyICSParser" + CRLF
    attendee = ""
    for att in attendees:
        attendee += (
            "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-    PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE"
            + CRLF
            + " ;CN="
            + att
            + ";X-NUM-GUESTS=0:"
            + CRLF
            + " mailto:"
            + att
            + CRLF
        )
    ical = (
        "BEGIN:VCALENDAR"
        + CRLF
        + "PRODID:pyICSParser"
        + CRLF
        + "VERSION:2.0"
        + CRLF
        + "CALSCALE:GREGORIAN"
        + CRLF
    )
    ical += (
        "METHOD:REQUEST"
        + CRLF
        + "BEGIN:VEVENT"
        + CRLF
        + "DTSTART:"
        + dtstart
        + CRLF
        + "DTEND:"
        + dtend
        + CRLF
        + "DTSTAMP:"
        + dtstamp
        + CRLF
        + organizer
        + CRLF
    )
    ical += "UID:FIXMEUID" + dtstamp + CRLF
    ical += (
        attendee
        + "CREATED:"
        + dtstamp
        + CRLF
        + description
        + "LAST-MODIFIED:"
        + dtstamp
        + CRLF
        + "LOCATION:"
        + CRLF
        + "SEQUENCE:0"
        + CRLF
        + "STATUS:CONFIRMED"
        + CRLF
    )
    ical += (
        "SUMMARY:LunchNinja lunch"
        + CRLF
        + "TRANSP:OPAQUE"
        + CRLF
        + "END:VEVENT"
        + CRLF
        + "END:VCALENDAR"
        + CRLF
    )

    ical_atch = MIMEBase("application/ics", ' ;name="%s"' % ("invite.ics"))
    ical_atch.set_payload(ical)

    email = EmailMessage(
        "LunchNinja Match found!!", message, "teamstellarse@gmail.com", attendees
    )
    email.attach(ical_atch)
    email.send()
    # import pdb
    #
    # pdb.set_trace()


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
    # print("users")
    # print(users)

    for each in users:
        ur = UserRequest.objects.filter(user_id=each.id)
        # print("ur")
        # print(set(ur))
        available_set = available_set.union(set(ur))
    # print("available set")
    # print(available_set)
    available_set = available_set.intersection(matchpool)
    return available_set


def save_matches(matches):
    # save matches to user_request_match table
    for match in matches:
        user1 = match[0].user
        user2 = match[1].user
        request_match = UserRequestMatch(user1=user1, user2=user2)
        request_match.save()
        send_invitations(match, request_match)

        # if user_id in matchpool:
        #     #remove selected user
        #     matchpool.remove(user_id)


def find_match_user(available_set):

    match_request = random.choice(list(available_set))
    return match_request

def creat_match_matrix(matchpool,preference_score):
    match_matrix=np.zeros((len(matchpool),len(matchpool)))

    for user_r in matchpool:
        available_set_cuisine=cuisine_filter(matchpool,user_r)
        available_set_single_department=single_department_filter(matchpool,user_r)
        available_set_same_department=same_department_filter(matchpool,user_r)
        available_set_dual_department=dual_department_filter(matchpool,user_r)
        return 0
def match():
    creat_match_matrix()


match()
