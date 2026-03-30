from classes.User import User
from classes.Admin import Admin
from utils.csv_manager import save_user, charger_users, FICHIER_USERS, init_fichiers
from utils.Auth import authentifier
from utils.file_manager import init_dossiers_regions, obtenir_chemin_region, naviguer_arbo, creer_element, modifier_fichier, copier_element, deplacer_element, supprimer_element
import os
import csv
import shutil

utilisateur_connecte = None

def verification_connexion():
    """On verifie si un user/admin/SUPERADMIN est co"""
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
    print("10 - Naviguer dans l'arborescence des fichiers")
    print("11 - Créer un répertoire / fichier")
    print("12 - Modifier un fichier")
    print("13 - Copier un element")
    print("14 - Déplacer un élément")
    print("--------------------------------------------------------------------")

def main_menu():
    """Boucle du menu principal"""
    print("Initialisation des dossiers des régions...")
    init_dossiers_regions()
    print(".........")

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

            login_recherche = input("Entrez le login à chercher : ")

            utilisateurs = charger_users()

            if utilisateur_connecte['niveau_droits'] == "1":
                utilisateurs_filtres = []
                for user_filtre in utilisateurs:
                    if user_filtre['region'] == utilisateur_connecte['region']:
                        utilisateurs_filtres.append(user_filtre)
            else:
                utilisateurs_filtres = utilisateurs

            utilisateur_trouve = None   # Initié utilisateur_trouve à rien pour le remplir si l'utilisateur est trouvé 
            for user_filtre in utilisateurs_filtres:
                if user_filtre['login'] == login_recherche:
                    utilisateur_trouve = user_filtre
                    break

            if utilisateur_trouve is not None:
                print("Utilisateur trouvé !")
                print(f"Nom : {utilisateur_trouve['nom']}")
                print(f"Prénom : {utilisateur_trouve['prenom']}")
                print(f"Login : {utilisateur_trouve['login']}")
                print(f"Type : {utilisateur_trouve['type']}")
                print(f"Niveau de droits : {utilisateur_trouve['niveau_droits']}")
                print(f"Région : {utilisateur_trouve['region']}")
            else:
                print(f"L'utilisateur {login_recherche} est introuvable")
                if utilisateur_connecte['niveau_droits'] == "1":
                    print(f"Recherche limité à la région {utilisateur_connecte['region']}")
            
            input("Appuyez sur Entrée pour continuer....")

        elif choix == "6":
            if not verification_connexion():
                break
            print("Modification en cours...")

            login_modification = input("Entrez le login de l'utilisateur à modifier : ")

            utilisateurs = charger_users()

            utilisateur_trouve = None
            index_user = -213

            for compteur, user_filtre in enumerate(utilisateurs):
                if user_filtre['login'] == login_modification:
                    if utilisateur_connecte['niveau_droits'] == "1":
                        if user_filtre['region'] != utilisateur_connecte['region']: #REFUS D'ACCES SI PAS BONNE REGION
                            print(f"Accès refusé ! L'utilisateur est dans la region {user_filtre['region']}, mauvaise région ! Sinon connectez vous en SUPERADMIN !")
                            input("Appuyez sur Entrée pour continuer.....")
                            break
                        if user_filtre['type'] == 'admin': #REFUS D'ACCES SI PAS SUPERADMIN S'IL VEUT MODIFIER UN ADMIN
                            print("Accès refusé ! Connectez vous en SUPERADMIN pour modifier un admin !")
                            input("Appuyez sur Entrée pour continuer....")
                            break
                    utilisateur_trouve = user_filtre
                    index_user = compteur
                    break

            if utilisateur_trouve is not None:
                print(f"Utilisateur trouvé : {utilisateur_trouve['prenom']}, {utilisateur_trouve['nom']}")
                print("Que voulez-vous modifier ? 1 = Nom, 2 = Prénom, 3 = Région et 4 = Annuler")

                choix_modification = input("Votre choix : ")

                if choix_modification == "1":
                    nouveau_nom = input("Nouveau nom : ")
                    utilisateurs[index_user]['nom'] = nouveau_nom
                    print(f"Nom modifié : {nouveau_nom}")
                elif choix_modification == "2":
                    nouveau_prenom = input("Nouveau prénom : ")
                    utilisateurs[index_user]['prenom'] = nouveau_prenom
                    print(f"Prénom modifié : {nouveau_prenom}")
                elif choix_modification == "3":
                    if utilisateur_connecte['niveau_droits'] == "1":
                        print("Seul un SUPERADMIN peut toucher à ça !")
                    else:
                        print("Région disponible : 1 - Marseille / 2 - Rennes / 3 - Grenoble")
                        choix_region = input("1, 2 ou 3 : ")

                        if choix_region =="1":
                            utilisateurs[index_user]['region'] = "Marseille"
                        elif choix_region == "2":
                            utilisateurs[index_user]['region'] = "Rennes"
                        elif choix_region == "3":
                            utilisateurs[index_user]['region'] = "Grenoble"
                        else:
                            print("Région indisponible !")
                            input("Appuyez sur Entrée pour continuer......")
                            break

                        print(f"Région modifiée : {utilisateurs[index_user]['region']}")
                elif choix_modification == "4":
                    print("Modification annulée !")
                    input("Appuyez sur Entrée pour continuer ......")
                    break

                if choix_modification in ["1", "2", "3"]:
                    os.remove(FICHIER_USERS)

                    init_fichiers()

                    with open(FICHIER_USERS, 'a', newline='', encoding='utf-8') as fichier:
                        writer = csv.writer(fichier)
                        for user in utilisateurs:
                            writer.writerow([user['nom'],user['prenom'],user['login'],user['password'],user['type'],user['niveau_droits'], user['region']])
                    
                    print("Modifications sauvegardées !")

                elif utilisateur_trouve is None and index_user == -213:
                    print("Utilisateur introuvable !")

                input("Appuyez sur Entrée pour continuer......")

        elif choix == "7":
            if not verification_connexion():
                break
            print("Suppresion en cours...")

            login_suppression = input("Entrez le login de l'utilisateur à supprimer : ")

            utilisateurs = charger_users()

            utilisateur_trouve = None
            index_user = -213

            for compteur, user_filtre in enumerate(utilisateurs):
                if user_filtre['login'] == login_suppression:
                    if utilisateur_connecte['niveau_droits'] == "1":
                        if user_filtre['region'] != utilisateur_connecte['region']:
                            print(f"Accès refusé ! L'utilisateur est dans la region {user_filtre['region']}, mauvaise région ! Sinon connectez vous en SUPERADMIN !")
                            input("Appuyez sur Entrée pour continuer.....")
                            break
                        if user_filtre['type'] == 'admin':
                            print("Accès refusé ! Connectez vous en SUPERADMIN pour supprimer un admin !")
                            input("Appuyez sur Entrée pour continuer....")
                            break
                    utilisateur_trouve = user_filtre
                    index_user = compteur

            if utilisateur_trouve is not None:
                print(f"Vous allez supprimer : {utilisateur_trouve['nom']} avec le login {utilisateur_trouve['login']} qui est un {utilisateur_trouve['type']}")

                confirmation = input(f"Sûr de vouloir supprimer {utilisateur_trouve['login']} ? ")
                confirmation2 = input(f" Il a une famille... Il a un prénom aussi... Son prénom est {utilisateur_trouve['prenom']}... ")
                confirmation3 = input("C'est la faute à qui ?")
                confirmation4 = input(f"Bon bah si Madame OULMI veut le supprimer.... (Réponds par oui / non) ")

                if confirmation4.lower() == "oui":
                    utilisateurs.pop(index_user) # pop = supprimer

                    os.remove(FICHIER_USERS)

                    init_fichiers()

                    with open(FICHIER_USERS, 'a', newline='', encoding='utf-8') as fichier:
                        writer = csv.writer(fichier)
                        for user in utilisateurs:
                            writer.writerow([user['nom'],user['prenom'],user['login'],user['password'],user['type'],user['niveau_droits'], user['region']])
                    
                    print(f"Modifications sauvegardées ! Utilisateur {login_suppression} supprimé. Vous êtes cruelle...")

            elif utilisateur_trouve is None and index_user == -213:
                    print("Utilisateur introuvable !")
            input("Appuyez sur Entrée pour continuer......")

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

        elif choix == "10":
            if not verification_connexion():
                continue

            print("Navigation dans l'arborescence...")

            if utilisateur_connecte['niveau_droits'] == "1":
                chemin = obtenir_chemin_region(utilisateur_connecte['region'])
                print(f"Arborescence de la région ({utilisateur_connecte['region']}) :")
                print()
                naviguer_arbo(chemin)
            else:
                print("Choisissez la région à explorer :")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Votre choix (1, 2 ou 3) : ")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Choix invalide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue

                chemin = obtenir_chemin_region(region)
                print(f"Arborescence de la région {region} :")
                naviguer_arbo(chemin)

        elif choix == "11":
            if not verification_connexion():
                continue
            print("Création d'un répertoire ou d'un fichier...")

            if utilisateur_connecte['niveau_droits'] == "1":
                chemin = obtenir_chemin_region(utilisateur_connecte['region'])
                print(f"Création dans votre région ({utilisateur_connecte['region']}).")
                creer_element(chemin)
            else:
                print("Dans quelle région voulez-vous créer ?")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Votre choix 1, 2 ou 3 : ")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Choix invalide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue

                chemin = obtenir_chemin_region(region)
                print(f"Création dans la région de {region}.")
                creer_element(chemin)

            input("Appuyez sur Entrée pour continuer...")         

        elif choix == "12":
            if not verification_connexion():
                continue
            print("Modification d'un fichier...")

            if utilisateur_connecte['niveau_droits'] == "1":
                chemin = obtenir_chemin_region(utilisateur_connecte['region'])
                print(f"Modification dans votre région ({utilisateur_connecte['region']}).")
                modifier_fichier(chemin)
            else:
                print("Dans quelle région voulez-vous créer ?")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Votre choix 1, 2 ou 3 : ")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Choix invalide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue

                chemin = obtenir_chemin_region(region)
                print(f"Modification dans la région de {region}.")
                modifier_fichier(chemin)

            input("Appuyez sur Entrée pour continuer...") 
        
        elif choix == "13":
            if not verification_connexion():
                continue
            print("Copie d'un élément...")

            if utilisateur_connecte['niveau_droits'] == "1":
                chemin = obtenir_chemin_region(utilisateur_connecte['region'])
                print(f"Copie dans votre région ({utilisateur_connecte['region']}).")
                copier_element(chemin)
            else:
                print("Dans quelle région voulez-vous copier ?")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Votre choix 1, 2 ou 3 : ")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Choix invalide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue

                chemin = obtenir_chemin_region(region)
                print(f"Modification dans la région de {region}.")
                copier_element(chemin)

            input("Appuyez sur Entrée pour continuer...")

        elif choix == "14":
            if not verification_connexion():
                continue
            print("Déplacement d'un élément...")

            if utilisateur_connecte['niveau_droits'] == "1":
                chemin = obtenir_chemin_region(utilisateur_connecte['region'])
                print(f"Déplacement dans votre région ({utilisateur_connecte['region']}).")
                deplacer_element(chemin)
            else:
                print("Dans quelle région voulez-vous déplacer ?")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Votre choix 1, 2 ou 3 : ")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Choix invalide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue

                chemin = obtenir_chemin_region(region)
                print(f"Déplacement dans la région de {region}.")
                deplacer_element(chemin)

            input("Appuyez sur Entrée pour continuer...")

        elif choix == "15":
            if not verification_connexion():
                continue
            print("Suppression d'un élément...")

            if utilisateur_connecte['niveau_droits'] == "1":
                chemin = obtenir_chemin_region(utilisateur_connecte['region'])
                print(f"Suppression dans votre région ({utilisateur_connecte['region']}).")
                supprimer_element(chemin)
            else:
                print("Dans quelle région voulez-vous déplacer ?")
                print("1 - Marseille")
                print("2 - Rennes")
                print("3 - Grenoble")
                choix_region = input("Votre choix 1, 2 ou 3 : ")

                if choix_region == "1":
                    region = "Marseille"
                elif choix_region == "2":
                    region = "Rennes"
                elif choix_region == "3":
                    region = "Grenoble"
                else:
                    print("Choix invalide !")
                    input("Appuyez sur Entrée pour continuer...")
                    continue

                chemin = obtenir_chemin_region(region)
                print(f"Suppression dans la région de {region}.")
                supprimer_element(chemin)

            input("Appuyez sur Entrée pour continuer...")



        else:
            print("Veillez à entrer un chiffre entre 1 et 10 inclus !")