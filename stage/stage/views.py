from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.http.request import HttpRequest
from utilisateur.forms import UtilisateurProfilModificationForm
from boutique.models import Categorie, Produit, ProduitPanier, Commande
import stripe
from utilisateur.models import Utilisateur
from django.views.decorators.csrf import csrf_exempt
from boutique.utilitaire import envoyeurmail


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
    
def panier(request:HttpRequest):
    if request.method == "GET":
       if request.user.is_authenticated:
           user = request.user
           panier = user.panier
           produitspanier = ProduitPanier.objects.filter(panier=panier)
           prixTotal = 0
           for panierpro in produitspanier:
               prixTotal += panierpro.prixTotal
           return render(request, "panier.html", {"produitspanier":produitspanier, "prixTotal":prixTotal})
       else:
           return redirect("connexion")
    else:
        return redirect("index")
    
    
    
def validerajoutpanier(request:HttpRequest):
    if request.method == "POST":
       if request.user.is_authenticated:
           user = request.user
           panier = user.panier
           
           data = request.POST
           produit_id=data.get('produit_id')
           quantite=data.get('num-product')
           
           if produit_id is None or quantite is None:
               return redirect("produits")
           
           try:
               produit_id = int(produit_id)
               quantite = int(quantite)
           except:
                return redirect("produits")
            
           try:
               monproduit=Produit.objects.get(pk=produit_id)
               if quantite > monproduit.quantite:
                  return redirect("produits")
               
               if ProduitPanier.objects.filter(produit=monproduit, panier=panier).exists():
                   produitExistant = ProduitPanier.objects.get(produit=monproduit, panier=panier)
                   nouvellequantite = produitExistant.quantiteSouhaite + quantite
                   produitExistant.quantiteSouhaite=nouvellequantite
                   produitExistant.prixTotal=produitExistant.prix * nouvellequantite
                   produitExistant.save()
                   return redirect("panier")
                 
               produitpanier = ProduitPanier() 
               produitpanier.produit = monproduit
               produitpanier.quantiteSouhaite = quantite
               produitpanier.prix = monproduit.prix
               produitpanier.prixTotal = monproduit.prix * quantite
               produitpanier.panier = panier
               produitpanier.save()
               return redirect("panier")
           except:
                return redirect("produits")

       else:
           return redirect("connexion")
    else:
        return redirect("index")
    
def viderpanier(request:HttpRequest):
    if request.method=="GET":
        if request.user.is_authenticated:
            user = request.user
            panier = user.panier
            mesProduitsPanier = ProduitPanier.objects.filter(panier=panier)
            if mesProduitsPanier.exists():
                for product in mesProduitsPanier:
                    product.delete()
                    
            return redirect("panier")
        else:
            return redirect("produits")
    else:
        return redirect("produits")
    
    
