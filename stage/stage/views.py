from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from utilisateur.forms import UtilisateurProfilModificationForm
from boutique.models import Categorie, Produit

def index(request):
    return render(request, "index.html")

def apropos(request):
    return render(request, "apropos.html")

def contact(request):
    return render(request, "contact.html")

def inscription(request):
    return render(request, "inscription.html")


def connexion(request):
    return render(request, "connexion.html")

def profil(request:HttpRequest):
    
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            form = UtilisateurProfilModificationForm(instance=user)
            return render(request, "profil.html", {"form": form})
        else:
            return redirect("connexion")
    elif request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            form = UtilisateurProfilModificationForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
                return redirect('profil')
            return render(request, "profil.html", {"form": form})
        else:
            return redirect("connexion")
        i    

def categories(request:HttpRequest):
    mescategories = Categorie.objects.all()
    return render(request, "categories.html", {"categories": mescategories})

def produits(request:HttpRequest):
    mesproduits = Produit.objects.all()
    mescategories = Categorie.objects.all()
    return render(request, "produits.html", {"produits": mesproduits, "categories": mescategories})


def produit(request:HttpRequest, id):
    try:
        monproduit = Produit.objects.get(pk=id)
        return render(request, "produit-detail.html", {'produit': monproduit})
    except Produit.DoesNotExist:
        return redirect("produits")