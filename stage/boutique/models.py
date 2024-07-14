from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator


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
