from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Utilisateur
from django import forms

class UtilisateurCreationForm(UserCreationForm):
    class Meta:
        model = Utilisateur
        fields = ('pseudo',)
        
class UtilisateurChangeForm(UserChangeForm):
    class Meta:
        model = Utilisateur
        fields = ('pseudo',)
        
        
class UtilisateurProfilModificationForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['nom', 'prenom', 'adresse']
        labels ={
            'nom':"Votre nom",
            'prenom':"Votre prenom",
            'adresse':"Votre adresse"
        }
        
        widgets = {
            'nom': forms.TextInput(attrs={'class':"stext-111 cl2 plh3 size-116 p-l-62 p-r-30"}),
            'prenom': forms.TextInput(attrs={'class':"stext-111 cl2 plh3 size-116 p-l-62 p-r-30"}),
            'adresse': forms.TextInput(attrs={'class':"stext-111 cl2 plh3 size-116 p-l-62 p-r-30"})
        }
        
        error_messages = {
            'nom':{
                'required': "Le champ nom est obligatoire",
            }
        }