from django.urls import path, re_path
from . import views

urlpatterns = [
    path("homepage/", views.index),
    path("serviceRequest/", views.user_service),
    path("matchHistory/", views.match_history),
    # path("homepage/test/", views.test),
    path("settings/", views.settings),
    path("about/", views.about),
    path("toggle-service/", views.toggle_user_service),
    # path("homepage/test/match", views.match),
    # path("homepage/test/create_users", views.create_users),
    # path("homepage/test/create_ur", views.create_ur),
    # path("feedback/", views.feedback),
    re_path(r"feedback/", views.feedback),
    re_path(r"^[a-zA-Z]*/ajax/load_departments_homepage/$", views.handle_ajax),
    re_path(r"^[a-zA-Z]*/ajax/load_school_homepage/$", views.handle_ajax),
]
