# Importation de la fonction de création de l'application depuis le package app
from app import create_app

# Création de l'instance de l'application Flask à l'aide de la fonction d'usine
app = create_app()

# Vérifie que le script est exécuté directement (et non importé comme module)
if __name__ == "__main__":
    # Démarrage du serveur Flask avec les paramètres suivants :
    app.run(
        host="127.0.0.1",  # Adresse IP locale : le serveur ne sera accessible que depuis la machine locale
        port=5000,  # Port utilisé pour accéder à l'application
        debug=True,  # Active le mode debug : rechargement automatique et affichage des erreurs détaillées
        ssl_context=("cert.pem", "key.pem")  # Active le HTTPS avec un certificat SSL local (auto-signé ou généré)
        # "cert.pem" : certificat public, "key.pem" : clé privée
    )
