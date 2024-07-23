from django.contrib import admin
from .models import Categorie, Produit, Panier, ProduitPanier,Commande

# Register your models here.

admin.site.register([Categorie, Produit, Panier, ProduitPanier, Commande])
