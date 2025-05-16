# Importation des modules nécessaires à l'application Flask
from flask import Flask  # Framework web principal
from flask_sqlalchemy import SQLAlchemy  # ORM (Object Relational Mapper) pour interagir avec la base de données
from flask_login import LoginManager  # Gestion des sessions utilisateur (authentification)
from flask_bcrypt import Bcrypt  # Pour le hachage sécurisé des mots de passe
from config import Config  # Fichier de configuration personnalisé

# Initialisation des extensions sans les lier à l'application (elles le seront plus tard dans create_app)
db = SQLAlchemy()  # Base de données SQLAlchemy
login_manager = LoginManager()  # Gestionnaire de connexion Flask-Login
bcrypt = Bcrypt()  # Outil pour le hachage des mots de passe

# Configuration de Flask-Login
login_manager.login_view = 'main.login'  # Nom de la vue à afficher lorsqu’un utilisateur non connecté tente d'accéder à une page protégée
login_manager.login_message_category = 'info'  # Catégorie de message flash affichée quand un utilisateur est redirigé vers la page de login

# Fonction d'usine pour créer une instance de l'application Flask
def create_app():
    app = Flask(__name__)  # Création de l'application Flask
    print("[INFO] Initialisation de l'application Flask...")  # Message d'information dans la console

    app.config.from_object(Config)  # Chargement de la configuration à partir de la classe Config

    # Liaison des extensions avec l'application Flask
    db.init_app(app)  # Initialisation de SQLAlchemy avec l'application
    login_manager.init_app(app)  # Initialisation de Flask-Login avec l'application
    bcrypt.init_app(app)  # Initialisation de Flask-Bcrypt avec l'application

    # Importation du modèle User ici pour éviter les imports circulaires
    from app.models import User

    # Déclaration de la fonction permettant de charger un utilisateur par son ID (requis par Flask-Login)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))  # Recherche de l'utilisateur par son ID (converti en int)

    # Importation et enregistrement des routes définies dans le blueprint principal
    from app.routes import main
    app.register_blueprint(main)  # Enregistrement du blueprint 'main' (routes de l'application)

    print("[INFO] Application prête.")  # Message indiquant que tout est prêt
    return app  # Retour de l'application Flask configurée
