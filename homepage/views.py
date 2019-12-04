from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import base64


from .models import (
    UserRequest,
    School,
    Cuisine,
    UserRequestMatch,
    # Days_left,
    Interests,
    Department,
    Days,
    Question,
    Feedback,
)
from user_account.models import LunchNinjaUser
from datetime import datetime, timezone, timedelta, date
from collections import Counter

# Dont remove, for macthing algorithm

# from background_task.models import Task
# from homepage.tasks import run_matching
# new_years_2022 = datetime(2022, 1, 1)
# run_matching(repeat=Task.DAILY, repeat_until=new_years_2022)


# Create your views here.
Service_days = {"Daily": 1, "Weekly": 7, "Monthly": 30}


def get_user(request):
    return request.user


def merge():
    department = Department.objects.all()
    school = School.objects.all()
    school_list = []
    department_list = []

    for s in school:
        school_list.append((s.name, s.id))

    for d in department:
        department_list.append((d.name, d.school.id))

    school_department = {}
    id_school = {}
    department_school = {}
    school = []
    department = []
    for schoolitem in school_list:
        school.append(schoolitem[0])
        id_school[str(schoolitem[1])] = schoolitem[0]
        school_department[schoolitem[0]] = []
    for departmentitem in department_list:

        department.append(departmentitem[0])
        school_department[id_school[str(departmentitem[1])]].append(departmentitem[0])
        department_school[departmentitem[0]] = [id_school[str(departmentitem[1])]]

    school_department["select school"] = department

    return school, department, school_department, department_school


def check_login(request):
    if request.session.get("is_login", None) and not request.user.is_anonymous:
        return True
    else:
        return False


def check_user_authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


def User_service_send_email_authenticated(
    request,
    service_type,
    cuisine_names,
    interests_names,
    selected_days_names,
    school,
    department,
):
    email_subject = "Service Confirmation"
    message = render_to_string(
        "service_confirmation.html",
        {
            "user": get_user(request).first_name,
            "service_type": service_type,
            "cuisines_selected": cuisine_names,
            "selected_interests": interests_names,
            "selected_days_names": selected_days_names,
            "school": school,
            "department": department,
        },
    )
    to_email = get_user(request).email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


def getModelData(user):
    all_selected_cuisine = UserRequest.objects.values_list("cuisines", flat=True)
    all_selected_interests = UserRequest.objects.values_list("interests", flat=True)

    # get top 7 most common cuisine
    most_frequent_cuisine = [x for x, _ in Counter(all_selected_cuisine).most_common(7)]

    # get top 5 most common interests
    most_frequent_interest = [
        x for x, _ in Counter(all_selected_interests).most_common(5)
    ]

    school_set = School.objects.all()
    department_set = Department.objects.all()
    school_list = []
    department_list = []
    try:

        user_request_instance = UserRequest.objects.get(user=user)
        # print(user_request_instance)
        selected_school = user_request_instance.school
        selected_department = user_request_instance.department

        # When user selected preference school show all departments in that school
        new_department_set = Department.objects.filter(school=selected_school)

        for s in school_set:
            if not s == selected_school:
                school_list.append(s)
        for d in new_department_set:
            if not d == selected_department:
                department_list.append(d)

        school_list.append(selected_school)
        department_list.append(selected_department)
    # else:
    #     for s in school_set:
    #         school_list.append(s)
    #     for d in department_set:
    #         department_list.append(d)
    except Exception:
        for s in school_set:
            school_list.append(s)
        for d in department_set:
            department_list.append(d)
    return {
        "cuisines": Cuisine.objects.all(),
        "schools": school_list,
        "departments": department_list,
        "interests": Interests.objects.all(),
        "week_days": [
            Days.objects.get(id=0),
            Days.objects.get(id=1),
            Days.objects.get(id=2),
            Days.objects.get(id=3),
            Days.objects.get(id=4),
            Days.objects.get(id=5),
            Days.objects.get(id=6),
        ],
        "username": user.username,
        "top_cuisines": most_frequent_cuisine,
        "top_interests": most_frequent_interest,
    }


def Merge(dict1, dict2, dict3):
    res = {**dict1, **dict2, **dict3}
    return res


