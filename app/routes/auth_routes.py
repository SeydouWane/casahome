from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user
from werkzeug.security import check_password_hash
from flask_login import logout_user
from flask import redirect, url_for
from app.forms.user_forms import RegisterForm
from app.models import User
from app.forms.user_forms import LoginForm
from app import db
from werkzeug.security import generate_password_hash

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.mot_de_passe, form.mot_de_passe.data):
            login_user(user)
            flash("Connexion réussie", "success")
            return redirect(url_for('admin_routes.dashboard')) if user.is_admin else redirect(url_for('public.trouver_famille'))
        else:
            flash("Email ou mot de passe invalide", "danger")
    return render_template('auth/login.html', form=form)




@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('public.accueil'))

@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Vérifier si l'email est déjà pris
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Cet email est déjà utilisé.", "danger")
            return render_template('auth/register.html', form=form)

        user = User(
            nom=form.nom.data,
            prenom=form.prenom.data,
            email=form.email.data,
            is_admin=False  # Le touriste n’est pas admin
        )
        user.mot_de_passe = generate_password_hash(form.mot_de_passe.data)
 # suppose que tu as une méthode set_password()
        db.session.add(user)
        db.session.commit()
        flash("Compte créé avec succès. Vous pouvez maintenant vous connecter.", "success")
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html', form=form)
