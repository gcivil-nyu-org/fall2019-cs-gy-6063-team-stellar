from django.conf.urls import url
from django.urls import path, re_path
from . import views


urlpatterns = [
    url(r"^$", views.usersignup, name="register_user"),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate_account,
        name="activate",
    ),
    path("signup/", views.usersignup),
    path("login/", views.userlogin),
    path("logout/", views.userlogout),
    re_path(r"^ajax/load_departments/$", views.usersignup),
    re_path(r"^ajax/load_school/$", views.usersignup),
]
