from django.shortcuts import render, redirect
from .models import UserRequest, Department, School, Cuisine
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

# Create your views here.


def index(request):
    if request.session.get("is_login", None):  # no repeat log in
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
    if request.method == "POST":
        service_type = request.POST["service_type"]
        cuisine = request.POST.getlist("cuisine[]")
        school = request.POST["school"]
        if request.user.id:
            id = request.user.id
        else:
            id = -1
        req = UserRequest(
                user_id=id, service_type=service_type, cuisine=cuisine, school=school
            )
        req.save()


        email_subject = "Service Confirmation"
        message = render_to_string(
            "service_confirmation.html",
            {"user": request.user, "type": service_type, "cuisine": cuisine},
        )
        if request.user.email:
            to_email = request.user.email
        else:
            to_email = "up@nyu.edu"
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect("/")
    else:
        return False
