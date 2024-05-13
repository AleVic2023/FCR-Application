import flask_login
from flask import Flask, request,render_template,redirect,url_for,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask import flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import jsonify
from app import clients

app = Flask(__name__)
app.secret_key = '@l3V1c2024*'


login_manager = LoginManager()



# CREATION DE CLASSES
class Personne:
    def __init__(self, nom, prenom, sexe):

        self.nom = nom
        self. prenom =  prenom
        self.sexe = sexe

class Client(Personne):
    compter_id = 0
    def __init__(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        super().__init__(nom, prenom, sexe)
        self.id = Client.compter_id #Atriuto id es igual a la variable
        Client.compter_id += 1
        self.date_inscriptionn = date_inscription
        self.courriel = courriel
        self.mot_de_passe = mot_de_passe


class Acteur(Personne):
    def __init__(self, nom, prenom, sexe, nom_personnage, date_debut_emploi, date_fin_emploi, cachet):
        super().__init__(nom, prenom, sexe)
        self.nom_personnage = nom_personnage
        self.date_debut_emploi = date_debut_emploi
        self.date_fin_emploi = date_fin_emploi
        self.cachet = cachet

class Employe(Personne):

    def __init__(self, nom, prenom, sexe, date_embacuhe, code_utilisateur, mot_de_passe, type_acces):
        super().__init__(nom, prenom, sexe)
        self.date_embacuhe = date_embacuhe
        self.code_utilisateur = code_utilisateur
        self.mot_de_passe = mot_de_passe
        self.type_acces = type_acces

class Cartecredit:
    def __init__(self, numero, date_expiration, code_secret):
        self.numero = numero
        self.date_expiration = date_expiration
        self.code_secret = code_secret


class Film:
    def __init__(self, nom, duree, description, acteurs,categorie):
        self.nom = nom
        self.duree = duree
        self.description = description
        self.acteurs = acteurs
        self.categorie = categorie


class Categorie:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description




#Creation de dictionaires
def garder_base_de_donnees():

    clients = [
        Client("Achury", "Angelica", "F", "2021-04-24", "aachury@gmail.com", "motdepasse1"),
        Client("Langlais", "Alain", "M", "2022-11-25", "alainlanglois15@hotmail.com", "motdepasse2"),
        Client("Pauline", "Bellanda", "F", "2023-01-15", "bpaul@hotmail.com", "motdepasse3"),
        Client("Gagnon", "Benoita", "M", "2024-03-07", "gbenoit@gmail.com", "motdepasse4")

    ]

    acteurs = [
        Acteur("Pitt", "Brad", "M", "Tyler Durden", "1999-01-01", "2000-12-31", 1000000),
        Acteur("Jolie", "Angelina", "F", "Lara Croft", "2001-01-01", "2002-12-31", 1500000),
        Acteur("Bonham", "Helena", "F", "Marla Singer", "1999-02-15", "2001-12-31", 1300000),
        Acteur("Elgort", "Ansel", "M", "Augustus Waters", "2013-01-18", "2014-11-27", 1800000)
    ]

    employes = [
        Employe("Calixto", "Victor", "M", "2019-09-06", "vaco1985", "cle123", "admin"),
        Employe("Rodriguez", "Carol", "F", "2021-02-07", "carola87", "cle456", "lecture")

    ]

    cartecredits = [

        Cartecredit(45130256987, "2025-05-31", 523),
        Cartecredit(19425683216, "2027-01-31", 712),
        Cartecredit(45192412061, "2024-09-31", 972),
        Cartecredit(28091407194, "2026-07-31", 824)
    ]

    films = [
        Film("Fight Club", 139,"Un employe de bureau insomniaque et un fabricant de savons diaboliques forment un club de lutte clandestin qui evolue beaucoup.",["Brad Pitt", "Edward Norton", "Helena Bonhamt"],'Action'),
        Film("Lara Croft: Tomb Raider", 100,"Laventuriere des jeux video Lara Croft prend vie dans un film ou elle court contre le temps et les mechants pour recuperer de puissants artefacts anciens",["Angelina Jolie", "Alicia Vikander", "Daniel Craig"],'Aventure'),
        Film("Sous la meme etoile", 120,"Depuis son enfance, Hazel a des problemes respiratoires, lobligeant a porter un tube a oxygene en permanence. Sur les conseils de sa mere, elle participe a un groupe de soutien, ou elle fait la connaissance dAugustus, qui a perdu une jambe a cause dun cancer..",["Shailene Woodley", "Ansel Elgort", "Nat Wolff"],'Romantique'),
        Film("Le secret de ses yeux", 153,"Buenos Aires. Benjamin Esposito enquete sur le meurtre violent dune jeune femme. Vingt cinq ans plus tard, il decide decrire un roman base sur cette affaire classee dont il a ete témoin et protagoniste. Benjamin replonge ainsi dans cette periode sombre de lArgentine où lambiance etait etouffante et les apparences trompeuses.",["Ricardo Darin", "ESoledad Villamil", "Guillermo Francella"],'Drame')
    ]

    categories = [
        Categorie("Action", "Des films pleins de scenes daction passionnantes."),
        Categorie("Aventure", "Des films qui vous menent a des voyages passionnants et des decouvertes."),
        Categorie("Romantique", "Films qui vous font reflechir sur les choses vraiment importantes dans la vie."),
        Categorie("Drame", "Des films qui traversent lintrigue et la recherche pour decouvrir la verite.")
    ]



    donnees = {
        "clients": [client.__dict__ for client in clients],
        "acteurs": [acteur.__dict__ for acteur in acteurs],
        "employes": [employe.__dict__ for employe in employes],
        "cartecredits":[cartecredit.__dict__ for cartecredit in cartecredits],
        "films":[film.__dict__ for film in films],
        "categories":[categorie.__dict__ for categorie in categories]

    }

#Garder ma base de donnees

    with open('data/base_de_donnees.json', 'w') as f:
        json.dump(donnees, f, indent=4)


def authenticate_employe(code_utilisateur, mot_de_passe):
    with open('data/base_de_donnees.json', 'r') as f:
        donnees = json.load(f)
        for employe in donnees["employes"]:
            if employe['code_utilisateur'] == code_utilisateur and employe['mot_de_passe'] == mot_de_passe:
                return True, employe['type_acces']
    return False, None




#Creation de routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        code_utilisateur = request.form['code_utilisateur']
        mot_de_passe = request.form['mot_de_passe']

        employe, type_acces = authenticate_employe(code_utilisateur, mot_de_passe)

        if employe:
            session['type_acces'] = type_acces
            if type_acces == "admin":
                return redirect(url_for('admin'))
            elif type_acces == "lecture":
                return redirect(url_for('lecture'))
        else:
            return render_template('login.html', erreur='Votre code utilisateur ou mot de passe sont incorrects')
    else:
        return render_template('login.html')

def obtenir_donnees():
    route_fichier = os.path.join('data', 'base_de_donnees.json')
    with open(route_fichier, 'r') as file:
        donnees = json.load(file)
    return donnees



@app.route('/admin')
def admin():
    with open('data/base_de_donnees.json', 'r') as f:
        donnees = json.load(f)
        clients = donnees['clients']
        films = donnees['films']

        if 'type_acces' in session and session['type_acces'] == 'admin':
            return render_template('admin.html', clients=clients, films=films)
        else:
            return redirect(url_for('login'))  # Redirige vers la page de connexion

def charger_donnees():
    route_fichier = os.path.join('data', 'base_de_donnees.json')
    with open(route_fichier, 'r') as file:
        donnees = json.load(file)
    return donnees

# Ruta para obtener la lista de clientes
@app.route('/clients')
def obtenir_clients():
    donnees = obtenir_donnees()
    return jsonify(donnees['clients'])


#Route pour creer un nouveau client
@app.route('/creer_client', methods=['POST'])
def creer_client():
    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    courriel = request.form.get('courriel')

    donnees = obtenir_donnees()
    clients = donnees['clients']
    nouveau_id = len(clients) + 1
    nouveau_client = {"id": nouveau_id, "nom": nom, "prenom": prenom, "courriel": courriel}
    clients.append(nouveau_client)

    route_fichier = os.path.join('data', 'base_de_donnees.json')
    with open(route_fichier, 'w') as file:
        json.dump(donnees, file, indent=4)

    return redirect('/admin')





# Ruta para modificar un cliente
@app.route('/modifier_client/<int:client_id>', methods=['POST'])
def modifier_client(client_id):
    donnees = charger_donnees()
    for client in donnees['clients']:
        if client['id'] == client_id:
            client['nom'] = request.form.get('nom')
            client['prenom'] = request.form.get('prenom')
            client['courriel'] = request.form.get('courriel')
            break
    garder_donnees(donnees)
    return redirect('/admin')


# Ruta para eliminar un cliente
@app.route('/supprimer_client', methods=['POST'])
def supprimer_client():
    client_id = int(request.form['client_id'])
    donnees = charger_donnees()
    donnees['clients'] = [client for client in donnees['clients'] if client['id'] != client_id]
    garder_donnees(donnees)
    return redirect('/admin')

# Función para guardar los datos en el archivo JSON
def garder_donnees(donnees):
    route_fichier = os.path.join('data', 'base_de_donnees.json')
    with open(route_fichier, 'w') as file:
        json.dump(donnees, file, indent=4)



# Ruta para obtener la lista de películas
@app.route('/films')
def obtenir_films():
    donnees = obtenir_donnees()
    return jsonify(donnees['films'])


@app.route('/lecture')
def lecture():
    with open('data/base_de_donnees.json', 'r') as f:
        donnees = json.load(f)
        clients = donnees['clients']
        films = donnees['films']

        if 'type_acces' in session and session['type_acces'] == 'lecture':
            return render_template('lecture.html', clients=clients, films=films)
        else:
            return redirect(url_for('login'))  # Redirige vers la page de connexion

@app.route('/logout')
def logout():
    return render_template('login.html')

# Creation des fonctions pour la templeate admin.html





if __name__ == "__main__":

    app.run(debug=True)