def get_selected_data(user):
    try:
        user_request_instance = UserRequest.objects.get(user=user)
        preffered_cuisines_instances = user_request_instance.cuisines.all()
        preffered_interests_instances = user_request_instance.interests.all()
        preffered_days_instances = user_request_instance.days.all()
        selected_type = user_request_instance.service_type
        selected_school = user_request_instance.school
        selected_department = user_request_instance.department
        selected_cuisine = preffered_cuisines_instances
        selected_interest = preffered_interests_instances
        selected_days = preffered_days_instances

        selected_department_priority = user_request_instance.department_priority
        selected_cuisine_priority = user_request_instance.cuisines_priority
        selected_interest_priority = user_request_instance.interests_priority
        # if not UserRequest.objects.filter(user = user).count() == 0:
        #     print(UserRequest.objects.get(user = user).service_status)
        #     service_status = UserRequest.objects.get(user = user).service_status
        # else:
        #     service_status = False

        selected_info = {
            "selected_type": selected_type,
            "selected_school": selected_school,
            "selected_department": selected_department,
            "selected_cuisine": selected_cuisine,
            "selected_interest": selected_interest,
            "selected_days": selected_days,
            "selected_department_priority": selected_department_priority,
            "selected_cuisine_priority": selected_cuisine_priority,
            "selected_interest_priority": selected_interest_priority,
            # "servcie_status":
        }
    except Exception:
        selected_info = {
            "selected_type": "Daily",
            "selected_department_priority": 5,
            "selected_cuisine_priority": 5,
            "selected_interest_priority": 5,
        }

    return selected_info


def index(request):
    if check_login(request):  # no repeat log in
        preference_model_data = getModelData(request.user)
        selected_info = get_selected_data(request.user)
        if not UserRequest.objects.filter(user_id=request.user.id).count() == 0:

            ur = UserRequest.objects.get(user_id=request.user.id).service_status
            if ur is True:
                service_status = 1
            else:
                service_status = 0
        else:
            service_status = 0
        # context = Merge({"service_status": service_status}, preference_model_data, selected_info)
        return render(
            request,
            "homepage.html",
            Merge(
                {"service_status": service_status}, preference_model_data, selected_info
            ),
        )
    return redirect("/login/")


def handle_ajax(request):
    schoolist, departmentlist, school_departments, depatment_school = merge()
    if request.method == "GET" and "/ajax/load_departments_homepage" in request.path:

        school_id = request.GET.get("school_id", None)
        response = school_departments[school_id]
        return JsonResponse(response, safe=False)
    elif request.method == "GET" and "/ajax/load_school_homepage" in request.path:
        department_id = request.GET.get("department_id", None)
        school = depatment_school[department_id][0]
        response = []
        response.append(school)
        for s in schoolist:
            if not s == school or s == "select school":
                response.append(s)
        return JsonResponse(response, safe=False)


def user_service(request):
    if request.method == "POST":
        if check_user_authenticated(request):
            service_type = request.POST["service_type"]
            school = request.POST["school"]
            school_object = School.objects.get(name=school)
            department = request.POST["department"]
            department_object = school_object.department_set.get(name=department)
            cuisines_priority = request.POST.get("cuisines_priority")
            department_priority = request.POST.get("department_priority")
            interests_priority = request.POST.get("interests_priority")
            cuisine_ids = request.POST.getlist("cuisine[]")
            cuisine_objects = Cuisine.objects.filter(id__in=cuisine_ids)
            cuisine_names = ", ".join([cuisine.name for cuisine in cuisine_objects])

            interests_ids = request.POST.getlist("interests[]")
            interests_objects = Interests.objects.filter(id__in=interests_ids)
            interests_names = ", ".join(
                [interest.name for interest in interests_objects]
            )

            selected_days_ids = request.POST.getlist("days[]")
            selected_days_objects = Days.objects.filter(id__in=selected_days_ids)
            selected_days_names = ", ".join([day.day for day in selected_days_objects])

            logged_user = request.user

            # if request already exist then update the request otherwise update it
            try:
                req = UserRequest.objects.get(pk=logged_user)
                req.service_type = service_type
                req.school = school_object
                req.department = department_object
                req.cuisines_priority = cuisines_priority
                req.department_priority = department_priority
                req.interests_priority = interests_priority
                req.cuisines.clear()
                req.interests.clear()
                req.days.clear()
                req.available_date = date.today() + timedelta(days=1)
                req.time_stamp = datetime.now()
                req.service_status = True
                req.save()
                req.cuisines.add(*cuisine_objects)
                req.interests.add(*interests_objects)
                req.days.add(*selected_days_objects)

            except ObjectDoesNotExist:
                req = UserRequest(
                    user=logged_user,
                    service_type=service_type,
                    school=school_object,
                    department=department_object,
                    cuisines_priority=cuisines_priority,
                    department_priority=department_priority,
                    interests_priority=interests_priority,
                    available_date=date.today() + timedelta(days=1),
                )
                req.service_status = True
                req.save()
                req.cuisines.add(*cuisine_objects)
                req.interests.add(*interests_objects)
                req.days.add(*selected_days_objects)

            User_service_send_email_authenticated(
                request,
                service_type,
                cuisine_names,
                interests_names,
                selected_days_names,
                school,
                department,
            )
        return redirect("/")

    else:
        return redirect("/login/")


