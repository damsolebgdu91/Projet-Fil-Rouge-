# Importation des outils Flask-WTF et des champs WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, EqualTo, Regexp, Optional


# Formulaire d'inscription d'un nouvel utilisateur
class RegisterForm(FlaskForm):
    username = StringField(
        'Nom d’utilisateur',
        validators=[
            DataRequired(message="Le nom d’utilisateur est requis."),  # Le champ ne doit pas être vide
            Length(min=3, max=20, message="Le nom doit contenir entre 3 et 20 caractères."),
            Regexp(r'^[A-Za-z0-9_]+$', message="Le nom ne doit contenir que des lettres, chiffres ou underscores.")
        ]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[
            DataRequired(message="Le mot de passe est requis."),
            Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères.")
        ]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            DataRequired(message="Veuillez confirmer le mot de passe."),
            EqualTo('password', message="Les mots de passe doivent correspondre.")  # Vérifie la correspondance
        ]
    )
    submit = SubmitField('S’inscrire')  # Bouton de soumission


# Formulaire de connexion utilisateur
class LoginForm(FlaskForm):
    username = StringField(
        'Nom d’utilisateur',
        validators=[
            DataRequired(message="Le nom d’utilisateur est requis.")
        ]
    )
    password = PasswordField(
        'Mot de passe',
        validators=[
            DataRequired(message="Le mot de passe est requis.")
        ]
    )
    remember = BooleanField('Se souvenir de moi')  # Case à cocher pour la session persistante
    submit = SubmitField('Connexion')


# Formulaire pour ajouter une nouvelle tâche
class TaskForm(FlaskForm):
    content = StringField(
        'Nouvelle tâche',
        validators=[
            DataRequired(message="Le contenu de la tâche est requis."),
            Length(min=1, max=100, message="La tâche doit contenir entre 1 et 100 caractères."),
            Regexp(
                r'^[A-Za-z0-9À-ÿ\s\.,!?()\'"-]+$',
                message="Caractères non autorisés."  # Autorise lettres, chiffres, ponctuation courante
            )
        ]
    )
    submit = SubmitField('Ajouter')  # Bouton pour ajouter la tâche


# Formulaire de modification du profil utilisateur
class EditProfileForm(FlaskForm):
    username = StringField(
        'Nouveau nom d’utilisateur',
        validators=[
            DataRequired(message="Le nom d’utilisateur est requis."),
            Length(min=3, max=20, message="Le nom doit contenir entre 3 et 20 caractères."),
            Regexp(r'^[A-Za-z0-9_]+$', message="Caractères autorisés : lettres, chiffres, underscore.")
        ]
    )
    password = PasswordField(
        'Nouveau mot de passe',
        validators=[
            Optional(),  # Le champ peut être laissé vide
            Length(min=8, message="Le mot de passe doit contenir au moins 8 caractères.")
        ]
    )
    confirm_password = PasswordField(
        'Confirmer le mot de passe',
        validators=[
            Optional(),
            EqualTo('password', message="Les mots de passe doivent correspondre.")  # Vérifie la correspondance si rempli
        ]
    )
    submit = SubmitField('Mettre à jour')  # Bouton pour mettre à jour le profil
