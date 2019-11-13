import os
import math
import random
import django
from django.core.mail import EmailMessage
import numpy as np
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
import datetime
import requests
import json
import time
from django.db.models import Q

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
            < 3
        ):
            close_to_1.append(each)
        else:
            if (
                getDistanceFromLatLonInKm(
                    school2.latitude, school2.longitude, each.latitude, each.longitude
                )
                < 3
            ):
                close_to_2.append(each)

    restautants_1 = {}
    restautants_2 = {}
    if len(close_to_1) != 0:
        try:
            restautants_1 = random.sample(close_to_1, 5)
        except Exception:
            restautants_1 = random.sample(close_to_1, 1)
        # restautants_1 = random.sample(list(close_to_1), 1)
    if len(close_to_2) != 0:
        try:
            restautants_2 = random.sample(close_to_2, 5)
        except Exception:
            restautants_2 = random.sample(close_to_2, 1)
    # print("In restaurant, restaurant1 is")
    # print(restautants_1)
    return restautants_1, restautants_2


def get_yelp_link(restaurant):
    url = "https://api.yelp.com/v3/businesses/search"

    # In the dictionary, term can take values like food, cafes or businesses like McDonalds
    params = {
        "term": restaurant.name.capitalize(),
        "location": restaurant.building
        + " "
        + restaurant.street
        + ", "
        + restaurant.borough,
    }  # noqa: E501
    req = requests.get(url, params=params, headers=headers)
    # proceed only if the status code is 200
    if not req.status_code == 200:
        return -1
    yelp_result = json.loads(req.text)
    if len(yelp_result["businesses"]) == 0:
        return -1
    yelp_link = yelp_result["businesses"][0]["url"]
    return yelp_link


def compose_email(
    userRequest1,
    userRequest2,
    restaurants1,
    restaurants2,
    cuisine_names,
    interests_names,
):
    html_content = (
        "<p>Hi "
        + userRequest1.user.first_name
        + ",</p>"
        + "You got it! You have been matched with "
        + "<b>"
        + userRequest2.user.first_name
        + " "
        + userRequest2.user.last_name
        + "</b> ("
        + userRequest2.user.email
        + ")"
        + " from "
        + userRequest2.user.department
        + " department at "
        + userRequest2.user.school
        + ". "
        + "<h3><b>Your match was based on your preferrences:-</b></h3>"
        + "<p><b> School & Department: </b>"
        + userRequest1.school
        + ", "
        + userRequest1.department
        + "</p>"
        + "<p><b> Common cuisines: </b>"
        + str(cuisine_names)
        + "</p>"
        + "<p><b> Common conversation interests: </b>"
        + str(interests_names)
        + "</p>"
        + "<h3>Here are recommended restaurants based on both of your locations, cuisines types and NYC Health Department inspection score:-</h3>"
    )

    # Add restaurant near school1
    if not len(restaurants1) == 0:
        html_content = html_content + "<u><i>Restaurants near your school:</i></u>"
        for i, resturant in enumerate(restaurants1):
            link = get_yelp_link(resturant)

            html_content = (
                html_content
                + "<p><b>"
                + str(i + 1)
                + ") "
                + resturant.name.capitalize()
                + "</b></p>"
            )
            address = (
                "Address: "
                + resturant.building
                + " "
                + resturant.street
                + ", "
                + resturant.borough
                + " "
                + str(resturant.zipcode)
            )
            html_content = html_content + "<p>" + address + "</p>"
            if not link == -1:
                html_content = html_content + "Yelp link: "
                html_content = html_content + "<div>" + link + "</div>"

    # Add restaurant near school2
    if not len(restaurants2) == 0:
        html_content = (
            html_content
            + "<br style=“line-height:2;”<u><i>Restaurants near your lunch partner's school:</i></u>"
        )
        for i, resturant in enumerate(restaurants2):
            link = get_yelp_link(resturant)

            html_content = (
                html_content
                + "<p><b>"
                + str(i + 1)
                + ") "
                + resturant.name.capitalize()
                + "</b></p>"
            )
            address = (
                "Address: "
                + resturant.building
                + " "
                + resturant.street
                + ", "
                + resturant.borough
                + " "
                + str(resturant.zipcode)
            )
            html_content = html_content + "<p>" + address + "</p>"
            if not link == -1:
                html_content = html_content + "Yelp link: "
                html_content = html_content + "<div>" + link + "</div>"

    # Add image
    html_content = html_content + '<p><img src="cid:myimage" /></p>'
    html_content = html_content + "<p>Bon appétit!</p>"
    html_content = html_content + "<p>Lunch Ninja</p>"
    return html_content


