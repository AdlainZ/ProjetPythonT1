import random
import string
import hashlib

def generer_mdp(taille = 12): # définition d'une valeur par défaut comme ça
    """Generation d'un mdp aléatoire avec la taille x"""
    caracteres = string.ascii_letters + string.digits + string.punctuation

    mdp = ""
    for i in range(taille):
        mdp += caracteres[random.randint(0, len(caracteres)-1)]
    
    return mdp

def hash_mdp(mdp):
    """Hash le mdp avec l'algorithme SHA-256"""
    mdp_hashed = hashlib.sha256(mdp.encode()).hexdigest() # .encode en bytes pr que sha comprenne
    return mdp_hashed
