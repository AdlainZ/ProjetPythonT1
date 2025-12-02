from classes.User import User
from classes.Admin import Admin
from utils.csv_manager import save_user, charger_users
from utils.Auth import authentifier

def afficher_menu():
    print("===============")
    print("SYSTEME DE GESTION DES UTILISATEURS")
    print("1 - Se connecter")
    print("2 - Créer un utilisateur")
    print("3 - Créer un administrateur")
    print("4 - Afficher tous les utilisateurs")
    print("5 - Rechercher un utilisateur")
    print("6 - Modifier un utilisateur")
    print("7 - Supprimer un utilisateur")
    print("8 - Quitter")
    print("===============")

def main_menu():
    """Boucle du menu principal"""
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == 1:
            print("Connexion en cours...")

        elif choix == 2:
            print("Création en cours...")
        
        elif choix == 3:
            print("Création d'un administrateur en cours...")
        
        elif choix == 4:
            print("Chargement des utilisateurs...")

        elif choix == 5:
            print("Recherche d'un utilisateur...")

        elif choix == 6:
            print("Modification en cours...")

        elif choix == 7:
            print("Suppresion en cours...")
        
        elif choix == 8:
            print("Au revoir !")
            break

        else:
            print("Veillez à entrer un chiffre entre 1 et 8 inclus !")
            