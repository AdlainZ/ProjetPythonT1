import os
import shutil

def init_dossiers_regions():
    """Initialise les dossiers des régions si ça n'existe pas"""

    regions = ["marseille", "rennes", "grenoble"]

    for region in regions:
        nom_dossier = f"fichiers_{region}"
        if not os.path.exists(nom_dossier):
            os.mkdir(nom_dossier)
            print(f"Dossier {nom_dossier} créé")
        else:
            print(f"Dossier {nom_dossier} existe déjà.")