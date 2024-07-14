from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from django.core.validators import validate_email
from utilisateur.models import Utilisateur
from django.contrib.auth import authenticate, login, logout
from utilisateur.forms import UtilisateurChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def validerconnexion(request: HttpRequest):
    if request.method == "POST":
        data = request.POST
        pseudo = data.get('pseudo')
        mdp = data.get('mdp')
        
        if not pseudo or len(str(pseudo).strip()) <= 0:
            return redirect("/connexion/")
        pseudo = str(pseudo).lower()
        
        if not mdp or len(str(mdp).strip()) < 6:
            return redirect("/connexion/")
        mdp = str(mdp).strip()
        
        try:
            validate_email(pseudo)
        except:
            return redirect("/connexion/")
        
        user = authenticate(request, username=pseudo, password=mdp)
        
        if user is None:
            return redirect("/connexion/")
        else:
            login(request, user)
            return redirect("/")
            
        
    else:
        return redirect("/")

def validerinscription(request:HttpRequest):
    if request.method == "POST":
        data = request.POST
        nom =data.get("nom")
        prenom = data.get("prenom")
        adresse = data.get("adresse")
        pseudo = data.get('pseudo')
        mdp = data.get('mdp')
        
        if not nom or len(str(nom).strip()) <= 0:
            return redirect("/inscription/")
        nom = str(nom).strip()
        
        if not prenom or len(str(prenom).strip()) <= 0:
            return redirect("/inscription/")
        prenom = str(prenom).strip()
        
        if not adresse or len(str(adresse).strip()) <= 0:
            return redirect("/inscription/")
        adresse = str(adresse).strip()
        
        if not pseudo or len(str(pseudo).strip()) <= 0:
            return redirect("/inscription/")
        pseudo = str(pseudo).lower()
        
        if not mdp or len(str(mdp).strip()) < 6:
            return redirect("/inscription/")
        mdp = str(mdp).strip()
        
        try:
            validate_email(pseudo)
        except:
            return redirect("/inscription/")
        
        try:
            user = Utilisateur.objects.get(pseudo=pseudo)
            return redirect("/inscription/")
        except:
            new_user = Utilisateur()
            new_user.pseudo = pseudo
            new_user.nom = nom
            new_user.prenom = prenom
            new_user.adresse = adresse
            new_user.set_password(mdp) 
            new_user.save()
            return redirect("/connexion/")
        
            
        
    else:
        return redirect("/")
def deconnexion(request:HttpRequest):
    logout(request)
    return redirect("/connexion/")

