from django.conf.urls import url
from django.urls import path
from . import views


urlpatterns = [
    url(r"^$", views.usersignup, name="register_user"),
    url(
        r"^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        views.activate_account,
        name="activate",
    ),
    path("signup/", views.usersignup),
    path("index/", views.index),
    path("login/", views.userlogin),
    path("logout/", views.userlogout),
]
