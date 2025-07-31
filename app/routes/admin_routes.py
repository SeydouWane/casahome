# app/routes/admin_routes.py

from flask import Blueprint, render_template, abort, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Famille, DemandeSejour, ActiviteFamille, User, Ethnie, Langue
from app.forms.admin_forms import FamilleForm
from app import db

admin_routes = Blueprint('admin_routes', __name__)

admin = Blueprint('admin', __name__)

# 📊 Dashboard principal
@admin_routes.route('/dashboard')
@login_required
def dashboard():
    if not getattr(current_user, "is_admin", False):
        abort(403)
    
    nb_familles = Famille.query.count()
    nb_demandes = DemandeSejour.query.count()
    nb_activites = ActiviteFamille.query.count()

    return render_template('admin/dashboard.html',
                           nb_familles=nb_familles,
                           nb_demandes=nb_demandes,
                           nb_activites=nb_activites)


# 📋 Liste des familles
@admin_routes.route('/admin/familles')
@login_required
def liste_familles():
    if not current_user.is_admin:
        abort(403)

    familles = Famille.query.all()
    return render_template('admin/liste_familles.html', familles=familles)


# 📋 Liste des demandes
@admin_routes.route('/admin/demandes')
@login_required
def liste_demandes():
    if not current_user.is_admin:
        abort(403)

    demandes = DemandeSejour.query.all()
    return render_template('admin/liste_demandes.html', demandes=demandes)


# 👥 Liste des utilisateurs
@admin_routes.route('/admin/utilisateurs')
@login_required
def liste_utilisateurs():
    if not current_user.is_admin:
        abort(403)

    utilisateurs = User.query.all()
    return render_template('admin/liste_utilisateurs.html', utilisateurs=utilisateurs)


# ➕ Ajout d'une famille
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'app/static/images/familles'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
@admin_routes.route('/admin/familles/ajouter', methods=['GET', 'POST'])
@login_required
def creer_famille():
    if not current_user.is_admin:
        abort(403)

    form = FamilleForm()
    if form.validate_on_submit():
        filename = None
        if form.photo_principale.data:
            file = form.photo_principale.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Création de l'objet famille avec les ethnies/langues déjà sélectionnées
        famille = Famille(
            nom_famille=form.nom_famille.data,
            region=form.region.data,
            ville=form.ville.data,
            localisation=form.localisation.data,
            taille_famille=int(form.taille_famille.data) if form.taille_famille.data else None,
            ethnies=form.ethnies.data,
            langues=form.langues.data,
            autres_ethnies=form.autres_ethnies.data,
            autres_langues=form.autres_langues.data,
            description=form.description.data,
            photo_principale=filename
        )

        db.session.add(famille)

        # ✅ Ajout dynamique d'une ethnie si saisie manuelle
        if form.autres_ethnies.data:
            nouvelle_ethnie = Ethnie(nom=form.autres_ethnies.data.strip())
            db.session.add(nouvelle_ethnie)
            famille.ethnies.append(nouvelle_ethnie)

        # ✅ Ajout dynamique d'une langue si saisie manuelle
        if form.autres_langues.data:
            nouvelle_langue = Langue(nom=form.autres_langues.data.strip())
            db.session.add(nouvelle_langue)
            famille.langues.append(nouvelle_langue)

        db.session.commit()
        flash("Famille ajoutée avec succès.", "success")
        return redirect(url_for('admin_routes.liste_familles'))

    return render_template("admin/creer_famille.html", form=form)

@admin_routes.route('/admin/familles/<int:famille_id>')
@login_required
def details_famille(famille_id):
    if not current_user.is_admin:
        abort(403)

    famille = Famille.query.get_or_404(famille_id)
    return render_template('admin/details_famille.html', famille=famille)

@admin_routes.route('/admin/familles/<int:famille_id>/supprimer', methods=['GET'])
@login_required
def supprimer_famille(famille_id):
    if not current_user.is_admin:
        abort(403)

    famille = Famille.query.get_or_404(famille_id)
    db.session.delete(famille)
    db.session.commit()
    flash("Famille supprimée avec succès.", "success")
    return redirect(url_for('admin_routes.liste_familles'))
