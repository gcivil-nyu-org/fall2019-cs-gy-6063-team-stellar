from django.urls import path
from . import views

urlpatterns = [
    path("homepage/", views.index),
    path("serviceRequest/", views.user_service),
]
