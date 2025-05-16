# -------------------------------
# IMPORTATIONS
# -------------------------------

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta

from app import db, bcrypt
from app.forms import RegisterForm, LoginForm, TaskForm, EditProfileForm
from app.models import User, Task

# -------------------------------
# INITIALISATION DU BLUEPRINT
# -------------------------------

main = Blueprint('main', __name__)

# -------------------------------
# SÉCURITÉ : Limitation des tentatives de login
# -------------------------------

login_attempts = {}  # Dictionnaire {username: [nb_tentatives, dernière_tentative]}
MAX_ATTEMPTS = 5  # Nombre de tentatives autorisées
BLOCK_DURATION = timedelta(minutes=5)  # Durée du blocage après trop d’échecs

# -------------------------------
# PAGE D’ACCUEIL : Redirection vers login
# -------------------------------

@main.route('/')
def index():
    return redirect(url_for('main.login'))

# -------------------------------
# INSCRIPTION
# -------------------------------

@main.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        # Vérifie si le nom d’utilisateur est déjà utilisé
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Ce nom d'utilisateur est déjà pris.", 'danger')
            return render_template('register.html', form=form)

        # Hash du mot de passe
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        # Création du nouvel utilisateur
        user = User(username=form.username.data, password=hashed_pw)
        db.session.add(user)
        db.session.commit()

        flash('Compte créé avec succès.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html', form=form)

# -------------------------------
# CONNEXION (avec limitation des tentatives)
# -------------------------------

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    username = form.username.data

    # Vérifie si le compte est bloqué temporairement
    if username in login_attempts:
        attempts, last_try = login_attempts[username]
        if attempts >= MAX_ATTEMPTS and datetime.now() - last_try < BLOCK_DURATION:
            flash("Trop de tentatives échouées. Réessayez plus tard.", "danger")
            return render_template('login.html', form=form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()

        # Vérifie si l’utilisateur existe et que le mot de passe est correct
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            login_attempts.pop(username, None)  # Réinitialise les tentatives
            flash('Connexion réussie.', 'success')
            return redirect(url_for('main.dashboard'))
        else:
            # Mise à jour du compteur d’échecs
            if username not in login_attempts:
                login_attempts[username] = [1, datetime.now()]
            else:
                login_attempts[username][0] += 1
                login_attempts[username][1] = datetime.now()

            flash("Identifiants invalides.", "danger")

    return render_template('login.html', form=form)

# -------------------------------
# TABLEAU DE BORD : liste et ajout de tâches
# -------------------------------

@main.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()

    if form.validate_on_submit():
        # Crée une nouvelle tâche liée à l’utilisateur connecté
        task = Task(content=form.content.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Tâche ajoutée.", "success")
        return redirect(url_for('main.dashboard'))

    # Récupère toutes les tâches de l’utilisateur courant
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', form=form, tasks=tasks)

# -------------------------------
# SUPPRESSION DE COMPTE
# -------------------------------

@main.route('/delete_account', methods=['POST'])
@login_required
def delete_account():
    # Supprime toutes les tâches de l’utilisateur
    Task.query.filter_by(user_id=current_user.id).delete()

    # Supprime le compte utilisateur
    db.session.delete(current_user)
    db.session.commit()

    # Déconnexion de l’utilisateur
    logout_user()
    flash("Votre compte a bien été supprimé.", "info")
    return redirect(url_for('main.register'))

# -------------------------------
# SUPPRESSION D’UNE TÂCHE
# -------------------------------

@main.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    # Récupère la tâche uniquement si elle appartient à l’utilisateur
    task = Task.query.filter_by(id=task_id, user_id=current_user.id).first_or_404()
    db.session.delete(task)
    db.session.commit()
    flash("Tâche supprimée.", "info")
    return redirect(url_for('main.dashboard'))

# -------------------------------
# MODIFICATION DU PROFIL
# -------------------------------

@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        # Mise à jour du nom d’utilisateur
        current_user.username = form.username.data

        # Mise à jour du mot de passe si champ rempli
        if form.password.data:
            hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_pw

        db.session.commit()
        flash("Profil mis à jour.", "success")
        return redirect(url_for('main.dashboard'))

    # Préremplit le champ avec l’ancien nom d’utilisateur
    form.username.data = current_user.username
    return render_template('profile.html', form=form)

# -------------------------------
# DÉCONNEXION
# -------------------------------

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Déconnexion réussie.', 'info')
    return redirect(url_for('main.login'))
