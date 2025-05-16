# Importation de la fonction de création de l'application et de l'instance SQLAlchemy
from app import create_app, db

# Importation des modèles à créer dans la base de données
from app.models import User, Task

# Création de l'application Flask avec la configuration définie
app = create_app()

# Création d'un contexte d'application pour accéder aux extensions comme SQLAlchemy
with app.app_context():
    db.create_all()  # Création des tables dans la base de données, si elles n'existent pas déjà
    print("[INFO] Base de données initialisée.")  # Message de confirmation dans la console
