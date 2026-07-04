import socket
import time
import datetime
import threading


def menu_scan_reseau():
    while True:
        print("\nMenu Scan Réseau : \n")
        print("1 /Scanner une IP (reverse DNS)")
        print("2 /Scanner un nom de machine (DNS)")
        print("3 /Scanner une plage d'adresses")
        print("4 /Scanner tout le reseau")
        print("5 /Quitter")

        choix = input("Votre choix : ")

        if choix == '1':
            ip = input("Adresse IP a Scanné :")
            debut = time.time()
            reverse_dns(ip)
            fin = time.time()
            duree = fin - debut
            print(f"Temps d'execution : {duree:.3f} secondes")
            ecrire_log(f"Reverse DNS {ip} - duree {duree:.5f}s")

        elif choix == '2':
            nom = input("Nom de machine a Scanné : ")
            debut = time.time()
            dns(nom)
            fin = time.time()
            duree = fin - debut
            print(f"Temps d'execution : {duree:.4f} secondes")
            ecrire_log(f"DNS {nom} - duree {duree:.3f}s")

        elif choix == '3':
            base = input("Base du reseau 10.213.213.sans ici : ")
            try:
                poste_debut = int(input("Poste de debut : "))
                poste_fin = int(input("Poste de fin : "))
                debut = time.time()
                scan_plage(base, poste_debut, poste_fin)
                fin = time.time()
                duree = fin - debut
                print(f"Temps d'execution : {duree:.4f} secondes")
                ecrire_log(f"Scan plage {base}[{poste_debut}-{poste_fin}] - duree {duree:.4f}s")
            except ValueError:
                print("Erreur : les postes doivent etre des nombres entiers.")

        elif choix == '4':
            base_reseau = input("Base du reseau 10.213.sans ici : ")
            try:
                sous_reseau_debut = int(input("Sous-reseau de debut : "))
                sous_reseau_fin = int(input("Sous-reseau de fin : "))
                poste_debut = int(input("Poste de debut : "))
                poste_fin = int(input("Poste de fin : "))
                debut = time.time()
                scan_reseau(base_reseau, sous_reseau_debut, sous_reseau_fin, poste_debut, poste_fin)
                fin = time.time()
                duree = fin - debut
                print(f"Temps d'execution : {duree:.4f} secondes")
                ecrire_log(f"Scan reseau {base_reseau}[{sous_reseau_debut}-{sous_reseau_fin}] postes[{poste_debut}-{poste_fin}] - duree {duree:.4f}s")
            except ValueError:
                print("Erreur : les valeurs doivent etre des nombres entiers.")

        elif choix == '5':
            print("Fin du scan reseau.")
            break

        else:
            print("Choix invalide, veuillez reessayer.")


def ecrire_log(message):
    with open('scan_reseau_log.txt', 'a', encoding='utf-8') as f:
        date_actuelle = datetime.datetime.now().date()
        heure_actuelle = datetime.datetime.now().time()
        f.write(f"{date_actuelle} {heure_actuelle.strftime('%H:%M:%S')} - {message}\n\n")


def reverse_dns(ip):
    try:
        nom = socket.gethostbyaddr(ip)
        print(f"L'adresse IP {ip} correspond a : {nom[0]}")
        resultat = nom[0]
    except socket.herror:
        print(f"Aucun nom trouve pour l'adresse {ip}")
        resultat = "inconnu"
    return resultat


def dns(nom_machine):
    try:
        ip = socket.gethostbyname(nom_machine)
        print(f"Le nom {nom_machine} correspond a l'adresse IP : {ip}")
        resultat = ip
    except socket.gaierror:
        print(f"Impossible de Scanné le nom {nom_machine}")
        resultat = "inconnu"
    return resultat


def reverse_dns_thread(ip, resultats):
    resultat = reverse_dns(ip)
    resultats[ip] = resultat


def scan_plage(base, poste_debut, poste_fin):
    resultats = {}
    threads = []
    for poste in range(poste_debut, poste_fin + 1):
        ip = base + str(poste)
        t = threading.Thread(target=reverse_dns_thread, args=(ip, resultats))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return resultats


def scan_reseau(base_reseau, sous_reseau_debut, sous_reseau_fin, poste_debut, poste_fin):
    resultats = {}
    threads = []
    for sous_reseau in range(sous_reseau_debut, sous_reseau_fin + 1):
        for poste in range(poste_debut, poste_fin + 1):
            ip = f"{base_reseau}{sous_reseau}.{poste}"
            t = threading.Thread(target=reverse_dns_thread, args=(ip, resultats))
            threads.append(t)
            t.start()
    for t in threads:
        t.join()
    return resultats


if __name__ == '__main__':
    menu_scan_reseau()