def toggle_user_service(request):
    if request.method == "POST":
        if check_user_authenticated(request):
            logged_user = request.user
            req = UserRequest.objects.get(pk=logged_user)
            req.service_status = (
                True if request.POST["service_status"] == "true" else False
            )
            req.available_date = date.today() + timedelta(days=1)
            req.save()
            return JsonResponse({"service_status": req.service_status}, safe=False)
        else:
            return redirect("/login/")


def match_history(request):
    if check_login(request):
        # request.user
        user_matches = UserRequestMatch.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        ).order_by("-match_time")

        next_lunch_matches = []
        past_lunch_macthes = []

        for match in user_matches:
            matched_user = match.user2 if match.user1 == request.user else match.user1
            matched_user_cuisines_instance = UserRequest.objects.get(
                user=matched_user
            ).cuisines.all()
            matched_user_interests_instances = UserRequest.objects.get(
                user=matched_user
            ).interests.all()
            matched_user_cuisines = ", ".join(
                [cuisine.name for cuisine in matched_user_cuisines_instance]
            )
            matched_user_interests = ", ".join(
                [interest.name for interest in matched_user_interests_instances]
            )
            # matched_restaurants = ", ".join(
            #     [restaurant.name.capitalize() for restaurant in match.restaurants.all()]
            # )
            match_dict = {
                "match_time": match.match_time,
                "matched_user_name": matched_user.first_name
                + " "
                + matched_user.last_name,
                "matched_email": matched_user.email,
                "matched_user_school": matched_user.school,
                "matched_user_department": matched_user.department,
                "matched_user_cuisines": matched_user_cuisines,
                "matched_user_interests": matched_user_interests,
            }
            if datetime.now(timezone.utc) <= match.match_time:
                next_lunch_matches.append(match_dict)
            else:
                past_lunch_macthes.append(match_dict)

        preference_model_data = getModelData(request.user)
        selected_info = get_selected_data(request.user)
        return render(
            request,
            "match_history.html",
            Merge(
                {
                    "next_lunch_matches": next_lunch_matches,
                    "past_lunch_macthes": past_lunch_macthes,
                },
                preference_model_data,
                selected_info,
            ),
        )

    return redirect("/login/")


def settings(request):

    if check_login(request):

        user_info = LunchNinjaUser.objects.get(id=request.user.id)
        user_profile = {
            "username": user_info.username,
            "name": user_info.first_name + " " + user_info.last_name,
            "email": user_info.email,
            "phone": user_info.Phone,
            "school": user_info.school,
            "department": user_info.department,
        }

        try:
            user_request_instance = UserRequest.objects.get(user=request.user)
            preffered_cuisines_instances = user_request_instance.cuisines.all()
            preffered_interests_instances = user_request_instance.interests.all()
            preffered_days_instances = user_request_instance.days.all()

            user_request = {
                "service_type": user_request_instance.service_type,
                "service_start_date": user_request_instance.time_stamp,
                "preffered_school": user_request_instance.school,
                "preffered_department": user_request_instance.department,
                "service_status": user_request_instance.service_status,
                "preferred_cuisines": ", ".join(
                    [cuisine.name for cuisine in preffered_cuisines_instances]
                ),
                "preferred_interests": ", ".join(
                    [interest.name for interest in preffered_interests_instances]
                ),
                "department_priority": user_request_instance.department_priority,
                "cuisines_priority": user_request_instance.cuisines_priority,
                "interests_priority": user_request_instance.interests_priority,
                "preferred_weekday": ", ".join(
                    [day.day for day in preffered_days_instances]
                ),
                "next_meet_day": str(user_request_instance.available_date),
            }
        except UserRequest.DoesNotExist:
            user_request = None

        preference_model_data = getModelData(request.user)
        selected_info = get_selected_data(request.user)

        return render(
            request,
            "settings.html",
            Merge(
                {"user_request": user_request, "user_profile": user_profile},
                preference_model_data,
                selected_info,
            ),
        )
    return redirect("/login/")


