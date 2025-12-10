from classes.Person import Person
from utils.password_utils import generer_mdp, hash_mdp
from utils.csv_manager import charger_users

class User(Person):
    """Classe qui hérite de Person, et donc qui récupère nom et prenom ainsi que les méthodes dedans."""
    
    def __init__(self, nom, prenom, region):
        print("Création d'un utilisateur...")
        Person.__init__(self, nom, prenom)
        self.login = None # A revoir ##
        self.region = region

        mdp_clair = generer_mdp()
        print(f"Mot de passe généré : {mdp_clair}")
        self.password = hash_mdp(mdp_clair)
    
    def generer_login(self, nom, prenom):
        """Generation du login via le nom et prenom"""
        premiere_lettre = prenom[0]
        login_base = premiere_lettre + nom
        login_base = login_base.lower() # ca met en minuscule ( avec sananes, ça faisait des calculs via la table ASCII )
        
        print("Chargement des utilisateurs...")
        utilisateurs = charger_users()
        print(f"Nombre de users : {len(utilisateurs)}")

        login_exist = []
        for user in utilisateurs:
            login_exist.append(user['login'])
        print(f"Logins existant : {login_exist}")

        login = login_base
        compteur = 1

        while login in login_exist:
            login = login_base + str(compteur) # galère : str va convertir le nombre en texte parce qu'on ne peut pas faire : jhonny + 1 ( deux types différents)
            compteur = compteur + 1
            
        print(f"Login final : {login}")
        self.login = login