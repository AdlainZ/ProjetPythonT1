import os
import shutil

def init_dossiers_regions():
    """Initialise les dossiers des régions et le serveur FTP si ça n'existe pas"""

    regions = ["marseille", "rennes", "grenoble"]

    for region in regions:
        nom_dossier = f"fichiers_{region}"
        if not os.path.exists(nom_dossier):
            os.mkdir(nom_dossier)
            print(f"Dossier {nom_dossier} créé")
        else:
            print(f"Dossier {nom_dossier} existe déjà.")

    serveurftp = "serveur_ftp_paris"

    if not os.path.exists(serveurftp):
        os.mkdir(serveurftp)
        print(f"Dossier du serveur FRP créé avec succès : {serveurftp}")
    else:
        print(f"Dossier {serveurftp} existe déjà soit concentré...")

    regions = ["marseille", "rennes", "grenoble"]

    for region in regions:
        path_region = os.path.join(serveurftp, region)

        if not os.path.exists(path_region):
            os.mkdir(path_region)
            print(f"Dossier de la région FTP bien créé : {path_region}")
        else:
            print(f"Soit concentré... C'est déjà créé ! {path_region}")

def obtenir_chemin_region(region):
    """Retourne le chemin du dossier correspondant à la région donnée"""
    region_lower = region.lower()

    chemin = f"fichiers_{region_lower}/"

    return chemin

def naviguer_arbo(chemin, niveau=0):
    """Afficher les dossiers et fichiers appartenant à une région"""

    if not os.path.exists(chemin):
        print(f"Erreur : Le chemin {chemin} n'existe pas.")
        return
    
    indentation = "  " * niveau

    try:
        elements = os.listdir(chemin)

        if len(elements) == 0:
            print(f"{indentation}(Dossier vide)")
            return
        
        for element in elements:
            chemin_complet = os.path.join(chemin, element)

            if os.path.isdir(chemin_complet):
                print(f"{indentation}Dossier :{element}/")
                naviguer_arbo(chemin_complet, niveau + 1)
            else:
                print(f"{indentation}Fichier :{element}")

    except PermissionError:
        print(f"{indentation} Accès refusé !")


def creer_element(chemin_base):
    """Créer un dossier ou un fichier dans le chemin spécifié"""

    print("Créer un dossier ( 1 ) ou un fichier ( 2 ) ?")
    choix = input("Votre choix ( 1 ou 2 ) : ")

    if choix == "1":
        print("Vous pouvez utiliser des chemins")
        nom_dossier = input("Nom du dossier ou du chemin : ")

        chemin_complet = os.path.join(chemin_base, nom_dossier)

        if os.path.exists(chemin_complet):
            print(f"Erreur : Le dossier '{nom_dossier} existe déjà!")
            return
        
        os.makedirs(chemin_complet)
        print(f"Dissier créé ! {chemin_complet}")
    elif choix == "2":
        print("Vous pouvez utiliser des chemins")
        nom_fichier = input("Nom du fichier avec ou sans chemin : ")

        chemin_complet = os.path.join(chemin_base, nom_fichier)

        if os.path.exists(chemin_complet):
            print(f"Erreur, le fichier '{nom_fichier} existe déjà !")
            return
        
        dossier_parent = os.path.dirname(chemin_complet)
        if not os.path.exists(dossier_parent):
            print(f"Erreur : Le dossier '{dossier_parent}' n'existe pas !")
            print("Il faut créer le dossier d'abord, ou utiliser un chemin existant.")
            return
        
        print("Contenu du fichier (Entrée pour un fichier vide) : ")
        contenu = input()

        with open(chemin_complet, 'w', encoding='utf-8') as fichier:
            fichier.write(contenu)

            print(f"Fichier créé ! {chemin_complet}")
        
    else:
        print("Choix invalide !")


