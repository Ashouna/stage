from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UtilisateursManager

# Create your models here.
class Utilisateur(AbstractBaseUser, PermissionsMixin):
    nom = models.CharField(max_length=255)
    prenom = models.CharField(max_length=255)
    pseudo = models.EmailField(unique=True)
    adresse = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
  
  
    objects = UtilisateursManager()
      
    USERNAME_FIELD = 'pseudo'
    REQUIRED_FIELD = []