def send_email(html_content, ical_atch, attendee):
    img_data = open("homepage/static/img/catcopy.jpg", "rb").read()
    html_part = MIMEMultipart(_subtype="related")
    # body = MIMEText('<p>Hello <img src="cid:myimage" /></p>', _subtype='html')
    body = MIMEText(html_content, _subtype="html")
    html_part.attach(body)
    # Now create the MIME container for the image
    img = MIMEImage(img_data, "jpg")
    img.add_header("Content-Id", "<myimage>")  # angle brackets are important
    img.add_header("Content-Disposition", "inline", filename="myimage")
    html_part.attach(img)
    msg = EmailMessage(
        "LunchNinja Match found!!", None, "teamstellarse@gmail.com", attendee
    )
    msg.attach(
        html_part
    )  # Attach the raw MIMEBase descendant. This is a public method on EmailMessage
    msg.attach(ical_atch)
    time.sleep(5)
    print("sending out email")
    msg.send()


def send_invitations(userRequest, userMatch):
    # Send email to matched users

    user1Email = userRequest[0].user.email
    user2Email = userRequest[1].user.email
    match_time = userMatch.match_time

    user1Cuisines = userRequest[0].cuisines.all()
    user2Cuisines = userRequest[1].cuisines.all()

    commonCuisines = list(user1Cuisines & user2Cuisines)
    cuisine_names = ", ".join(
        [cuisine.name for cuisine in (user1Cuisines & user2Cuisines)]
    )

    user1Interests = userRequest[0].interests.all()
    user2Interests = userRequest[0].interests.all()

    interests_name = ", ".join(
        [interest.name for interest in (user1Interests & user2Interests)]
    )

    restaurants1, restaurants2 = recommend_restaurants(
        userRequest[0].user, userRequest[1].user, commonCuisines
    )

    CRLF = "\r\n"
    organizer = "ORGANIZER;CN=organiser:mailto:teamstellarse" + CRLF + " @gmail.com"

    dur = datetime.timedelta(hours=1)

    dtend = match_time + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = match_time.strftime("%Y%m%dT%H%M%S")
    dtend = dtend.strftime("%Y%m%dT%H%M%S")

    attendees = [user1Email, user2Email]
    # attendees = ["utkarshprakash21@gmail.com", "monsieurutkarsh@gmail.com"]

    description = (
        "DESCRIPTION: Lunch meeting with"
        + userRequest[1].user.first_name
        + " "
        + userRequest[1].user.last_name
        + "</b>("
        + userRequest[1].user.email
        + ")"
        + CRLF
    )
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

    to1 = [attendees[0]]
    to2 = [attendees[1]]
    html_content = compose_email(
        userRequest[0],
        userRequest[1],
        restaurants1,
        restaurants2,
        cuisine_names,
        interests_name,
    )
    send_email(html_content, ical_atch, to1)
    html_content = compose_email(
        userRequest[1],
        userRequest[0],
        restaurants1,
        restaurants2,
        cuisine_names,
        interests_name,
    )
    send_email(html_content, ical_atch, to2)


def cuisine_filter(matchpool, req):
    # get the preferred cuisine
    cuisine_list = req.cuisines.all()
    available_set = set()
    for c in cuisine_list:
        available_set = available_set.union(c.userrequest_set.all())
    available_set = available_set.intersection(matchpool)

    return available_set


def interest_filter(matchpool, req):
    # get the preferred cuisine
    interests_list = req.interests.all()
    available_set = set()
    for i in interests_list:
        available_set = available_set.union(i.userrequest_set.all())
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

    for user in users:
        user_request = UserRequest.objects.filter(user_id=user.id)
        available_set = available_set.union(set(user_request))

    available_set = available_set.intersection(matchpool)
    return available_set


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
        request_match = UserRequestMatch(user1=user1, user2=user2)
        request_match.save()
        for r in restaurants1:
            request_match.restaurants.add(r)
        for r in restaurants2:
            request_match.restaurants.add(r)
        send_invitations(match, request_match)


def find_match_user(available_set):

    match_request = random.choice(list(available_set))
    return match_request


def get_matchpool():
    matchpool = set()
    reqlist = []
    days_entry = Days_left.objects.filter(days=1)
    for day in days_entry:
        user = day.user
        matchpool.add(UserRequest.objects.get(user_id=user.id))
        reqlist.append(UserRequest.objects.get(user_id=user.id))
    return matchpool, reqlist


