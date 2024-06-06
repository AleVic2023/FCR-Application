import unittest
from app1 import app, authenticate_employe, obtenir_client, obtenir_donnees
import json
import os


class TestCase(unittest.TestCase):

    # Création de fichier JSON temporel pour les essais
    @classmethod
    def setUpClass(cls):
        cls.test_db_path = 'data/base_de_donnees_test.json'
        os.makedirs(os.path.dirname(cls.test_db_path), exist_ok=True)

        # Données d'essais des employés
        donnees = {
            "clients": [
                {"id": 1, "nom": "Garibello", "prenom": "Lina", "courriel": "linagaribello@hotmail.com", "mot_de_passe": "motdepasse4"},
                {"id": 2, "nom": "Landry", "prenom": "Sonia", "courriel": "slandryr@gmail.com", "mot_de_passe": "motdepasse5"}
            ],
            "acteurs": [],
            "employes": [
                {
                    "nom": "Calixto",
                    "prenom": "Victor",
                    "sexe": "M",
                    "date_embacuhe": "2019-09-06",
                    "code_utilisateur": "vaco1985",
                    "mot_de_passe": "cle123",
                    "type_acces": "admin"
                },
                {
                    "nom": "Rodriguez",
                    "prenom": "Carol",
                    "sexe": "F",
                    "date_embacuhe": "2021-02-07",
                    "code_utilisateur": "carola87",
                    "mot_de_passe": "cle456",
                    "type_acces": "lecture"
                }
            ],
            "cartecredits": [],
            "films": [],
            "categories": []
        }

        # Garder données de test dans le fichier JSON
        with open(cls.test_db_path, 'w') as f:
            json.dump(donnees, f, indent=4)

        # Remplacer la route du fichier  JSON dnas les fonctions du module app1
        app.route_fichier = cls.test_db_path

    # Supprimer le fichier JSON temporel après des essais
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_db_path)

    # Configuration du client d'essai
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Essai pour la page principale
    def test_index(self):
        result = self.app.get('/')
        self.assertEqual(result.status_code, 200)

    # Essai de la route du login avec des credentiales valides et no validés
    def test_login(self):
        response = self.app.post('/login', data=dict(
            code_utilisateur='vaco1985',
            mot_de_passe='cle123'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'admin', response.data)

        response = self.app.post('/login', data=dict(
            code_utilisateur='invalid',
            mot_de_passe='invalid'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Votre code utilisateur ou mot de passe sont incorrects', response.data)

    # Essai de credentiales valides pour un employé avec accés admin
    def test_authenticate_employe(self):
        is_authenticated, type_acces = authenticate_employe('vaco1985', 'cle123')
        self.assertTrue(is_authenticated)
        self.assertEqual(type_acces, 'admin')

        # Essai de credentiales valides pour un employé avec accés lecture
        is_authenticated, type_acces = authenticate_employe('carola87', 'cle456')
        self.assertTrue(is_authenticated)
        self.assertEqual(type_acces, 'lecture')

        # Essai de credentiales invalidés
        is_authenticated, type_acces = authenticate_employe('invalid_user', 'invalid_password')
        self.assertFalse(is_authenticated)
        self.assertIsNone(type_acces)

        # Essai de mot de passe incorrect
        is_authenticated, type_acces = authenticate_employe('vaco1985', 'wrong_password')
        self.assertFalse(is_authenticated)
        self.assertIsNone(type_acces)

if __name__ == '__main__':
    unittest.main()


