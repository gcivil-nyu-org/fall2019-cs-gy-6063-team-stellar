from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate,logout
from .forms import UserSignUpForm,UserSignInForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token_generator import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage

def index(request):
    # if not request.session.get('is_login', None):
    #     return redirect('/login/')
    return render(request, 'index.html')

def usersignup(request):

    if request.method == 'POST':
        signup_form = UserSignUpForm(request.POST)
        print(signup_form)
        if signup_form.is_valid():
            print("AAAAAAAAAAAA")
            user = signup_form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            email_subject = 'Activate Your Account'
            message = render_to_string('activate_account.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':  urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = signup_form.cleaned_data.get('email')
            email = EmailMessage(email_subject, message, to=[to_email])
            email.send()
            return HttpResponse('We have sent you an email, please confirm your email address to complete registration')
    else:
        signup_form = UserSignUpForm()
    return render(request, 'signup.html',locals())
def userlogin(request):
    if request.session.get('is_login', None):  # no repeat log in
        return redirect('/index/')
    login_form = UserSignInForm(request.POST)

    if login_form.is_valid():
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print("AAAAAAAA")
        if user is not None:
            login(request, user)
            print(user)
            request.session['is_login'] = True
            request.session['user_id'] = user.id
            request.session['user_name'] = user.first_name
            return redirect('/index/')
            # Redirect to a success page.
        else:
            # Return an 'invalid login' error message.

            message = 'Incorrect username or password!'
            return render(request, 'login.html', locals())
    return render(request, 'login.html', locals())

def userlogout(request):
    if not request.session.get('is_login', None):
        # user must log in
        return redirect("/login/")
    request.session.flush()
    logout(request)
    return redirect("/login/")


def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('Your account has been activate successfully')
    else:
        return HttpResponse('Activation link is invalid!')




