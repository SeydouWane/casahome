# app/routes/public_routes.py

from flask import Blueprint, render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from app.models import Famille, Ethnie, Langue
from app import db

public = Blueprint('public', __name__)

@public.route('/')
def accueil():
    return render_template('public/accueil.html')

@public.route('/trouver-famille')
@login_required
def trouver_famille():
    if current_user.is_admin:
        return redirect(url_for('admin_routes.dashboard'))

    selected_region = request.args.get('region')
    selected_ethnie = request.args.get('ethnie')
    selected_langue = request.args.get('langue')

    query = Famille.query.filter_by(is_visible=True)
    if selected_region:
        query = query.filter(Famille.region == selected_region)
    if selected_ethnie:
        query = query.filter(Famille.ethnies.any(nom=selected_ethnie))
    if selected_langue:
        query = query.filter(Famille.langues.any(nom=selected_langue))

    familles = query.all()
    regions = db.session.query(Famille.region).distinct().all()
    ethnies = db.session.query(Ethnie.nom).distinct().all()
    langues = db.session.query(Langue.nom).distinct().all()

    return render_template(
        'public/trouver_famille.html',
        familles=familles,
        regions=[r[0] for r in regions],
        ethnies=[e[0] for e in ethnies],
        langues=[l[0] for l in langues],
        selected_region=selected_region,
        selected_ethnie=selected_ethnie,
        selected_langue=selected_langue
    )

@public.route('/contact')
def contact():
    return render_template('public/contact.html')

@public.route('/a-propos')
def a_propos():
    return render_template('public/a_propos.html')

@public.route('/details-famille/<int:id>')
def details_famille(id):
    famille = Famille.query.get_or_404(id)
    return render_template('public/details_famille.html', famille=famille)