def procederpaiement(request:HttpRequest):
    if request.method == "POST":
        if request.user.is_authenticated:
            user = request.user
            panier = user.panier
            produitspanier = ProduitPanier.objects.filter(panier=panier)
            prixTotal = 0
            for panierpro in produitspanier:
               prixTotal += panierpro.prixTotal
            
            try:
                data = request.POST
                adresse_livraison = data.get("adresse_livraison")

                if adresse_livraison is None or (len(adresse_livraison.strip()) <10):
                    return redirect("panier")
                
                domain_url = "http://localhost:8000"
                stripe.api_key = "sk_test_51PfpVoBrMnkWcD7ZDIWZB1RPsnyezDrSHa4nayFcECy1GmCgBHPHJOSPuoUNeOlqtt77DMvIXeQX9sjNeu9Rmali00W9DfRzMm"
                try:
                    # Create new Checkout Session for the order
                    # Other optional params include:
                    # [billing_address_collection] - to display billing address details on the page
                    # [customer] - if you have an existing Stripe Customer ID
                    # [payment_intent_data] - capture the payment later
                    # [customer_email] - prefill the email input in the form
                    # For full details see https://stripe.com/docs/api/checkout/sessions/create

                    # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
                    checkout_session = stripe.checkout.Session.create(
                        success_url=domain_url + f"/paiementeffectuer/",
                        cancel_url=domain_url + f"/paiementannuler/",
                        payment_method_types=['card'],
                        mode='payment',
                        line_items=[
                            {
                                'price_data':{
                                    'currency': 'cad',
                                    'unit_amount': (int(prixTotal) * 100),
                                    'product_data':{
                                        'name': "Paiement du panier",
                                        'description': f"Ceci Sont les frais de paiement de votre panier L&H store",
                                        'images': ['https://img.freepik.com/vecteurs-libre/creation-logo-local-magasin-dessine-main_23-2149575766.jpg?t=st=1721766548~exp=1721770148~hmac=ad1b963a1ace448384e402b4daa111f1e6bdf178529f2781fbf34d3e280f703a&w=740'],
                                    }
                                },
                                'quantity': 1,
                            }
                        ],
                        metadata = {
                            "adresse_livraison" : adresse_livraison,
                            "panier_pk":panier.pk,
                            "user_pseudo":user.pseudo
                        }
                    )
                    return redirect(checkout_session.url,code=303)
                except Exception:
                    return redirect('panier')
                
            except Exception:
                return redirect('panier')      
        else:
            return redirect("produits")
    else:
        return redirect("produits")
 
def paiementannuler(request:HttpRequest):     
    return render(request, "paiementannuler.html")

def paiementeffectuer(request:HttpRequest):     
    return render(request, "paiementeffectuer.html")

@csrf_exempt
def procederpaiementwebhook(request:HttpRequest):
    stripe.api_key = "sk_test_51PfpVoBrMnkWcD7ZDIWZB1RPsnyezDrSHa4nayFcECy1GmCgBHPHJOSPuoUNeOlqtt77DMvIXeQX9sjNeu9Rmali00W9DfRzMm"
    endpoint_secret = "whsec_29c7766136d5857290f807f425d469e8bd2f7eef5ff3c3550b1ae1952de70f7e"
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        return HttpResponse("Value Error",status=400)
    except stripe.error.SignatureVerificationError as ex:
        return HttpResponse("Invalid signature",status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # Attention : Le print n'est pas fait dans la console dans laquelle stripe est lancé 
        # Le print est fait dans la console dans laquelle django est lancé en dev
        metadatas = event["data"]["object"]["metadata"]
        idSession = event["data"]["object"]["id"]
        user_pseudo = metadatas["user_pseudo"]
        adresse_livraison = metadatas["adresse_livraison"]
        panier_pk = metadatas["panier_pk"]

        
        try:
            utilisateur = Utilisateur.objects.get(pseudo=user_pseudo)
            # panier = utilisateur.panier
            produitspanier = ProduitPanier.objects.filter(panier=panier_pk)
            articlescommandes = ""
            for produitpan in produitspanier:
                articlescommandes += f"Nom : {produitpan.produit.nom} - Quantité : {produitpan.quantiteSouhaite} \n"
                produitvrai = produitpan.produit
                produitvrai.quantite = produitvrai.quantite - produitpan.quantiteSouhaite
                produitvrai.save()
                produitpan.delete()
                
            commande = Commande()
            commande.utilisateur = utilisateur
            commande.articles = articlescommandes
            commande.adresse = adresse_livraison
            commande.save()
          
            envoyeurmail.envoyer_commande_client_email(
                emailclient=user_pseudo,
                prenom=utilisateur.prenom,
                nom = utilisateur.nom,
                articles=articlescommandes
                
                
            )
            
            return HttpResponse(status=200)
        except Exception as ex:
            print(ex)
            return HttpResponse("Une erreur critique est arrivée",status=400)
        
    return HttpResponse(status=200)
