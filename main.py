from classes.Person import Person
from classes.User import User
from utils.password_utils import generer_mdp, hash_mdp
from utils.csv_manager import save_user, charger_users
from utils.Auth import authentifier
from Menu import main_menu


#Test Person

print("----------PERSON----------")

# personne1 = Person("Nium", "Jhonny")
# personne2 = Person("Dupont", "Jean")

# personne1.afficher()
# personne2.afficher()

# print(f"Nom récupéré :{personne1.get_nom()}")
# print(f"Prénom récupéré : {personne1.get_prenom()}")
# print(f"Nom récupéré :{personne2.get_nom()}")
# print(f"Prénom récupéré :{personne2.get_prenom()}")

# personne1.set_nom("Martin")
# personne1.afficher()

# personne1.set_nom("")
# personne1.afficher()

print("-----------------USER------------------------")

#Test User

# user1 = User("Martin", "Sophie")
# user1.afficher()
# print(f"Login : {user1.login} ")
# user2 = User("DUPONT", "Jean")
# print(f"Login : {user2.login}")

# print("-----------MDP--------------------")

# mdp1 = generer_mdp()
# print(f"Mot de passe : {mdp1}")

# mdp2 = generer_mdp(5)
# print(f"Mot de passe court : {mdp2}")

# print("HASHED")

# mdp_clair = "MonMotDePasse213"
# mdp_hash = hash_mdp(mdp_clair)
# print(f"Mot de passe en clair : {mdp_clair}")
# print(f"Mot de passe hashed : {mdp_hash}")

# user1 = User("Jhonnyy", "Niumm")
# print(f"Login : {user1.login}")
# print(f"Password hashed : {user1.password}")

# print("\n--- TEST USER + DOUBLONS ---")
# user1 = User("Martin", "Sophie")
# print(f"User 1 - Login: {user1.login}")
# save_user(user1, "user")

# user2 = User("Martin", "Sophie")
# print(f"User 2 - Login: {user2.login}")
# save_user(user2, "user")

# user3 = User("Martin", "Sophie")
# print(f"User 3 - Login: {user3.login}")
# save_user(user3, "user")


# print("=================")
# print("=================")
# print("======TEST AUTHENTIFICATION===========")
# print("=================")
# print("=================")

# usertest = User("Babar", "John")
# print(f"Login créé : {usertest.login}")

# save_user(usertest, "user")

# print("Connexion")
# login_input = input("Entrez le login : ")
# mdp_input = input ("Entrez le mot de passe : ")

# resultat = authentifier(login_input, mdp_input)

# if resultat is not None:
#     print("Bienvenue !")
#     print(f"Bienvenue {resultat['prenom']}{resultat['nom']}")
#     print(f"Votre compte est un {resultat['type']}")
# else:
#     print("Echec de connexion.")
#
# 
# 
main_menu()

# print("-------------Test de l'ajout de la région :----------------------")

#user_test = User("Jhonny", "Tibaxx", "Marseille")
#save_user(user_test, "user")