def modifier_fichier(chemin_base):
    """Modifie le contenu d'un fichier existant"""

    print("Nom du fichier à modifier ( avec le chemin si besoin )")
    nom_fichier = input()

    chemin_complet = os.path.join(chemin_base, nom_fichier)

    if not os.path.exists(chemin_complet):
        print(f"Erreur : Le fichier '{nom_fichier} n'existe pas !")
        return
    
    if not os.path.isfile(chemin_complet):
        print(f"Erreur : '{nom_fichier} est un dossier, pas un fichier !")
        return
    
    print("\nContenu du fichier : ")
    try:
        with open(chemin_complet, 'r', encoding='utf-8') as fichier:
            contenu_actuel = fichier.read()
            if contenu_actuel:
                print(contenu_actuel)
            else:
                print("(Fichier vide)")
    
    except Exception as e:
        print(f"Erreur lors de la lecture : {e}")
        return
    print("Fin du contenu\n")

    print("Comment voulez-vous modifier le fichier ? 1 pour remplacer le contenu et 2 pour ajouter du contenu à la fin")
    choix = input("Votre choix, 1 ou 2 : ")
    
    if choix == "1":
        print("Nouveau contenu du fichier :")
        nouveau_contenu = input()

        with open(chemin_complet, 'w', encoding='utf-8') as fichier:
            fichier.write(nouveau_contenu)

            print(f"Fichier modifié ( tout le contenu a été remplacé !) : {chemin_complet}")
    
    elif choix == "2":
        print("Contenu à ajouter à la fin du fichier :")
        contenu_ajouter = input()

        with open(chemin_complet, 'a', encoding='utf-8') as fichier:
            fichier.write("\n") # Saut de ligne sinon pas beau
            fichier.write(contenu_ajouter)
        
        print(f"Fichier modifié (Contenu ajouté !): {chemin_complet}")

    else:
        print("Choix invalide on t'a dis !")

def copier_element(chemin_base):
    """Copie un fichier ou un dossier et son contenu"""

    print("Nom de l'élement à copier ( chemin possible oui oui)")
    nom_source = input()

    chemin_source = os.path.join(chemin_base, nom_source)

    if not os.path.exists(chemin_source):
        print(f"Erreur : '{nom_source}' n'existe pas !")
        return

    print("Nom de la destination (avec chemin si besoin)")
    nom_destination = input()

    chemin_destination = os.path.join(chemin_base, nom_destination)

    if os.path.exists(chemin_destination):
        print(f"Erreur : {nom_destination} existe déjà !")
        return
    
    try:
        if os.path.isfile(chemin_source):
            shutil.copy(chemin_source, chemin_destination)
            print(f"Fichier copié : {chemin_source} vers {chemin_destination}")

        elif os.path.isdir(chemin_source):
            shutil.copytree(chemin_source, chemin_destination)
            print(f"Dossier copié : {chemin_source} vers {chemin_destination}")
    
    except Exception as e:
        print(f"Erreur lors de la copie : {e}")

def deplacer_element(chemin_base):
    """Déplacer un fichier ou un dossier"""

    print("Nom de l'élément à déplacer : ")
    nom_source = input()

    chemin_source = os.path.join(chemin_base, nom_source)

    if not os.path.exists(chemin_source):
        print(f"Erreur : '{nom_source}' n'existe pas !")
        return
    
    print("Nom de la destination : ")
    nom_destination = input()

    chemin_destination = os.path.join(chemin_base, nom_destination)

    if os.path.exists(chemin_destination):
        print(f"Erreur '{nom_destination}' existe déjà !")
        return
    
    dossier_parent = os.path.dirname(chemin_destination)
    if dossier_parent and not os.path.exists(dossier_parent):
        print(f"Erreur : Le dossier parent '{dossier_parent}' n'existe pas")
        print("Créer d'abord le dossier de destination")
        return
    
    try:
        shutil.move(chemin_source, chemin_destination)
        print(f"Element deplacé !")
    
    except Exception as e:
        print(f"Erreur lors du déplacement : {e}")

def supprimer_element(chemin_base):
    """Supprime un fichier ou un dossier"""

    print("ATTENTION, supprimé c'est supprimé reprendre c'est pas possible !")
    print("Nom de l'élément à supprimer : ")
    nom_element = input()

    chemin_complet = os.path.join(chemin_base, nom_element)
    
    if not os.path.exists(chemin_complet):
        print(f"Erreur : '{nom_element}' n'existe pas !")
        return
    
    if os.path.isfile(chemin_complet):
        print(f"Fichier à supprimer : {chemin_complet}")
    elif os.path.isdir(chemin_complet):
        print(f"Dossier à supprimer : {chemin_complet}")
    
    confirmation1 = input("Êtes-vous sûr de supprimer ??? Tapez oui.")
    if confirmation1.lower() != "oui":
        print("Suppression annulée. Il fallait mettre oui. Ou OuI, ou OUI.")
        return
    
    try:
        if os.path.isfile(chemin_complet):
            os.remove(chemin_complet)
            print(f"Fichier supprimé : {chemin_complet}")
        elif os.path.isdir(chemin_complet):
            shutil.rmtree(chemin_complet)
            print(f"Dossier supprimé : {chemin_complet}")
    except Exception as e:
        print(f"Erreur lors de la suppression : {e}")

