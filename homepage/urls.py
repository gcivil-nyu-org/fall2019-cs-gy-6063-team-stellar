from django.urls import path
from . import views

urlpatterns = [path("homepage/", views.index),
               path('service/', views.ServicetypeView.as_view(), name='service'),
               path('school/', views.SchoolView.as_view(), name='school'),
               path('cuisine/', views.CuisinetypeView.as_view(), name='cuisine'),
               ]
