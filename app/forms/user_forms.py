from wtforms import EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired()])
    submit = SubmitField("Connexion")

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

class RegisterForm(FlaskForm):
    prenom = StringField("Prénom", validators=[DataRequired()])
    nom = StringField("Nom", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    mot_de_passe = PasswordField("Mot de passe", validators=[DataRequired()])
    confirmer = PasswordField("Confirmer le mot de passe", validators=[
        DataRequired(),
        EqualTo('mot_de_passe', message="Les mots de passe doivent correspondre")
    ])
    submit = SubmitField("Créer un compte")