# Create match matrix for matching. The value in the matrix indicate the score two of each possible matches
def creat_match_matrix(matchpool, matchlist, preference_score):
    match_matrix = np.zeros((len(matchpool), len(matchpool)))
    for user_r in matchlist:

        # calculate the score for each preference
        cuisine_score = user_r.cuisines_priority * 10
        same_department_score = user_r.department_priority * 10
        single_department_score = user_r.department_priority * 10
        dual_department_score = 100
        interest_score = user_r.interests_priority * 10
        match_history = UserRequestMatch.objects.filter(
            Q(user1=user_r.user) | Q(user2=user_r.user)
        )

        for matched_user in match_history:
            # users cannot match matched users
            user1 = UserRequest.objects.filter(user_id=matched_user.user1_id)[0]
            user2 = UserRequest.objects.filter(user_id=matched_user.user2_id)[0]
            match_matrix[matchlist.index(user1)][matchlist.index(user2)] = -1000
            match_matrix[matchlist.index(user2)][matchlist.index(user1)] = -1000
        # find all possible matches base on the users preference
        available_set_cuisine = cuisine_filter(matchpool, user_r)
        available_set_interest = interest_filter(matchpool, user_r)
        available_set_single_department = single_department_filter(matchpool, user_r)
        available_set_same_department = same_department_filter(matchpool, user_r)
        available_set_dual_department = dual_department_filter(matchpool, user_r)

        # calculate scores for each possible matches
        for user_m in matchlist:
            matched_prefer = 0
            if user_m in available_set_cuisine:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] += cuisine_score
                matched_prefer += 1
            else:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] -= cuisine_score
            # for user_m in matchlist:
            if user_m in available_set_interest:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] += interest_score
                matched_prefer += 1
            else:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] -= interest_score
            # for user_m in matchlist:
            if user_m in available_set_single_department:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] += single_department_score

            else:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] -= single_department_score
            # for user_m in matchlist:
            if user_m in available_set_same_department:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] += same_department_score

            else:
                match_matrix[matchlist.index(user_r)][matchlist.index(user_m)] -= 0
            # for user_m in matchlist:
            if user_m in available_set_dual_department:
                match_matrix[matchlist.index(user_r)][
                    matchlist.index(user_m)
                ] += dual_department_score
                matched_prefer += 1
            else:
                match_matrix[matchlist.index(user_r)][matchlist.index(user_m)] -= 0
            if matched_prefer >= 3:
                match_matrix[matchlist.index(user_r)][matchlist.index(user_m)] = 1000
        # user cannot match themselves
        match_matrix[matchlist.index(user_r)][matchlist.index(user_r)] = -1000
        # if the user turn off the service he will not be considered
        if not user_r.service_status:
            for i in range(0, len(matchlist)):
                match_matrix[matchlist.index(user_r)][i] = -1000
                match_matrix[i][matchlist.index(user_r)] = -1000
    # print(match_matrix)
    return match_matrix


# match users base on match matrix
# The matches with highest score will be consider first
def match():
    matchpool, reqlist = get_matchpool()
    preference_score = {
        "cuisine": 10,
        "interest": 10,
        "same department": 10,
        "single department": 10,
        "dual department": 100,
    }
    matchlist = []
    for user in matchpool:
        matchlist.append(user)
    match_matrix = creat_match_matrix(matchpool, matchlist, preference_score)
    match_score_list = []

    for i in range(0, len(matchlist)):

        for j in range(0, len(matchlist)):
            bi_score = match_matrix[i][j] + match_matrix[j][i]
            match_score_list.append((i, j, bi_score))

    def take_2(elem):
        return elem[2]

    # print(match_score_list)
    random.shuffle(match_score_list)
    match_score_list.sort(key=take_2, reverse=True)
    # print(match_score_list)
    matched_user_request = []
    matched_user = []
    not_matched_user = []

    for user_tuple in match_score_list:
        if user_tuple[2] < 0:
            continue
        user_num1 = user_tuple[0]
        user_num2 = user_tuple[1]
        user1 = matchlist[user_num1]
        user2 = matchlist[user_num2]
        if user1 in matchpool and user2 in matchpool:
            matched_user.append([user1.user_id, user2.user_id])
            matched_user_request.append([user1, user2])

            matchpool.remove(user1)
            matchpool.remove(user2)
    for user in matchpool:
        not_matched_user.append(user)
    save_matches(matched_user_request)


match()
