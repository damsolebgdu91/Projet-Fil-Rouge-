# Importation de l'objet db pour accéder aux fonctionnalités de SQLAlchemy
from app import db

# Importation de UserMixin pour intégrer les méthodes nécessaires à Flask-Login (is_authenticated, get_id, etc.)
from flask_login import UserMixin

# -------------------------------
# Modèle représentant un utilisateur
# -------------------------------
class User(db.Model, UserMixin):
    # Clé primaire unique pour identifier l'utilisateur
    id = db.Column(db.Integer, primary_key=True)

    # Nom d'utilisateur, unique et requis (max 20 caractères)
    username = db.Column(db.String(20), unique=True, nullable=False)

    # Mot de passe (haché), requis, stocké sous forme de chaîne (longueur max 128)
    password = db.Column(db.String(128), nullable=False)

    # Relation un-à-plusieurs avec le modèle Task :
    # Chaque utilisateur peut avoir plusieurs tâches
    # backref='owner' permet à chaque tâche d'accéder à son utilisateur via `task.owner`
    # lazy=True signifie que les tâches sont chargées seulement quand on y accède
    tasks = db.relationship('Task', backref='owner', lazy=True)

# -------------------------------
# Modèle représentant une tâche
# -------------------------------
class Task(db.Model):
    # Clé primaire unique pour chaque tâche
    id = db.Column(db.Integer, primary_key=True)

    # Contenu de la tâche (texte), requis (max 100 caractères)
    content = db.Column(db.String(100), nullable=False)

    # Statut de la tâche : True si faite, False sinon (par défaut False)
    done = db.Column(db.Boolean, default=False)

    # Clé étrangère vers l'utilisateur propriétaire de la tâche
    # Cela crée un lien avec `User.id`
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
