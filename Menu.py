from classes.User import User
from classes.Admin import Admin
from utils.csv_manager import save_user, charger_users
from utils.Auth import authentifier

utilisateur_connecte = None

def verification_connexion():
    """On verifie si un admin est co"""
    if utilisateur_connecte is None:
        print("Accès refusé !")
        print("Vous devez être connecté avec un compte administrateur pour accéder à cette interface.")
        input("Appuyez sur Entrée pour continuer........")
        return False
    return True

def afficher_menu():
    print("-------------------------")
    print("SYSTEME DE GESTION DES UTILISATEURS")

    if utilisateur_connecte is not None:
        print(f"Connecté : {utilisateur_connecte['prenom']} {utilisateur_connecte['nom']} {utilisateur_connecte['region']}.")
    else:
        print("Non connecté.")

    print("1 - Se connecter")
    print("2 - Créer un utilisateur")
    print("3 - Créer un administrateur")
    print("4 - Afficher tous les utilisateurs")
    print("5 - Rechercher un utilisateur")
    print("6 - Modifier un utilisateur")
    print("7 - Supprimer un utilisateur")
    print("8 - Se déconnecter")
    print("9 - Quitter (proprement sans ctrl+C)")
    print("--------------------------------------------------------------------")

def main_menu():
    """Boucle du menu principal"""
    while True:
        afficher_menu()
        choix = input("Votre choix : ")

        if choix == "1":
            global utilisateur_connecte

            print("Connexion en cours...")
            login = input("Login : ")
            mot_de_passe = input("Mot de passe : ")

            resultat = authentifier(login, mot_de_passe)

            if resultat is not None:
                if resultat['type'] == 'admin':
                    utilisateur_connecte = resultat
                    print(f"Connexion réussie !")
                    print(f"Bienvenue {resultat['prenom']} {resultat['nom']}")
                    print(f"Type de compte : {resultat['type']}")
                    print(f"Niveau de droits : {resultat['niveau_droits']}")
                    print(f"Region : {resultat['region']}")

                else:
                    print("Echec de connexion !")
                    print("Seuls les administrateurs peuvent se connecter !")

                input("Appuyez sur Entrée pour continuer...........")    

        elif choix == "2":
            if not verification_connexion():
                break

            print("Création d'un utilisateur en cours...")
            nom = input("Nom : ")
            prenom = input("Prénom : ")

            if utilisateur_connecte['niveau_droits'] == "1":
                region = utilisateur_connecte['region']
                print(f"Région : {region} ( votre région )")
            else:
                print("Choix parmi les régions suivantes :")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Choisissez la région ( 1, 2 ou 3)")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Region invalide ! Region par défaut : Marseille.")
                    region = "Marseille"

            new_user = User(nom, prenom, region)
            save_user(new_user, "user")

            print(f"L'utilisateur {new_user.login} a été créé avec succès dans la région {region}")
            input("Appuyez sur Entrée pour continuer.......")
        
        elif choix == "3":
            if not verification_connexion():
                break

            print("Création d'un administrateur en cours...")

            if utilisateur_connecte['niveau_droits'] == "1":
                print("Accès refusé. Seul un SUPERADMIN peut faire cela.")
                input("Appuyez sur Entrée pour continuer.....")
                break

            nom = input("Nom : ")
            prenom = input("Prénom : ")
            print("Choix parmi les régions suivantes :")
            print("1 - Marseille")
            print("2 - Rennes")
            print("3 - Grenoble")
            choix_region = input("Choisissez la région ( 1, 2 ou 3)")
            if choix_region == "1":
                region = "Marseille"
            elif choix_region == "2":
                region = "Rennes"
            elif choix_region == "3":
                region = "Grenoble"
            else:
                print("Region invalide !")
                input("Appuyez sur Entrée pour continuer....")
                break

            print("Niveau de droits :")
            print("1 - Administrateur ( Il peut gérer les utilisateurs de sa région )")
            print("2 - SuperAdministrateur ( BIGBOSS )")
            niveau = input("Choisissez le niveau ( 1 ou 2 ) : ")

            if niveau == "1":
                niveau_droits = 1
            elif niveau == "2":
                niveau_droits = 2
            else:
                print("Niveau invalide. Droits User appliqués")
                niveau_droits = 0 #Droits par défaut quand il y a eu une erreur

            nouvel_admin = Admin(nom, prenom, region, niveau_droits)

            save_user(nouvel_admin, "admin")
            print(f"Administrateur {nouvel_admin.login} créé avec succès")
            print(f"Region : {region}")
            print(f"Niveau de droits : {nouvel_admin.niveau_droits}")
            input("Appuyez sur Entrée pour continuer...........")
        
        elif choix == "4":
            if not verification_connexion():
                break
            
            print("Chargement des utilisateurs...")

            utilisateurs = charger_users()

            if utilisateur_connecte['niveau_droits'] == "1":
                utilisateurs_filtres = []
                for user_filtre in utilisateurs:
                    if user_filtre['region'] == utilisateur_connecte['region']:
                        utilisateurs_filtres.append(user_filtre)
                        print(f"Région : {utilisateur_connecte['region']}")
            else:
                utilisateurs_filtres = utilisateurs
                print("Toutes les régions pour vous Monsieur/Madame le superadmin BIGBOSS")

            if len(utilisateurs_filtres) == 0:
                print("Aucun utilisateur enregistré")
            else:
                print(f"Nombre total : {len(utilisateurs_filtres)} utilisateurs dans le fichier.")
                print(f"{'type':<12} / {'nom':<15} / {'prenom':<15} / {'login':<20} / {'niveau':<8} / {'region':<10}") # Permet juste d'aligner correctement vers la gauche de x caractères
                print("--------------------------------------------------------------------------------------------------------------------")

                for user in utilisateurs_filtres:
                    print(f"{user['type']:<12} / {user['nom']:<15} / {user['prenom']:<15} / {user['login']:<20} / {user['niveau_droits']:<8} / {user['region']:<10}")

            input("Appuyez sur Entrée pour continuer......")
        elif choix == "5":
            if not verification_connexion():
                break
            print("Recherche d'un utilisateur...")


        elif choix == "6":
            if not verification_connexion():
                break
            print("Modification en cours...")

        elif choix == "7":
            if not verification_connexion():
                break
            print("Suppresion en cours...")
        
        elif choix == "8":
            if utilisateur_connecte is not None:
                print("Au revoir !")
                utilisateur_connecte = None
            else :
                print("Vous n'êtes pas connecté")
            input("Appuyez sur Entrée pour continuer..........")
        
        elif choix == "9":
            print("Au revoir !")
            break

        else:
            print("Veillez à entrer un chiffre entre 1 et 9 inclus !")