def upload_fichier(chemin, region):
    """Upload un fichier avec versionning dans le fichier serveur ftp"""

    print("Upload vers le serveur FTP")
    print("Nom du fichier à upload : (chemin possible)")
    
    nom_fichier = input()

    chemin_source = os.path.join(chemin, nom_fichier)

    if not os.path.exists(chemin_source):
        print(f"Erreur : Le fichier '{nom_fichier}' existe pas")
        return
    
    if not os.path.isfile(chemin_source):
        print("Ce n'est pas un fichier !")
        return
    
    nom_fichieronly = os.path.basename(chemin_source)
    nom_sans_extension, extension = os.path.splitext(nom_fichieronly)

    region_lower = region.lower()
    cheminftp = os.path.join("serveur_ftp_paris", region_lower)

    num_v = 1

    if os.path.exists(cheminftp):
        fichiers = os.listdir(cheminftp)

        version_actuelles = []
        for fichier in fichiers:
     
            if fichier.startswith(f"{nom_sans_extension}_V") and fichier.endswith(extension):
                try:
                    partie_v = fichier.replace(f"{nom_sans_extension}_V", "").replace(extension, "")
                    num = int(partie_v)
                    version_actuelles.append(num)
                except ValueError:
                    pass
        
        if len(version_actuelles) > 0:
            num_v = max(version_actuelles) + 1
    
    nom_fichier_v = f"{nom_sans_extension}_V{num_v}{extension}"

    chemin_destination = os.path.join(cheminftp, nom_fichier_v)
    
    try:
        shutil.copy(chemin_source, chemin_destination)
        print("------------------------------------------------")
        print('--------------------------------------------')
        print(f"Version créée : V{num_v}")

    except Exception as e:
        print(f"Erreur lors de l'upload : {e}")

def download_fichier(chemin, region):
    """Download un fichier depuis le FTP Serveur"""

    print("Download depuis le serveur FTP Paris")

    region_lower = region.lower()
    cheminftp = os.path.join("serveur_ftp_paris", region_lower)

    if not os.path.exists(cheminftp):
        print(f"Erreur : Le serveur FTP pour la region {region} n'existe pas !")
        return

    fichiers = os.listdir(cheminftp)
    fichiers_only = []
    for fichier in fichiers:
        chemin_complet = os.path.join(cheminftp, fichier)
        if os.path.isfile(chemin_complet):
            fichiers_only.append(fichier)

    if len(fichiers_only) == 0:
        print(f"Le serveur FTP de la région de {region} est vide ( aucun fichier )")
        return
    
    print(f"Fichiers disponibles : ")
    print()
    for i, fichier in enumerate(fichiers_only, start=1):
        print(f"{i}. {fichier}")
    print("-------------------")
        
    print("Tapez le nom complet du fichier à télécharger : ")
    choix = input()

    fichier_choisi = None
    
    if choix in fichiers_only:
        fichier_choisi = choix
    else:
        print(f"Le fichier {choix} n'existe pas.")
        return

    chemin_source = os.path.join(cheminftp, fichier_choisi)

    print("____________________________________________________")
    print(f"Choisissez où télécharger le fichier {fichier_choisi} :")
    destination_usr = input()

    if destination_usr == "":
        chemin_destination = os.path.join(chemin, fichier_choisi)
    else:
        chemin_destination = os.path.join(chemin, destination_usr)
    
    if os.path.exists(chemin_destination):
        print(f" {chemin_destination} existe déjà !")
        confirmation = input("L'enregistrer quand même en écrasant l'autre ?")
        if confirmation.lower() !="oui":
            print("Téléchargement annulé")
            return
    try:
        shutil.copy(chemin_source, chemin_destination)
        print("------------------------------------------------")
        print('--------------------------------------------')
        print("Fichier téléchargé avec succès !")

    except Exception as e:
        print(f"Problème... : {e}")
