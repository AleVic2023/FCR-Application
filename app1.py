mport data
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required,current_user


app = Flask(__name__)

import json # poour povoir avoi l information enregistre


# creation des classes

class Personne:
    def __init__(self, nom, prenom, sexe):
        self.nom = nom
        self.prenom = prenom
        self.sexe = sexe

# La classe Client herite de la classe Personne
class Client(Personne):
    def __init__(self, nom, prenom, sexe, date_inscription, courriel, mot_de_passe):
        super().__init__(nom, prenom, sexe)
        self.date_inscription = date_inscription
        self.courriel = courriel
        self.mot_de_passe = mot_de_passe

# La classe Acteur herite de la classe Personne
class Acteur(Personne):
    def __init__(self, nom, prenom, sexe, nom_personnage, date_debut_emploi, date_fin_emploi, cachet):
        super().__init__(nom, prenom, sexe)
        self.nom_personnage = nom_personnage
        self.date_debut_emploi = date_debut_emploi
        self.date_fin_emploi = date_fin_emploi
        self.cachet = cachet

# La classe Employe hertie de la classe Personne

class Employe(Personne):
    def __init__(self, nom, prenom, sex, date_embauche, utilisateur, mot_de_passe, type_acces):
        super().__init__(nom, prenom, sex)
        self.date_embauche = date_embauche
        self.utilisateur = utilisateur
        self.mot_de_passe = mot_de_passe
        self.type_acces = type_acces


#Creation des autres classes

class CarteCredit:
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



# Maintenant on doit creer une fonctionne pour garder les donnees json pour apres pouvoir les consulter
def garder_donnees_json(donnees,data):
    with open(data, 'w') as file:
        json.dump(donnees, file, indent=4)


# Creation fichier jason


clients = [
    Client("Achury", "Angelica", "F", "2021-04-24", "aachury@gmail.com", "motdepasse"),
    Client("Langlais", "Alain", "M", "2022-11-25", "alainlanglois15@hotmail.com", "motdepasse1"),
    Client("Pauline", "Bellanda", "F", "2023-01-15", "bpaul@hotmail.com", "motdepasse2"),
    Client("Gagnon", "Benoita", "M", "2024-03-07", "gbenoit@gmail.com", "motdepasse3")
]

acteurs = [
    Acteur("Pitt", "Brad", "M", "Tyler Durden", "1999-01-01", "2000-12-31", 1000000),
    Acteur("Jolie", "Angelina", "F", "Lara Croft", "2001-01-01", "2002-12-31", 1500000)
]


employes = [

    Employe("Calixto","Victor","M","2019-09-06","vaco198","password","lecture"),
    Employe("Rodriguez","Carol","F","2021-02-07","carola87","password1","admin")

]


cartescredit = [

    CarteCredit(45130256987,"2025-05-31",523),
    CarteCredit(19425683216,"2027-01-31",712),
    CarteCredit(45192412061,"2024-09-31",972),
    CarteCredit(28091407194,"2026-07-31",824)
]


films = [
    Film("Fight Club", 139, "Un employé de bureau insomniaque et un fabricant de savons diaboliques forment un club de lutte clandestin qui évolue beaucoup.", ["Brad Pitt","Edward Norton","Helena Bonhamt"]),
    Film("Lara Croft: Tomb Raider", 100, "L’aventurière des jeux vidéo Lara Croft prend vie dans un film où elle court contre le temps et les méchants pour récupérer de puissants artefacts anciens", ["Angelina Jolie","Alicia Vikander","Daniel Craig"]),
    Film("Sous la même étoile", 120, "Depuis son enfance, Hazel a des problèmes respiratoires, l'obligeant à porter un tube à oxygène en permanence. Sur les conseils de sa mère, elle participe à un groupe de soutien, où elle fait la connaissance d'Augustus, qui a perdu une jambe à cause d'un cancer..", ["Shailene Woodley","Ansel Elgort","Nat Wolff"]),
    Film("Le secret de ses yeux", 153,"Buenos Aires. Benjamin Esposito enquête sur le meurtre violent d'une jeune femme. Vingt-cinq ans plus tard, il décide d'écrire un roman basé sur cette affaire classée dont il a été témoin et protagoniste. Benjamin replonge ainsi dans cette période sombre de l'Argentine où l'ambiance était étouffante et les apparences trompeuses.",["Ricardo Darin", "ESoledad Villamil", "Guillermo Francella"])
]

categories = [
    Categorie("Action", "Des films pleins de scènes d’action passionnantes."),
    Categorie("Aventure", "Des films qui vous mènent à des voyages passionnants et des découvertes."),
    Categorie("Romantique", "Films qui vous font réfléchir sur les choses vraiment importantes dans la vie."),
    Categorie("Drame", "Des films qui traversent l’intrigue et la recherche pour découvrir la vérité.")
]

# On va lier les donnees dans juste un seul dictionaire

donnees = {
    "clients":[client.__dict__ for client in clients],
    "acteurs":[acteur.__dict__ for acteur in acteurs],
    "employes":[employe.__dict__ for employe in employes],
    "cartescredit":[cartecredit.__dict__ for cartecredit in cartescredit],
    "films": [film.__dict__ for film in films],
    "categories":[categorie.__dict__ for categorie in categories]
}

# Je vais garder les donnees dans mon fichier json
garder_donnees_json(donnees,"data.json")


#Apres avoior les donnees dont jai besoin, maintenant je vais faire authentification pour les employes lesquels onnt acces comment admin et juste lecture

# la premiere chose est d





if __name__ == '__main__':
    app.run(debug=True)


