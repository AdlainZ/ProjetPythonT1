class Person(object):
    """La classe Person pour un utilisateur"""

    def __init__(self, nom, prenom):
        print("Initialisation de la classe Person avec comme paramètre le nom et le prénom")
        self.nom = nom
        self.prenom = prenom

    def get_nom(self):
        return self.nom
    
    def get_prenom(self):
        return self.prenom
    
    def set_nom(self, nouveau_nom):
        if nouveau_nom == "":
            print ("Erreur : Il faut compléter le champ.")
        else:
            self.nom = nouveau_nom
            print("Le nom a été modifié.")
    
    def set_prenom(self, nouveau_prenom):
        if nouveau_prenom == "":
            print("Nop il manque le prenom")
        else:
            self.prenom = nouveau_prenom
            print("C'est bon")
    
    def afficher(self):
        print(f"Personne : {self.nom}, {self.prenom}")


