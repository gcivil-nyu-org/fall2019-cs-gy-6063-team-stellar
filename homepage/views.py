from django.shortcuts import render, redirect
from .models import UserRequest, Department, School, Cuisine
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string

# Create your views here.
def index(request):
    department =Department.objects.all()
    school = School.objects.all()
    cuisine = Cuisine.objects.all()
    return render(request, "homepage.html",{"cuisines": cuisine, "schools":school, "departments":department})

def user_service(request):
    if request.method == "POST":
        service_type = request.POST["service_type"]
        cuisine = request.POST.getlist("cuisine[]")
        school = request.POST["school"]
        
        req = UserRequest(service_type=service_type, cuisine=cuisine, school=school)
        req.save()

        # current_site = get_current_site(request)
        # email_subject = "Activate Your Account"
        # message = render_to_string(
        #     "activate_account.html",
        #     {
        #         "user": user,
        #         "domain": current_site.domain,
        #         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        #         "token": account_activation_token.make_token(user),
        #     },
        # )
        # to_email = signup_form.cleaned_data.get("email")
        # email = EmailMessage(email_subject, message, to=[to_email])
        # email.send()
        return redirect("/")
    else:
        return False
