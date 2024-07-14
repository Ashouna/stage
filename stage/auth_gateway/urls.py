
from django.contrib import admin
from django.urls import path
from .views import *

app_name = "AuthGateway"
urlpatterns = [
    path("validerconnexion/", validerconnexion, name="validerconnexion"),
    path("validerinscription/", validerinscription, name="validerinscription"),
    path("logout/", deconnexion, name="logout"),

]
