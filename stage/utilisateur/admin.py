from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import UtilisateurCreationForm, UtilisateurChangeForm
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    add_form = UtilisateurCreationForm
    form = UtilisateurChangeForm
    model = Utilisateur
    list_display = ("pseudo", "nom", "is_staff", "is_active", "is_superuser")
    list_filter = ("pseudo", "is_staff", "is_active", "is_superuser")
    fieldsets = (
        (None, {"fields" : ("nom", "prenom",  "adresse", "pseudo", "password")}),
        ("Permission", {"fields" : ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes" : ("wide",),
            "fields" : (
                "nom", "prenom", "adresse", "pseudo", "password1", "password2",
                "is_staff", "is_active", "is_superuser", "groups", "user_permissions"
            )
        }),
    )
    search_fields = ("pseudo",)
    ordering = ("pseudo",)
    
admin.site.register(Utilisateur, UtilisateurAdmin)
    


