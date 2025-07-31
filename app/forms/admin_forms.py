from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField, SubmitField, SelectField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from app.models import Ethnie, Langue

class FamilleForm(FlaskForm):
    nom_famille = StringField("Nom de la famille", validators=[DataRequired()])
    
    region = SelectField("Région", choices=[
        ('Ziguinchor', 'Ziguinchor'), ('Kolda', 'Kolda'),
        ('Sédhiou', 'Sédhiou'), ('Dakar', 'Dakar'),
        ('Thiès', 'Thiès'), ('Saint-Louis', 'Saint-Louis')
    ], validators=[DataRequired()])

    ville = StringField("Ville", validators=[DataRequired()])
    localisation = StringField("Localisation (ex: quartier, rue...)")
    taille_famille = StringField("Nombre de membres")

    # Champs dynamiques depuis la base
    ethnies = QuerySelectMultipleField("Ethnie(s)", 
        query_factory=lambda: Ethnie.query.all(),
        get_label='nom', allow_blank=True)

    autres_ethnies = StringField("Autre(s) ethnie(s)")

    langues = QuerySelectMultipleField("Langue(s)", 
        query_factory=lambda: Langue.query.all(),
        get_label='nom', allow_blank=True)

    autres_langues = StringField("Autre(s) langue(s)")

    description = TextAreaField("Description de la famille")
    photo_principale = FileField("Photo de la famille")
    submit = SubmitField("Créer la famille")
