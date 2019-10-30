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
    return redirect("/login")


def user_service(request):
    if request.method == "POST":
        service_type = request.POST["service_type"]
        cuisine = request.POST.getlist("cuisine[]")
        school = request.POST["school"]
        id = request.user.id
        print("id is" + str(id))
        req = UserRequest(
            user_id=id, service_type=service_type, cuisine=cuisine, school=school
        )
        req.save()

        email_subject = "Activate Your Account"
        message = render_to_string(
            "service_confirmation.html",
            {"user": request.user, "type": service_type, "cuisine": cuisine},
        )
        to_email = request.user.email
        email = EmailMessage(email_subject, message, to=[to_email])
        email.send()
        return redirect("/")
    else:
        return False
