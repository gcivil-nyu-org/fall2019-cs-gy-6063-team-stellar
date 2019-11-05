from django.urls import path, re_path
from . import views

urlpatterns = [
    path("homepage/", views.index),
    path("serviceRequest/", views.user_service),
    path("homepage/match.html/", views.match),
    re_path(r"^homepage/ajax/load_departments_homepage/$", views.user_service),
    re_path(r"^homepage/ajax/load_school_homepage/$", views.user_service),
]