from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()

# 🔄 Relations plusieurs-à-plusieurs entre Famille ↔ Ethnie et Famille ↔ Langue
famille_ethnies = db.Table('famille_ethnies',
    db.Column('famille_id', db.Integer, db.ForeignKey('famille.id')),
    db.Column('ethnie_id', db.Integer, db.ForeignKey('ethnie.id'))
)

famille_langues = db.Table('famille_langues',
    db.Column('famille_id', db.Integer, db.ForeignKey('famille.id')),
    db.Column('langue_id', db.Integer, db.ForeignKey('langue.id'))
)

# 🔐 Utilisateur : Touriste ou Admin
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    mot_de_passe = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    demandes = db.relationship('DemandeSejour', backref='touriste', lazy=True)

# 🏡 Famille hôte
class Famille(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_famille = db.Column(db.String(100), nullable=False)
    region = db.Column(db.String(100), nullable=False)
    is_visible = db.Column(db.Boolean, default=True) 
    ville = db.Column(db.String(100))
    localisation = db.Column(db.String(255))
    taille_famille = db.Column(db.Integer)
    photo = db.Column(db.String(255), nullable=True)

    # Relations M2M
    ethnies = db.relationship('Ethnie', secondary=famille_ethnies, backref='familles')
    autres_ethnies = db.Column(db.Text)

    langues = db.relationship('Langue', secondary=famille_langues, backref='familles')
    autres_langues = db.Column(db.Text)

    photo_principale = db.Column(db.String(255))  # chemin image
    video_presentation = db.Column(db.String(255))  # chemin vidéo

    statut = db.Column(db.String(50), default="En attente")  # Validée, Inactive...
    visible_public = db.Column(db.Boolean, default=True)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

    description = db.Column(db.Text)

    membres = db.relationship('MembreFamille', backref='famille', cascade="all, delete-orphan")
    activites = db.relationship('ActiviteFamille', backref='famille', cascade="all, delete-orphan")
    demandes = db.relationship('DemandeSejour', backref='famille', cascade="all, delete-orphan")

# 👨‍👩‍👧‍👦 Membre de la famille
class MembreFamille(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100))
    prenom = db.Column(db.String(100))
    age = db.Column(db.Integer)
    fonction = db.Column(db.String(100))
    langues = db.Column(db.String(200))  # Ex : "Français, Jola"
    description = db.Column(db.Text)
    photo = db.Column(db.String(200))
    famille_id = db.Column(db.Integer, db.ForeignKey('famille.id'), nullable=False)

# 🎉 Activité proposée
class ActiviteFamille(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_activite = db.Column(db.String(100))
    description = db.Column(db.Text)
    media = db.Column(db.String(255))  # image ou vidéo
    famille_id = db.Column(db.Integer, db.ForeignKey('famille.id'), nullable=False)

# 📬 Demande de séjour
class DemandeSejour(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_demande = db.Column(db.DateTime, default=datetime.utcnow)
    statut = db.Column(db.String(50), default="En attente")  # Validée, Refusée...
    message = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    famille_id = db.Column(db.Integer, db.ForeignKey('famille.id'), nullable=False)

# 📚 Ethnies disponibles pour le multiselect
class Ethnie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True)

class Langue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True)


@property
def langues(self):
    import json
    try:
        return json.loads(self.langues_parlees)
    except:
        return []

@langues.setter
def langues(self, value):
    import json
    self.langues_parlees = json.dumps(value)
