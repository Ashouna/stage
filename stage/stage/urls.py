
from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index),
    path("apropos/", apropos, name="apropos"),
    path("contact/", contact, name="contact"),
    path("inscription/", inscription, name="inscription"),
    path("connexion/", connexion, name="connexion"),
    path("profil/", profil, name="profil"),
    path("categories/", categories, name="categories"),
    path("produits/", produits, name="produits"),
    path("produits/<int:id>/", produit, name="produit-detail"),
    path("auth/", include("auth_gateway.urls")),
    
]
