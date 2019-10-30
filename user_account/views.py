from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserSignUpForm, UserSignInForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.core.mail import EmailMessage
from django.http import JsonResponse
from homepage.models import  Department, School


from .models import LunchNinjaUser


def index(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')
    return render(request, "index.html")


# def retrieveschool():
#     conn = psycopg2.connect(database="lunchninja", host="localhost", user='postgres', password='password')
#     # conn = psycopg2.connect(database="lunchninja", host="localhost")
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur = conn.cursor()
#     cur.execute("SELECT name,id FROM school")
#     count = cur.fetchall()
#     # print(count)
#     conn.commit()
#     conn.close()
#     return count
#
#
# def retrievedepartment():
#     conn = psycopg2.connect(database="lunchninja", host="localhost", user='postgres', password='password')
#     # conn = psycopg2.connect(database="lunchninja", host="localhost")
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
#     cur = conn.cursor()
#     # cur.execute("SELECT id FROM school WHERE name LIKE \'" + schoolname +"\'")
#     # id = cur.fetchone()
#     sqlline = "SELECT name,school FROM department"
#     cur.execute(sqlline)
#     count = cur.fetchall()
#     # print(count)
#     conn.commit()
#     conn.close()
#     return count


def merge():
    department = Department.objects.all()
    school = School.objects.all()
    school_list=[]
    department_list=[]
    for s in school:
        school_list.append((s.name,s.id))

    for d in department:
        department_list.append((d.name,d.school))
    # schoollists = retrieveschool()
    # departmentlists = retrievedepartment()

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

        department = departmentitem[0]
        school_department[id_school[str(departmentitem[1])]].append(departmentitem[0])
        department_school[departmentitem[0]] = [id_school[str(departmentitem[1])]]

    school_department["select school"] = department

    # print(school_department)
    # print(department_school)
    return school, department, school_department, department_school


def usersignup(request):
    schoolist, departmentlist, school_departments, depatment_school = merge()
    if request.method == "POST":
        signup_form = UserSignUpForm(request.POST)
        error = signup_form.errors.get_json_data()
        if signup_form.is_valid():
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            school = signup_form.cleaned_data.get("school")
            department = signup_form.cleaned_data.get("department")
            Phone = signup_form.cleaned_data.get("Phone")
            user.school = school
            user.department = department
            user.Phone = Phone
            current_site = get_current_site(request)
            email_subject = "Activate Your Account"
            message = render_to_string(
                "activate_account.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = signup_form.cleaned_data.get("email")
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse(
                "We have sent you an email, "
                "please confirm your email address to complete registration"
            )
        errordict = {}
        for key in error:
            error_message = error[key]
            messagetext = error_message[0]["message"]
            errordict[key] = messagetext
        errordict["signup_form"] = signup_form
        return render(request, "signup.html", errordict)
    elif request.method == "GET" and request.path.startswith("/ajax/load_departments"):

        school_id = request.GET.get("school_id", None)
        response = school_departments[school_id]
        return JsonResponse(response, safe=False)
    elif request.method == "GET" and request.path.startswith("/ajax/load_school"):
        department_id = request.GET.get("department_id", None)
        school = depatment_school[department_id][0]
        response = []
        response.append(school)
        for s in schoolist:
            if not s == school or s == "select school":
                response.append(s)

        return JsonResponse(response, safe=False)
    else:
        signup_form = UserSignUpForm()
        return render(request, "signup.html", {"signup_form": signup_form})


def userlogin(request):
    # if request.session.get("is_login", None):  # no repeat log in
    #     return redirect("/homepage/")
    login_form = UserSignInForm(request.POST)

    if login_form.is_valid():
        username = login_form.cleaned_data.get("username")
        password = login_form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(user)
            request.session["is_login"] = True
            request.session["user_id"] = user.id
            request.session["user_name"] = user.first_name
            return redirect("/homepage/")
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.

            message = "Incorrect username or password!"
            return render(
                request, "login.html", {"login_form": login_form, "message": message}
            )
    return render(request, "login.html", locals())


def userlogout(request):
    request.session.flush()
    return redirect("/login/")


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = LunchNinjaUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, LunchNinjaUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse("Your account has been activate successfully")
    else:
        return HttpResponse("Activation link is invalid!")
