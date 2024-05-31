#Utilisation de microframework (flask) de python qui me permet de crrer des applications
import flask_login
from flask import Flask, request,render_template,redirect,url_for,session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user
from flask import flash
import json
import os
import jsonify
from app import clients


app = Flask(__name__)
app.secret_key = '@l3V1c2024*'


login_manager = LoginManager()
route_fichier = os.path.join('data', 'base_de_donnees.json')



# CREATION DE CLASSES
class Personne:
    def __init__(self, nom, prenom, sexe):

        self.nom = nom
        self. prenom =  prenom
        self.sexe = sexe

#La classe Client hérite de la classe Personne
class Client(Personne):
    compter_id = 1
    def __init__(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        super().__init__(nom, prenom, sexe)
        self.id = Client.compter_id
        Client.compter_id += 1 #Avec cette fonction l’identificateur est attaché automatiquement chaque fois qu’un client est créé
        self.date_inscription = date_inscription
        self.courriel = courriel
        self.mot_de_passe = mot_de_passe

#La classe Acteur hérite de la classe Personne
class Acteur(Personne):
    def __init__(self, nom, prenom, sexe, nom_personnage, date_debut_emploi, date_fin_emploi, cachet):
        super().__init__(nom, prenom, sexe)
        self.nom_personnage = nom_personnage
        self.date_debut_emploi = date_debut_emploi
        self.date_fin_emploi = date_fin_emploi
        self.cachet = cachet

#La classe Employe hérite de la classe Personne
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




#Création de dictionnaires (Les donnees pour le développement de l’application)

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

 # Organisation des données à enregistrer dans un fichier json
    donnees = {
        "clients": [client.__dict__ for client in clients],
        "acteurs": [acteur.__dict__ for acteur in acteurs],
        "employes": [employe.__dict__ for employe in employes],
        "cartecredits":[cartecredit.__dict__ for cartecredit in cartecredits],
        "films":[film.__dict__ for film in films],
        "categories":[categorie.__dict__ for categorie in categories]

    }

#Création d efichier json comment base de données

    with open('data/base_de_donnees.json', 'w') as f:
        json.dump(donnees, f, indent=4)


#Définition de l’authentification des données des employés
def authenticate_employe(code_utilisateur, mot_de_passe):
    with open('data/base_de_donnees.json', 'r') as f:
        donnees = json.load(f)
        for employe in donnees["employes"]:
            if employe['code_utilisateur'] == code_utilisateur and employe['mot_de_passe'] == mot_de_passe:
                return True, employe['type_acces']
    return False, None



#Création de routes

#Page principale
@app.route('/')
def index():
    return render_template('index.html')

#Page de login pour l’authentification
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
            flash ('Votre code utilisateur ou mot de passe sont incorrects','erreur')

    return render_template('login.html')

#Définition pour obtenir les données du fichier
def obtenir_donnees():
    route_fichier = os.path.join('data', 'base_de_donnees.json')
    with open(route_fichier, 'r') as file:
        donnees = json.load(file)
    return donnees

#Page d’accès pour l’administrateur
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



#Route pour créer un nouveau client quand la personne clique sur le bouton creer client
@app.route('/creer_client', methods=['GET','POST'])
def creer_client():
    if request.method == 'POST':
        nom = request.form.get('nom')
        prenom = request.form.get('prenom')
        courriel = request.form.get('courriel')
        mot_de_passe= request.form.get('mot_de_passe')
        route_fichier = os.path.join('data', 'base_de_donnees.json')

#Ici, le programme ouvre le fichier json et lit les données
        with open(route_fichier, 'r') as file:
            donnees = json.load(file)

#En ouvrant le fichier on valide que le  courriel soit unique

        courriels_existants = [client["courriel"] for client in donnees['clients']]
        if courriel in courriels_existants:
            flash("ce courriel existe déjà, s’il vous plaît entrer un courriel différent")
            return render_template('creer_client.html')

        # Validation de longeur de mot de passe
        if len(mot_de_passe) < 8:
            flash("Le mot de passe doit etre compose au moins 8 caracteres")
            return render_template('creer_client.html')

        # Obtenir ID maximun pour ajouter le nouveau dans la création de nouveau client

        max_id = max([client["id"] for client in donnees['clients']])
        nouveau_id = max_id + 1
        nouveau_client = {"id": nouveau_id, "nom": nom, "prenom": prenom, "courriel": courriel,'mot_de_passe':mot_de_passe}
        donnees['clients'].append(nouveau_client)
        donnees['dernier_id_client'] = nouveau_id

#Le programme garde les nouveaux données dans le fichier
        with open(route_fichier, 'w') as file:
             json.dump(donnees, file, indent=4)
        flash('Vous avez cree un nouveau client', 'success')
        return redirect('/admin')
    else:
        return render_template('creer_client.html')

#Définition de la fonction obtenir_client
def obtenir_client(client_id):
    try:
        client_id = int(client_id)  # Il faut convertir l’ID client en entier
    except ValueError:
        return None  # si l’ID du client n’est pas un nombre entier valide, renvoyer à None

    if client_id <= 0:
        return None  # Retourner None si l’ID du client est inférieur ou égal à zero

    if not os.path.exists(route_fichier):
        return None  # Si le fichier n'existe pas, retourner None

    with open(route_fichier, 'r') as file:
        try:
            donnees = json.load(file)

        except json.JSONDecodeError as e:
            return None  # Retourner None si le fichier JSON ne peut pas être décodé

        # Accéder à la liste des clients dans le dictionnaire 'données’
        clients = donnees.get('clients', [])
        for client in clients:
            if isinstance(client, dict) and client.get('id') == client_id:
                return client
    return None


#Création de route  pour la modification de clients
@app.route('/modifier_client', methods=['GET', 'POST'])
def modifier_client():
    if request.method == 'POST':
        try:
            client_id = int(request.form.get('client_id'))
        except (TypeError, ValueError) as e:
            print(f"Invalid client ID: {e}")  # Debug
            flash("ID du client non valide.", "error")
            return redirect('/modifier_client')

        client = obtenir_client(client_id)
        print(f"Client obtained: {client}")  # Debug

        if client:
            nom = request.form.get('nom')
            prenom = request.form.get('prenom')
            courriel = request.form.get('courriel')
            mot_de_passe = request.form.get('mot_de_passe')

            if not nom or not prenom or not courriel or not mot_de_passe:
                flash("Tous les champs sont obligatoires.", "error")
                return redirect('/modifier_client')

            # Validation de courriel unique
            with open(route_fichier, 'r') as file:
                donnees = json.load(file)


            clients = donnees.get('clients', [])
            courriels_existants = [c['courriel'] for c in clients if c['id'] != client_id]
            if courriel in courriels_existants:
                flash("Ce courriel existe déjà. Veuillez entrer un courriel différent.", "error")
                return redirect('/modifier_client')

            # Validation de longueur de mot de passe
            if len(mot_de_passe) < 8:
                flash("Le mot de passe doit comporter au moins 8 caractères.", "error")
                return redirect('/modifier_client')

            # Actualiser les donnés de clients
            for c in clients:
                if isinstance(c, dict) and c['id'] == client_id:
                    c['nom'] = nom
                    c['prenom'] = prenom
                    c['courriel'] = courriel
                    c['mot_de_passe'] = mot_de_passe
                    break

            # Sauvegarder les données des clients actualisés
            with open(route_fichier, 'w') as file:
                json.dump(donnees, file, indent=4)

            #Flash me permet de montrer les messages
            flash("Les données du client ont été mises à jour avec succès.", "success")
            return redirect('/admin')
        else:
            flash("Client non trouvé. Veuillez vérifier l'ID du client.", "error")
            return redirect('/modifier_client')
    else:
        client_id = request.args.get('client_id')
        if client_id:
            client = obtenir_client(client_id)

            if client:
                return render_template('modifier_client.html', client=client)
            else:
                flash("Client non trouvé. Veuillez vérifier l'ID du client.", "error")
                return redirect('/admin')
        else:
            return render_template('modifier_client.html', client=None)




# Route pour supprimer un client a travers l’id
@app.route('/supprimer_client', methods=['POST'])
def supprimer_client():
    client_id = int(request.form['client_id'])
    donnees = obtenir_donnees()
    donnees['clients'] = [client for client in donnees['clients'] if client['id'] != client_id]
    garder_donnees(donnees)
    flash("Vous avez supprimé correctement le client.", "success")
    return redirect('/admin')


# Fonction pour garder les donnees dans le fichier json
def garder_donnees(donnees):
    route_fichier = os.path.join('data', 'base_de_donnees.json')
    with open(route_fichier, 'w') as file:
        json.dump(donnees, file, indent=4)



# Route pour obtenir les films
@app.route('/films')
def obtenir_films():
    donnees = obtenir_donnees()
    return jsonify(donnees['films'])

#Route pour l’accès de seule lecture
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


# Route pour la deconnexion
@app.route('/logout')
def logout():
    flash('Vous avez ete deconnecte avec succes', 'success')
    return redirect(url_for('login'))


@app.route('/retourner')
def retourner():
    return redirect(url_for('admin'))


if __name__ == "__main__":
    app.run(debug=True)
