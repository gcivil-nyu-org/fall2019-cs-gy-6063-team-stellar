from django.urls import path, re_path
from . import views

urlpatterns = [
    path("homepage/", views.index),
    path("service/", views.service),
    path("matchHistory/", views.match_history),
    path("settings/", views.settings),
    path("about/", views.about),
    path("toggle-service/", views.toggle_user_service),
    re_path(r"feedback/", views.feedback),
    re_path(r"^[a-zA-Z]*/ajax/load_departments_homepage/$", views.handle_ajax),
    re_path(r"^[a-zA-Z]*/ajax/load_school_homepage/$", views.handle_ajax),
]

handler404 = "homepage.views.error_404_view"
