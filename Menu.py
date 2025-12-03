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

        if choix == "1":
            print("Connexion en cours...")
            login = input("Login : ")
            mot_de_passe = input("Mot de passe : ")

            resultat = authentifier(login, mot_de_passe)

            if resultat is not None:
                print(f"Connexion réussie !")
                print(f"Bienvenue {resultat['prenom']} {resultat['nom']}")
                print(f"Type de compte : {resultat['type']}")
                print(f"Niveau de droits : {resultat['niveau_droits']}")

            else:
                print("Echec de connexion !")
                print("Login ou mot de passe incorrect")

            input("Appuyez sur Entrée pour continuer...........")    

        elif choix == "2":
            print("Création d'un utilisateur en cours...")
            nom = input("Nom : ")
            prenom = input("Prénom : ")

            new_user = User(nom, prenom)
            save_user(new_user, "user")

            print(f"L'utilisateur {new_user.login} a été créé avec succès")
            input("Appuyez sur Entrée pour continuer.......")
        
        elif choix == "3":
            print("Création d'un administrateur en cours...")
            nom = input("Nom : ")
            prenom = input("Prénom : ")

            print("Niveau de droits :")
            print("1 - Administrateur ( Il peut gérer les utilisateurs )")
            print("2 - SuperAdministrateur ( Il peut gérer les utilisateurs et les administrateurs )")
            niveau = input("Choisissez le niveau ( 1 ou 2 ) : ")

            if niveau == "1":
                niveau_droits = 1
            elif niveau == "2":
                niveau_droits = 2
            else:
                print("Niveau invalide. Droits User appliqués")
                niveau_droits = 0 #Droits par défaut quand il y a eu une erreur

            nouvel_admin = Admin(nom, prenom, niveau_droits) # Rappel : Un superadmin est un admin avec + de droits

            save_user(nouvel_admin, "admin")
            print(f"Administrateur {nouvel_admin.login} créé avec succès")
            print(f"Niveau de droits : {nouvel_admin.niveau_droits}")
            input("Appuyez sur Entrée pour continuer...........")
        
        elif choix == "4":
            print("Chargement des utilisateurs...")

            utilisateurs = charger_users()

            if len(utilisateurs) == 0:
                print("Aucun utilisateur enregistré")
            else:
                print(f"Nombre total : {len(utilisateurs)} utilisateurs dans le fichier.")
                print(f"{'type':<12} / {'nom':<15} / {'prenom':<15} / {'login':<20} / {'niveau':<8}") # Permet juste d'aligner correctement vers la gauche de x caractères
                print("--------------------------------------------------------------------------------------------------------------------")

                for user in utilisateurs:
                    print(f"{user['type']:<12} / {user['nom']:<15} / {user['prenom']:<15} / {user['login']:<20} / {user['niveau_droits']:<8}")

            input("Appuyez sur Entrée pour continuer......")
        elif choix == "5":
            print("Recherche d'un utilisateur...")


        elif choix == "6":
            print("Modification en cours...")

        elif choix == "7":
            print("Suppresion en cours...")
        
        elif choix == "8":
            print("Au revoir !")
            break

        else:
            print("Veillez à entrer un chiffre entre 1 et 8 inclus !")

