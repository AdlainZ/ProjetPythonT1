from classes.User import User

class Admin(User):
    """Classe héritant de User, qui hérite lui meme de Person, pour eviter de refaire tous les autres paramètres"""

    def __init__(self, nom, prenom, niveau_droits=1):
        print("Création d'un admin...")
        User.__init__(self, nom, prenom)
        self.niveau_droits = niveau_droits

    def afficher_admin(self):
        """Affiche les infos de l'admin"""
        print(f"Admin : {self.nom} {self.prenom}")
        print(f"Login : {self.login}")
        print(f"Niveau de droits : {self.niveau_droits}")
        
    def verification_gerer_users(self):
        """Verifie si l'admin peut gérer les users"""
        return self.niveau_droits >=1
    
    def verification_gerer_admins(self):
        """Verifie si le superadmin peut gérer les autres admins"""
        return self.niveau_droits >=2
    