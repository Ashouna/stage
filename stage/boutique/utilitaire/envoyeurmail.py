from django.core.mail import EmailMessage
from django.template.loader import render_to_string
sender_email = "nepasrepondre@laurastore.com"


def envoyer_commande_client_email(emailclient,prenom,nom,articles):
    variables = {
        'prenom': prenom,
        'nom': nom,
        'articles':articles,
        'emailclient': emailclient
    }

    html_content = render_to_string('email/commandeclient.html', variables)

    msg = EmailMessage("Commande Recue - Laura store", html_content, sender_email, [emailclient])
    msg.content_subtype = "html"
    msg.send()
