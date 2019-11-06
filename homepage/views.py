from django.shortcuts import render, redirect

# Days_left,


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from .models import UserRequest, School, Cuisine, UserRequestMatch
from .models import Department

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
        department_list.append((d.name, d.school))

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


def check_index_login(request):
    if request.session.get("is_login", None):
        return True
    else:
        return False


def check_user_authenticated(request):
    if request.user.is_authenticated:
        return True
    else:
        return False


def User_service_send_email_authenticated(request, service_type, cuisine_names):
    email_subject = "Service Confirmation"
    message = render_to_string(
        "service_confirmation.html",
        {
            "user": request.user.first_name,
            "service_type": service_type,
            "cuisines_selected": cuisine_names,
        },
    )
    to_email = request.user.email
    email = EmailMessage(email_subject, message, to=[to_email])
    email.send()


def index(request):
    if check_index_login(request):  # no repeat log in
        department = Department.objects.all()
        school = School.objects.all()
        cuisine = Cuisine.objects.all()

        return render(
            request,
            "homepage.html",
            {"cuisines": cuisine, "schools": school, "departments": department},
        )
    return redirect("/login/")


def user_service(request):
    schoolist, departmentlist, school_departments, depatment_school = merge()

    if request.method == "POST":
        if check_user_authenticated(request):
            service_type = request.POST["service_type"]
            school = request.POST["school"]
            department = request.POST["department"]
            cuisine_ids = request.POST.getlist("cuisine[]")
            cuisine_objects = Cuisine.objects.filter(id__in=cuisine_ids)
            cuisine_names = ", ".join([cuisine.name for cuisine in cuisine_objects])

            logged_user = request.user

            # if request already exist then update the request otherwise update it
            try:
                req = UserRequest.objects.get(pk=logged_user)
                req.service_type = service_type
                req.school = school
                req.department = department
                req.cuisines.clear()
                req.save()
                req.cuisines.add(*cuisine_objects)
            except ObjectDoesNotExist:
                req = UserRequest(
                    user=logged_user,
                    service_type=service_type,
                    school=school,
                    department=department,
                )
                req.save()
                req.cuisines.add(*cuisine_objects)

            # daysleft = Days_left(user=logged_user, days=Service_days[service_type])
            # daysleft.save()
            User_service_send_email_authenticated(request, service_type, cuisine_names)
        else:
            email_subject = "Service Confirmation"
            message = "Service selected"
            to_email = "up@nyu.edu"
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
        return redirect("/")
    elif request.method == "GET" and request.path.startswith(
        "/homepage/ajax/load_departments_homepage"
    ):

        school_id = request.GET.get("school_id", None)
        response = school_departments[school_id]
        return JsonResponse(response, safe=False)
    elif request.method == "GET" and request.path.startswith(
        "/homepage/ajax/load_school_homepage"
    ):
        department_id = request.GET.get("department_id", None)
        school = depatment_school[department_id][0]
        response = []
        response.append(school)
        for s in schoolist:
            if not s == school or s == "select school":
                response.append(s)
        return JsonResponse(response, safe=False)

    else:
        return False


def match_history(request):
    if request.session.get("is_login", None):
        # request.user
        user_matches = UserRequestMatch.objects.filter(
            Q(user1=request.user) | Q(user2=request.user)
        ).order_by("-match_time")

        all_matches = []

        for match in user_matches:
            matched_user = match.user2 if match.user1 == request.user else match.user1
            matched_user_cuisines_instance = UserRequest.objects.get(
                user=matched_user
            ).cuisines.all()
            matched_user_cuisines = ", ".join(
                [cuisine.name for cuisine in matched_user_cuisines_instance]
            )
            match_dict = {
                "match_time": match.match_time,
                "matched_user_name": matched_user.first_name
                + " "
                + matched_user.last_name,
                "matched_email": matched_user.email,
                "matched_user_school": matched_user.school,
                "matched_user_department": matched_user.department,
                "matched_user_cuisines": matched_user_cuisines,
            }
            all_matches.append(match_dict)

        department = Department.objects.all()
        school = School.objects.all()
        cuisine = Cuisine.objects.all()

        return render(
            request,
            "match_history.html",
            {
                "matches": all_matches,
                "cuisines": cuisine,
                "schools": school,
                "departments": department,
            },
        )

    return redirect("/login/")

def settings(request):
    department = Department.objects.all()
    school = School.objects.all()
    cuisine = Cuisine.objects.all()

    user_request_instance = UserRequest.objects.get(user=request.user)
    preffered_cuisines_instances = user_request_instance.cuisines.all()
    user_request = {
        "service_type":user_request_instance.service_type,
        "service_start_date":user_request_instance.time_stamp,
        "preffered_school":user_request_instance.school,
        "preffered_department":user_request_instance.department,
        "service_status":user_request_instance.service_status,
        "preferred_cuisines":", ".join([cuisine.name for cuisine in preffered_cuisines_instances])
    }
   
    return render(request, "settings.html",{
                "cuisines": cuisine,
                "schools": school,
                "departments": department,
                "user_request":user_request
            })

def test(request):
    return render(request, "test.html")
