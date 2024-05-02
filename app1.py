import json
from flask import Flask, render_template, request, redirect, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required

app = Flask(__name__)
app.secret_key = 'cle_secret'

class Personne:
    def __init__(self, nom, prenom, sexe):
        self.nom = nom
        self. prenom =  prenom
        self.sexe = sexe

class Client(Personne):
    def __init__(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        super().__init__(nom, prenom, sexe)
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
    def __init__(self, nom, duree, description, acteurs):
        self.nom = nom
        self.duree = duree
        self.description = description
        self.acteurs = acteurs


class Categorie:
    def __init__(self, nom, description):
        self.nom = nom
        self.description = description





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
        Film("Fight Club", 139,"Un employé de bureau insomniaque et un fabricant de savons diaboliques forment un club de lutte clandestin qui évolue beaucoup.",["Brad Pitt", "Edward Norton", "Helena Bonhamt"]),
        Film("Lara Croft: Tomb Raider", 100,"L’aventurière des jeux vidéo Lara Croft prend vie dans un film où elle court contre le temps et les méchants pour récupérer de puissants artefacts anciens",["Angelina Jolie", "Alicia Vikander", "Daniel Craig"]),
        Film("Sous la même étoile", 120,"Depuis son enfance, Hazel a des problèmes respiratoires, l'obligeant à porter un tube à oxygène en permanence. Sur les conseils de sa mère, elle participe à un groupe de soutien, où elle fait la connaissance d'Augustus, qui a perdu une jambe à cause d'un cancer..",["Shailene Woodley", "Ansel Elgort", "Nat Wolff"]),
        Film("Le secret de ses yeux", 153,"Buenos Aires. Benjamin Esposito enquête sur le meurtre violent d'une jeune femme. Vingt-cinq ans plus tard, il décide d'écrire un roman basé sur cette affaire classée dont il a été témoin et protagoniste. Benjamin replonge ainsi dans cette période sombre de l'Argentine où l'ambiance était étouffante et les apparences trompeuses.",["Ricardo Darin", "ESoledad Villamil", "Guillermo Francella"])
    ]

    categories = [
        Categorie("Action", "Des films pleins de scènes d’action passionnantes."),
        Categorie("Aventure", "Des films qui vous mènent à des voyages passionnants et des découvertes."),
        Categorie("Romantique", "Films qui vous font réfléchir sur les choses vraiment importantes dans la vie."),
        Categorie("Drame", "Des films qui traversent l’intrigue et la recherche pour découvrir la vérité.")
    ]



    base_de_donnees = {
        "clients": [client.__dict__ for client in clients],
        "acteurs": [acteur.__dict__ for acteur in acteurs],
        "employes": [employe.__dict__ for employe in employes],
        "cartecredits":[cartecredit.__dict__ for cartecredit in cartecredits],
        "films":[film.__dict__ for film in films],
        "categories":[categorie.__dict__ for categorie in categories]

    }

#Garder ma base de donnees

    with open('base_de_donnees.json', 'w') as f:
        json.dump(base_de_donnees, f, indent=4)


def authenticar_employe(code_utilisateur, mot_de_passe):
    with open('base_de_donnees.json', 'r') as f:
        base_de_donnees = json.load(f)
        for employe in base_de_donnees["employes"]:
            if employe['code_utilisateur'] == code_utilisateur and employe['mot_de_passe'] == mot_de_passe:
                return True, employe['type_acces']
    return False, None

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        code_utilisateur=request.form['code_utilisateur']
        mot_de_passe=request.form['mot_de_passe']

        authenticated, type_acces = authenticar_employe(code_utilisateur, mot_de_passe)

        if authenticated:
            if type_acces == "admin":
                return render_template('admin.html', code_utilisateur=code_utilisateur)
            elif type_acces == "lecture":
                return render_template('lecture.html', code_utilisateur=code_utilisateur)
        else:
            return render_template('login.html', error='Votre code utilisateur ou mot de passe sont incorrects')




if __name__ == "__main__":
    garder_base_de_donnees()
    app.run(debug=True)

