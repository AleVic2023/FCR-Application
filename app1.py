import flask_login
from flask import Flask, request,render_template,redirect,url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '@l3V1c2024*'


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



# Utilisateurs avec acces de lecture et acces total

users = {
    'vaco1985': {'mot_de_passe':generate_password_hash('motdepasse1'),'acces': 'lecture'},
    'aleroja8712': {'mot_de_passe':generate_password_hash('motdepasse2'),'acces': 'lecture'},
    'carola87': {'mot_de_passe':generate_password_hash('motdepasse3'), 'acces': 'total'},
    'calixto0721': {'mot_de_passe':generate_password_hash('motdepasse4') ,'acces': 'total'},
}

#Class Utilisateur por Flas-Login
class Utilisateur(UserMixin):
    pass

@login_manager.user_loader
def charger_utilisateur(identifiant):
    if identifiant in users:
        utilisateur = Utilisateur()
        utilisateur.id = identifiant
        return utilisateur
    return None




@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        utilisateur = request.form['utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        if utilisateur in users and check_password_hash(users[utilisateur]['mot_de_passe'], mot_de_passe):
            utilisateur_obj = Utilisateur()
            utilisateur_obj.id = utilisateur
            login_user(utilisateur_obj)
            acces = users[utilisateur]['acces']
            if acces == 'total':
                return  render_template('accueil_total_acces.html')
            elif acces == 'lecture':
                return  render_template('lecture.html')
        else:
            flash('Identifiant ou mot de passe incorrect', 'error')

    return render_template('login.html')


@app.route('/lecture')
@login_required
def lecture():
    clients = [
        'Client1: Nom: Achury, Prenom: Angelica, Courriel: aachury@gmail.com',
        'Client2: Nom: Langlais, Prenom: Alain, Courriel: alainlanglois15@hotmail.com',
        'Client3: Nom: Pauline, Prenom: Bellanda, Courriel: bpaul@hotmail.com',
        'Client4: Nom: Gagnon, Prenom: Benoit,Courriel: gbenoit@gmail.com'
    ]
    return render_template("lecture.html",
                           clients= clients)


@app.route('/accueil_total_acces')
@login_required
def accueil_total_acces():
    return render_template('accueil_total_acces.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Vous avez ete deconnecte avec succes')
    return render_template('login.html')



if __name__ == '__main__':
    app.run(debug=True)

