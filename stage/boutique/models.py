from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator
from utilisateur.models import Utilisateur


class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    image = models.FileField(upload_to='static/images/boutique/categorie/')
    
    
    def __str__(self) -> str:
        return f"Categorie : {str(self.nom)} "
    
    
class Produit(models.Model):
    nom = models.CharField(max_length=255, validators=[MinLengthValidator(4)])
    image_principal = models.FileField(upload_to='static/images/boutique/produits/')
    prix = models.FloatField(validators=[MinValueValidator(10), MaxValueValidator(1000)])
    description = models.CharField(max_length=255)
    quantite = models.PositiveIntegerField()
    image_un = models.FileField(upload_to='static/images/boutique/produits/')
    image_deux = models.FileField(upload_to='static/images/boutique/produits/')
    categorie = models.ForeignKey(Categorie,on_delete=models.CASCADE)


    def __str__(self) -> str:
        return f"Produit : {str(self.nom)} de la categorie  {str(self.categorie.nom)}. Quantité disponible : {str(self.quantite)}"
    
class Panier(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
        
class ProduitPanier(models.Model):
    produit = models.ForeignKey(Produit, on_delete=models.CASCADE)
    quantiteSouhaite = models.IntegerField(default=0)
    prix = models.FloatField()
    prixTotal =models.FloatField()
    panier = models.ForeignKey(Panier, on_delete=models.CASCADE)
    
    
class Commande(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date_effectue = models.DateTimeField(auto_now_add=True)
    articles = models.TextField()
    adresse = models.CharField(max_length=255)
         
