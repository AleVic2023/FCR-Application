import flask_login
from flask import Flask, request,render_template,redirect,url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = '@l3V1c2024*'

# Configuration de la fenetre Login

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Utilisateurs avec acces de lecture et acces total

users = {
    'vac01985': {'mot_de_passe': 'motdepasse1', 'acces': 'lecture'},
    'aleroja8712': {'mot_de_passe': 'motdepasse2', 'acces': 'lecture'},
    'carola87': {'mot_de_passe': 'motdepasse3', 'acces': 'total'},
    'calixto0721': {'mot_de_passe': 'motdepasse4', 'acces': 'total'},
}


# Classe Utilisateur pour Flask-Login
class Utilisateur(flask_login.UserMixin):
    pass

@login_manager.user_loader
def charger_utilisateur(identifiant):
    if identifiant in users:
        utilisateur = Utilisateur()
        utilisateur.id = identifiant
        return utilisateur
    return None


@app.route('/')
def accueil():
    return render_template('accueil.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        utilisateur = request.form['utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        if utilisateur in users and users[utilisateur]['mot_de_passe'] == mot_de_passe:
            utilisateur_obj = Utilisateur()
            utilisateur_obj.id = utilisateur
            flask_login.login_user(utilisateur_obj)
            return redirect(url_for('accueil'))
        else:
            return 'Identifiant ou mot de passe incorrect'

    return render_template('login.html')


@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('accueil'))


def utilisateur_actuel():
    pass


@app.route('/contenu')
@flask_login.login_required
def contenu_protecte():
    if 'total' == users.get(utilisateur_actuel().id).get('acces'):
        return "Contenu accessible en lecture et écriture."
    else:
        return "Contenu accessible en lecture seule."


@login_manager.unauthorized_handler
def non_autorise():
    return 'Veuillez Vous connecter pour accéder à cette page.'


if __name__ == '__main__':
    app.run(debug=True)





