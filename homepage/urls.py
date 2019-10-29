from django.urls import path
from . import views

# urlpatterns = [path("homepage/", views.index),
# path('serviceSelect/', views.user_service)]

urlpatterns = [path("homepage/", views.index),
               # path('homepage/service', views.ServicetypeView.as_view(), name='service'),
               path('serviceSelect/', views.servicetype),
               # path('school/', views.SchoolView.as_view(), name='school'),
               # path('cuisine/', views.CuisinetypeView.as_view(), name='cuisine'),
               ]