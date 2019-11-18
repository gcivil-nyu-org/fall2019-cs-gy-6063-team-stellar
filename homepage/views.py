from django.shortcuts import render, redirect
from subprocess import run, PIPE
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import (
    UserRequest,
    School,
    Cuisine,
    UserRequestMatch,
    Days_left,
    Interests,
    Department,
)
from datetime import datetime, timezone, timedelta, date


# Create your views here.
Service_days = {"Daily": 1, "Weekly": 7, "Monthly": 30}


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


def check_ajax_department(request):
    if request.method == "GET" and "/ajax/load_departments_homepage" in request.path:
        return True
    return False


def check_ajax_school(request):
    if request.method == "GET" and "/ajax/load_school_homepage" in request.path:
        return True
    return False


def check_login(request):
    if request.session.get("is_login", None):
        return True
    else:
        return False


def check_user_authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


def User_service_send_email_authenticated(
    request, service_type, cuisine_names, interests_names, school, department
):
    email_subject = "Service Confirmation"
    message = render_to_string(
        "service_confirmation.html",
        {
            "user": request.user.first_name,
            "service_type": service_type,
            "cuisines_selected": cuisine_names,
            "selected_interests": interests_names,
            "school": school,
            "department": department,
        },
    )
    to_email = request.user.email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


def index(request):
    if check_login(request):  # no repeat log in
        department = Department.objects.all()
        school = School.objects.all()
        cuisine = Cuisine.objects.all()
        interests = Interests.objects.all()
        return render(
            request,
            "homepage.html",
            {
                "cuisines": cuisine,
                "schools": school,
                "departments": department,
                "interests": interests,
            },
        )
    return redirect("/login/")


def user_service(request):
    schoolist, departmentlist, school_departments, depatment_school = merge()
    if request.method == "POST":
        if check_user_authenticated(request):
            service_type = request.POST["service_type"]
            school = request.POST["school"]
            school_object = School.objects.filter(name=school)
            department = request.POST["department"]
            department_object = Department.objects.filter(name=department)
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

                # match_his = UserRequestMatch.objects.filter(Q(user1=req.user) | Q(user2=req.user)).order_by(
                #     "-match_time")
                # print(match_his[0])

                req.available_date = date.today() + timedelta(days=1)
                req.time_stamp = datetime.now()
                req.save()
                req.cuisines.add(*cuisine_objects)
                req.interests.add(*interests_objects)
                day = Days_left.objects.get(user_id=logged_user.id)
                day.days = Service_days[req.service_type]
                day.save()
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
                req.save()
                req.cuisines.add(*cuisine_objects)
                req.interests.add(*interests_objects)
                days = Days_left(user=logged_user, days=Service_days[req.service_type])
                days.save()

            # daysleft = Days_left(user=logged_user, days=Service_days[service_type])
            # daysleft.save()
            User_service_send_email_authenticated(
                request,
                service_type,
                cuisine_names,
                interests_names,
                school,
                department,
            )
        else:
            email_subject = "Service Confirmation"
            message = "Service selected"
            to_email = request.user.email
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
        return redirect("/")
    elif check_ajax_department(request):

        school_id = request.GET.get("school_id", None)
        response = school_departments[school_id]
        return JsonResponse(response, safe=False)
    elif check_ajax_school(request):
        department_id = request.GET.get("department_id", None)
        school = depatment_school[department_id][0]
        response = []
        response.append(school)
        for s in schoolist:
            if not s == school or s == "select school":
                response.append(s)
        return JsonResponse(response, safe=False)

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

        department = Department.objects.all()
        school = School.objects.all()
        cuisine = Cuisine.objects.all()
        interests = Interests.objects.all()

        return render(
            request,
            "match_history.html",
            {
                "next_lunch_matches": next_lunch_matches,
                "past_lunch_macthes": past_lunch_macthes,
                "cuisines": cuisine,
                "schools": school,
                "departments": department,
                "interests": interests,
            },
        )

    return redirect("/login/")


def settings(request):
    if check_login(request):
        department = Department.objects.all()
        school = School.objects.all()
        cuisine = Cuisine.objects.all()
        interests = Interests.objects.all()

        try:
            user_request_instance = UserRequest.objects.get(user=request.user)
            preffered_cuisines_instances = user_request_instance.cuisines.all()
            preffered_interests_instances = user_request_instance.interests.all()
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
            }
        except UserRequest.DoesNotExist:
            user_request = None

        return render(
            request,
            "settings.html",
            {
                "cuisines": cuisine,
                "schools": school,
                "departments": department,
                "user_request": user_request,
                "interests": interests,
            },
        )
    return redirect("/login/")


def test(request):
    return render(request, "test.html")


def match(request):
    run(["python", "match.py"], shell=False, stdout=PIPE)
    return redirect("/homepage/test")


def create_users(request):
    run(["python", "create_users.py"], shell=False, stdout=PIPE)
    return redirect("/homepage/test")


def create_ur(request):
    run(["python", "create_userrequests.py"], shell=False, stdout=PIPE)
    return redirect("/homepage/test")
