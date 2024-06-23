from django.urls import path, include
from . import views

urlpatterns = [
path('', views.skincare_scan, name='skin_care_scan'),
path('logout', views.logoutview, name='logoutview'),
path('detection', views.disease_scan, name='disease_scan'),
]