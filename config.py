import os  # Module pour interagir avec les variables d’environnement du système

class Config:
    # Clé secrète utilisée par Flask pour sécuriser les sessions, les cookies, les formulaires CSRF, etc.
    # Si la variable d'environnement 'SECRET_KEY' est définie, on l'utilise ; sinon, on utilise 'dev_key' par défaut.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key'

    # URI de connexion à la base de données. Flask-SQLAlchemy l’utilise pour se connecter au SGBD.
    # Ici, on essaye d'abord de lire l'URL depuis la variable d'environnement 'DATABASE_URL'.
    # Si elle n'est pas définie, on utilise une base locale MariaDB/MySQL par défaut :
    #   - utilisateur : todo_user
    #   - mot de passe : motdepasse
    #   - hôte : localhost
    #   - base : todo_db
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') or
        'mysql+pymysql://todo_user:motdepasse@localhost/todo_db'
    )

    # Désactive le système de suivi des modifications d’objet pour économiser des ressources.
    SQLALCHEMY_TRACK_MODIFICATIONS = False
