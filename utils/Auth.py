from utils.csv_manager import charger_users
from utils.password_utils import hash_mdp

def authentifier(login, mot_de_passe):
    """Authentification via le login et le mot de passe"""

    utilisateurs = charger_users()
    print(f"Voici le nombre d'utilisateurs : {len(utilisateurs)}")

    for user in utilisateurs:
        if user['login'] == login:
            print(f"L'identifiant est : {login}")
        mdp_hash = hash_mdp(mot_de_passe)
        print(f"DEBUG: Hash du mdp tapé : {mdp_hash}") 
        print(f"DEBUG: Hash stocké : {user['password']}")
        print("Verification du mot de passe...")

        if mdp_hash == user['password']:
            print("Connexion réussie !")
            return user
        else:
            print("Connexion échouée")
            return None