def feedback(request):
    if len(request.META.get("PATH_INFO").split("/")) != 3:
        context = {"message": "We could not find a match history for you"}
        return render(request, "error.html", context=context)
    raw1 = request.META.get("PATH_INFO").split("/")[-1]
    if len(raw1.split("'")) < 2:
        context = {"message": "We could not find a match history for you"}
        return render(request, "error.html", context=context)
    raw2 = raw1.split("'")[1]
    try:
        pair = str(base64.b64decode(bytes(raw2.encode())))[1:]
    except ValueError:
        context = {"message": "We could not find a match history for you"}
        return render(request, "error.html", context=context)
    matchpair = pair.split("'")[1]
    data = matchpair.split("-")
    print(matchpair)
    if request.method == "POST":
        # data = request.META.get("PATH_INFO")[1:].split("/")[-1].split("-")
        match_id = int(data[0])
        user_id = int(data[1])
        match = UserRequestMatch.objects.get(id=match_id)
        user = LunchNinjaUser.objects.get(id=user_id)
        attendecnce = request.POST["attendance"]
        experience = request.POST["experience"]
        restaurant = request.POST["restaurant"]
        partner = request.POST["partner"]
        comment = request.POST["comment"]
        count = int(Feedback.objects.all().count())
        fb = Feedback(id=count + 1, match=match, user=user, comment=comment)
        fb.save()
        q1 = Question.objects.get(label="attendance")
        c1 = q1.choice_set.get(choice_text=attendecnce)
        fb.choices.add(c1)
        q2 = Question.objects.get(label="experience")
        c2 = q2.choice_set.get(choice_text=experience)
        fb.choices.add(c2)
        q3 = Question.objects.get(label="restaurant")
        c3 = q3.choice_set.get(choice_text=restaurant)
        fb.choices.add(c3)
        q4 = Question.objects.get(label="partner")
        c4 = q4.choice_set.get(choice_text=partner)
        fb.choices.add(c4)
        return redirect("/homepage/")
    else:
        # data = request.META.get("PATH_INFO").split("/")[-1].split("-")
        if not len(data) == 2:
            context = {"message": "We could not find a match history for you"}
            return render(request, "error.html", context=context)
        match_id = int(data[0])
        user_id = int(data[1])
        if UserRequestMatch.objects.filter(id=match_id).count() == 0:
            context = {"message": "We could not find a match history for you"}
            return render(request, "error.html", context=context)

        match = UserRequestMatch.objects.get(id=match_id)
        match_user1 = match.user1
        match_user2 = match.user2
        if LunchNinjaUser.objects.filter(id=user_id).count() == 0:
            context = {"message": "We could not find a match history for you"}
            return render(request, "error.html", context=context)
        user = LunchNinjaUser.objects.get(id=user_id)

        count = Feedback.objects.filter(match=match, user=user).count()
        if count == 0 and (user.id == match_user1.id or user_id == match_user2.id):
            context = {"latest_question_list": Question.objects.all()}
            return render(request, "feedback.html", context=context)
        else:
            if not count == 0:
                context = {"message": "You have already submitted the form"}
                return render(request, "error.html", context=context)
            else:
                context = {"message": "We could not find a match history for you"}
                return render(request, "error.html", context=context)


def about(request):
    if check_login(request):  # no repeat log in
        preference_model_data = getModelData(request.user)
        selected_info = get_selected_data(request.user)
        return render(
            request, "about.html", Merge({}, preference_model_data, selected_info)
        )
    return redirect("/login/")


def error_404_view(request, exception):
    context = {"message": "We could not find the page"}
    return render(request, "error.html", context=context)


# def test(request):
#     return render(request, "test.html")

#
# def match(request):
#     run(["python", "match.py"], shell=False, stdout=PIPE)
#     return redirect("/homepage/test")
#
#
# def create_users(request):
#     run(["python", "create_users.py"], shell=False, stdout=PIPE)
#     return redirect("/homepage/test")
#
#
# def create_ur(request):
#     run(["python", "create_userrequests.py"], shell=False, stdout=PIPE)
#     return redirect("/homepage/test")
