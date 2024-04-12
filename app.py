from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField
from wtforms.validators import DataRequired
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Clé secrète pour la sécurité des formulaires

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)

# Simulation des utilisateurs
users = {'admin': {'password': 'admin', 'access_level': 'total'},
         'user': {'password': 'user', 'access_level': 'lecture'}}


# Définition de la classe Utilisateur pour Flask-Login
class Utilisateur(UserMixin):
    pass


@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        user = Utilisateur()
        user.id = user_id
        return user
    return None


# Formulaire de connexion
class LoginForm(FlaskForm):
    utilisateur = StringField('Nom d\'utilisateur', validators=[DataRequired()])
    mot_de_passe = PasswordField('Mot de passe', validators=[DataRequired()])
    submit = SubmitField('Se connecter')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        utilisateur = form.utilisateur.data
        mot_de_passe = form.mot_de_passe.data

        if utilisateur in users and users[utilisateur]['password'] == mot_de_passe:
            utilisateur_obj = Utilisateur()
            utilisateur_obj.id = utilisateur
            login_user(utilisateur_obj)
            return redirect(url_for('accueil'))
        else:
            flash('Identifiant ou mot de passe incorrect', 'error')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/accueil')
@login_required
def accueil():
    return render_template('accueil.html')


if __name__ == '__main__':
    app.run(debug=True)