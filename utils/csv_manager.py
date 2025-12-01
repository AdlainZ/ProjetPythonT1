import csv
import os # Interaction avec le système d'exploitation. Il permet de vérifier le fichier avec os.path, et de créer un dossier avec makedirs

FICHIER_USERS = "data/users.csv"

def init_fichiers():
    """Initialise le fichier en CSV, et si le fichier n'existe pas, il le créé"""
    if not os.path.exists("data"):
        print("Création du dossier data")
        os.makedirs("data")
    else:
        print("Le dossier existe déjà")

    print(f"Verification de l'existance du fichier {FICHIER_USERS}")
    if not os.path.exists(FICHIER_USERS):
        print("Création du fichier users.csv")
        with open(FICHIER_USERS, 'w', newline='', encoding='utf-8') as fichier:
            writer = csv.writer(fichier)
            writer.writerow(['nom', 'prenom', 'login', 'password', 'type', 'niveau_droits']) # '' et "" agissent pareil, c'est pour être clair dans le code
        print(f"Fichier {FICHIER_USERS} créé")
    else:
        print("Le fichier existe déjà")

def save_user(user, type_user):
    """Save le user dans le fichier csv"""

    init_fichiers()

    with open(FICHIER_USERS, 'a', newline='', encoding='utf-8') as fichier: # a c'est pour ajouter, alors que w c'est pour supprimé et réécrire
        writer = csv.writer(fichier)
        if type_user == "admin":
            niveau = user.niveau_droits
        else:
            niveau = 0
        writer.writerow([user.nom, user.prenom, user.login, user.password, type_user, niveau])

    print(f"Le compte {type_user.capitalize()} {user.login} est sauvegardé")

def charger_users():
    """Charge et ajoute tous les users du fichier csv"""
    init_fichiers()
    users = []
    with open(FICHIER_USERS, 'r', encoding='utf-8') as fichier: # r pour la lecture
        reader = csv.DictReader(fichier)
        for i in reader: # pour chaque ligne
            users.append(i) # append = ajouter
    return users

