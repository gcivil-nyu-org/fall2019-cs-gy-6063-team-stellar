from django.urls import path, re_path
from . import views

urlpatterns = [
    path("homepage/", views.index),
    path("serviceRequest/", views.user_service),
    path("matchHistory/", views.match_history),
    path("homepage/test/", views.test),
    path("settings/", views.settings),
    path("homepage/test/match", views.match),
    path("homepage/test/create_users", views.create_users),
    path("homepage/test/create_ur", views.create_ur),
    re_path(r"^homepage/ajax/load_departments_homepage/$", views.user_service),
    re_path(r"^homepage/ajax/load_school_homepage/$", views.user_service),
]
