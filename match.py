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
from django.db.models import Q

from dateutil.relativedelta import relativedelta

# Yelp API Key
api_key = "K5_zpUoEf7tPJvKRp6e8UrGB5lLzW6Ik5iFZ4E9xn6PnqafYRSHFGac6QOfdLLw67bj66fDkaZEXXNiHMm65nujAFr3SBNu7PcupsYc8_gXI59fsGkH__Z04L-3IXXYx"
headers = {"Authorization": "Bearer %s" % api_key}
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "lunchNinja.settings")
django.setup()
from homepage.models import (
    UserRequest,
    UserRequestMatch,
    Restaurant,
    School,
    Department,
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
    if len(close_to_1) > 5:
        restautants_1 = random.sample(close_to_1, 5)
    else:
        restautants_1 = random.sample(close_to_1, len(close_to_1))
        # restautants_1 = random.sample(list(close_to_1), 1)
    if len(close_to_2) > 5:
        restautants_2 = random.sample(close_to_2, 5)
    else:
        restautants_2 = random.sample(close_to_2, len(close_to_2))
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
        + "<h3><b>Your match was based on your preferrences:</b></h3>"
    )

    if not len(cuisine_names) == 0:
        html_content = (
            html_content + "<p><b> Common cuisines: </b>" + str(cuisine_names) + "</p>"
        )
    else:
        html_content = (
            html_content
            + "<p><b> Common cuisines: </b> You don't have any common cuisine.</p>"
        )

    html_content = (
        html_content
        + "<p><b> School & Department: </b>"
        + userRequest1.school.name
        + ", "
        + userRequest1.department.name
        + "</p>"
    )

    if not len(interests_names) == 0:
        html_content = (
            html_content
            + "<p><b> Common conversation interests: </b>"
            + str(interests_names)
            + "</p>"
        )
    else:
        html_content = (
            html_content
            + "<p><b> Common interests: </b> You don't have any common interests.</p>"
        )

    html_content = (
        html_content
        + "<br><h3><b> Restaurant recommendations</h3>"
        + "<p> NYU offers a wide variety of dining options on campus. To check it out, click "
        + "<a href='"
        + "https://www.nyu.edu/students/student-information-and-resources/housing-and-dining/dining/locations-and-menus.html"
        + "'>"
        + "NYU On-campus Dining"
        + "</a></p><br>"
    )

    # Add restaurant near school1
    if not len(restaurants1) == 0:
        html_content = html_content + "<p><b><i>Restaurants near your school:</p>"
        prevname = ""

        for restaurant in restaurants1:
            if not restaurant.name == prevname:
                link = get_yelp_link(restaurant)
                html_content = (
                    html_content + "<p><b>" + restaurant.name.capitalize() + "</b></p>"
                )
                address = (
                    "Address: "
                    + restaurant.building
                    + " "
                    + restaurant.street
                    + ", "
                    + restaurant.borough
                    + " "
                    + str(restaurant.zipcode)
                )
                html_content = html_content + "<p>" + address + "</p>"
                if not link == -1:
                    html_content = (
                        html_content + "<p> Yelp link for this restaurant is: </p>"
                    )
                    # html_content = (
                    #     html_content
                    #     + '<div> <a herf = "'
                    #     + link
                    #     + '">'
                    #     + restaurant.name.capitalize()
                    #     + "</a></div>"
                    # )
                    link_short = (
                        "<a href='"
                        + link
                        + "'>"
                        + restaurant.name.capitalize()
                        + "</a>"
                    )
                    html_content = html_content + "<div>" + link_short + "</div>"

                prevname = restaurant.name
    if not len(restaurants2) == 0:
        html_content = (
            html_content + "<p><b><i>Restaurants near your lunch partner's school:</p>"
        )
        for resturant in restaurants2:
            prevname = ""

            if not prevname == restaurant.name:
                link = get_yelp_link(resturant)

                html_content = (
                    html_content + "<p><b>" + resturant.name.capitalize() + "</b></p>"
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
                    html_content = (
                        html_content + "<p> Yelp link for this restaurant is: </p>"
                    )

                    link_short = (
                        "<a href='" + link + "'>" + resturant.name.capitalize() + "</a>"
                    )
                    html_content = html_content + "<div>" + link_short + "</div>"
                prevname = restaurant.name

    html_content = (
        html_content + "<br><p><b>" + "Not satisfied with the result?" + "</b></p>"
    )
    html_content = (
        html_content
        + "<a href='http:/lunch-ninja.herokuapp.com/settings'>Change your preference</a>"
    )
    # Add image
    # html_content = html_content + "<p> Not satisfied with the result? </p>"

    html_content = html_content + '<p><img src="cid:myimage" /></p>'
    html_content = html_content + "<p>Bon appétit!</p>"
    html_content = html_content + "<p>Lunch Ninja</p>"
    return html_content


def send_email(html_content, ical_atch, attendee):
    img_data = open("homepage/static/img/cat.jpg", "rb").read()
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
    print("cuisine_names is")
    print(cuisine_names)

    user1Interests = userRequest[0].interests.all()
    user2Interests = userRequest[0].interests.all()

    interests_name = ", ".join(
        [interest.name for interest in (user1Interests & user2Interests)]
    )

    restaurants1, restaurants2 = recommend_restaurants(
        userRequest[0].user, userRequest[1].user, commonCuisines
    )
    print("restaurants1 is")
    print(restaurants1)

    CRLF = "\r\n"
    # organizer = "ORGANIZER;CN=organiser:mailto:teamstellarse" + CRLF + " @gmail.com"
    # organizer = "ORGANIZER;CN=organiser:mailto:teamstellarse@outlook.com"
    # organizer = "ORGANIZER;CN=organiser:mailto:491759343@qq.com"

    dur = datetime.timedelta(hours=1)

    dtend = match_time + dur
    dtstamp = datetime.datetime.now().strftime("%Y%m%dT%H%M%SZ")
    dtstart = match_time.strftime("%Y%m%dT%H%M%S")
    dtend = dtend.strftime("%Y%m%dT%H%M%S")

    attendees = [user1Email, user2Email]
    # attendees = ["utkarshprakash21@gmail.com", "monsieurutkarsh@gmail.com"]

    description = (
        "DESCRIPTION: Lunch meeting: "
        + userRequest[1].user.first_name
        + " "
        + userRequest[1].user.last_name
        + " and "
        + userRequest[0].user.first_name
        + " "
        + userRequest[0].user.last_name
        + CRLF
    )
    attendee = ""
    for att in attendees:
        attendee += (
            "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE"
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
        # "METHOD:REQUEST"
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
        # + organizer
        # + CRLF
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

    A_users = LunchNinjaUser.objects.filter(department=req.department.name)
    for each in A_users:
        ur = UserRequest.objects.filter(user_id=each.id)
        available_set_A = available_set_A.union(set(ur))

    d = Department.objects.filter(name=req.user.department)
    B = UserRequest.objects.filter(department=d[0])
    M_A_B = available_set_A.intersection(set(B))
    available_set = M_A_B
    available_set = available_set.intersection(matchpool)
    return available_set


def single_department_filter(matchpool, req):
    available_set = set()
    users = LunchNinjaUser.objects.filter(department=req.department.name)
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


def begining_of_week(day):
    weekday = day.weekday()
    begining = day - datetime.timedelta(days=weekday)
    return begining


def find_day_prefer(user):
    days = user.days.all()
    if len(days) == 0:
        return 0
    else:
        return user.days.all()[0].id


def change_available_day(user1, user2):
    month = relativedelta(months=1)
    week = datetime.timedelta(weeks=1)
    day = datetime.timedelta(days=1)
    ur1 = UserRequest.objects.get(user_id=user1.id)
    ur2 = UserRequest.objects.get(user_id=user2.id)

    first_available_weekday_u1 = begining_of_week(today) + datetime.timedelta(
        days=find_day_prefer(ur1)
    )
    first_available_weekday_u2 = begining_of_week(today) + datetime.timedelta(
        days=find_day_prefer(ur2)
    )
    if ur1.service_type == "monthly":
        ur1.available_date = first_available_weekday_u1 + month
    elif ur1.service_type == "weekly":
        ur1.available_date = first_available_weekday_u1 + week
    elif ur1.service_type == "daily":
        ur1.available_date = first_available_weekday_u1 + day
    if ur2.service_type == "Monthly":
        ur2.available_date = first_available_weekday_u2 + month
    elif ur2.service_type == "Weekly":
        ur2.available_date = first_available_weekday_u2 + week
    elif ur2.service_type == "Daily":
        ur2.available_date = first_available_weekday_u2 + day
    ur1.save()
    ur2.save()
    return


def save_matches(matches):
    # save matches to user_request_match table
    # month = relativedelta(months=1)
    # week = datetime.timedelta(weeks=1)
    # day = datetime.timedelta(days=1)

    for match in matches:
        print(match)
        user1 = match[0].user
        user2 = match[1].user
        print(user1)
        print(user2)
        print(user1.id)
        print(user2.id)
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


today = datetime.date.today() + datetime.timedelta(days=1)


def get_matchpool():
    matchpool = set()
    reqlist = []

    # today = datetime.date.today()
    print(today)
    available_day_entry = UserRequest.objects.filter(available_date=today)
    # days_entry = Days_left.objects.filter(days=1)
    # for day in days_entry:
    #     user = day.user
    #     matchpool.add(UserRequest.objects.get(user_id=user.id))
    #     reqlist.append(UserRequest.objects.get(user_id=user.id))
    for user in available_day_entry:
        matchpool.add(user)
        reqlist.append(user)
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
            print(matched_user.user1_id)
            print(matched_user.user2_id)
            user1 = UserRequest.objects.filter(user_id=matched_user.user1_id)[0]
            user2 = UserRequest.objects.filter(user_id=matched_user.user2_id)[0]
            if user1 in matchlist and user2 in matchlist:
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
    print(match_score_list)
    for user_tuple in match_score_list:

        if user_tuple[2] < 0:
            continue
        user_num1 = user_tuple[0]
        user_num2 = user_tuple[1]
        user1 = matchlist[user_num1]
        user2 = matchlist[user_num2]
        print("[" + str(user1.user.id) + ", " + str(user2.user.id) + "]")
        if user1 in matchpool and user2 in matchpool:
            matched_user.append([user1.user_id, user2.user_id])
            matched_user_request.append([user1, user2])

            matchpool.remove(user1)
            matchpool.remove(user2)
    for user in matchpool:
        not_matched_user.append(user)
    save_matches(matched_user_request)

    for u in not_matched_user:
        print(u.user.username)

    fake_not_matched_user = []
    for user in not_matched_user:
        prefer_weekday = []
        for d in user.days.all():
            prefer_weekday.append(d.id)
        for i in prefer_weekday:
            if i > today.weekday():
                user.available_date = begining_of_week(today) + datetime.timedelta(
                    days=i
                )
                user.save()
                fake_not_matched_user.append(user)
    real_not_matched_user = []
    for user in not_matched_user:
        if user not in fake_not_matched_user:
            real_not_matched_user.append(user)
    print("matched user")
    print(matched_user_request)
    print("fake not matched user")
    print(fake_not_matched_user)
    print("real_matched_user")
    print(real_not_matched_user)

    return matched_user_request


matched_user_request = match()
userlist = UserRequest.objects.all()
for user in userlist:
    if user in matched_user_request:
        print("Matched")
    print(user.user.username)
    print(user.service_type)
    print(user.days.all())
    print(user.days.all())
    print(user.available_date)


# For testing mathcing algorithm
# def send_test_email():
#     # lookup user by id and send them a message
#     email = EmailMessage("Random Check", "Hi", to=["up293@nyu.edu"])
#     email.send()

# send_test_email()
