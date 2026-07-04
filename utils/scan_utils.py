import socket
import time
import datetime
import threading


def menu_scan():
    while True:
        print("\nScan menu :")
        print("1 / Scanner un port specifique")
        print("2 / Scanner une plage de port")
        print("3 / Scanner tous les ports d'une plage")
        print("4 /Quitter")

        choix = input("Choix :")

        if choix == '1':
            hote = input("Adresse IP ou nom de machine:")
            try:
                port = int(input("Numero port:"))
                debut = time.time()
                scan_port(hote, port)
                fin = time.time()
                duree = fin - debut
                print(f"Temps d'execution : {duree:.3f} secondes")
                ecrire_log(f"Scan port unique {hote}:{port} - duree {duree:.3f}s")
            except ValueError:
                print("Erreur le port doit etre un nombre ientier.")

        elif choix == '2':
            hote = input("Adresse IP ou nom de machine: ")
            try:
                port_debut = int(input("Port de debut : "))
                port_fin = int(input("Port de fin :"))
                debut = time.time()
                scan_plage_ports(hote, port_debut, port_fin)
                fin = time.time()
                duree = fin - debut
                print(f"Temps d'execution : {duree:.3f} secondes")
                ecrire_log(f"Scan plage {hote}[{port_debut}-{port_fin}] - duree {duree:.3f}s")
            except ValueError:
                print("Erreur : les ports doivent etre des nombres entiers")

        elif choix == '3':
            hote = input("Adresse IP ou nom de machine : ")
            try:
                port_debut = int(input("Port de debut : "))
                port_fin = int(input("Port de fin : "))
                debut = time.time()
                scan_tous_ports_thread(hote, port_debut, port_fin)
                fin = time.time()
                duree = fin - debut
                print(f"Temps d'execution : {duree:.3f} secondes")
                ecrire_log(f"Scan threade {hote}[{port_debut}-{port_fin}] - duree {duree:.11f}s")
            except ValueError:
                print("Erreur : les ports doivent etre des nombres entier")

        elif choix == '4':
            print("Fin du scan de ports !!!!")
            break

        else:
            print("Choix invalide, veuillez reessayer !!!!!1")


def ecrire_log(message):
    with open('scan_log.txt', 'a', encoding='utf-8') as f:
        date_actuelle = datetime.datetime.now().date()
        heure_actuelle = datetime.datetime.now().time()
        f.write(f"{date_actuelle} {heure_actuelle.strftime('%H:%M:%S')} - {message}\n")


def scan_port(hote, port):
    connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connexion.connect((hote, port))
        print(f"Le port {port} est ouvert.")
        resultat = "ouvert"
    except socket.error:
        print(f"Le port {port} est ferméé")
        resultat = "ferme"
    finally:
        connexion.close()
    ecrire_log(f"{hote}:{port} -> {resultat}")
    return resultat


def scan_plage_ports(hote, port_debut, port_fin):
    resultats = {}
    for port in range(port_debut, port_fin + 1):
        resultat = scan_port(hote, port)
        resultats[port] = resultat
    return resultats


def scan_port_thread(hote, port, resultats):
    resultat = scan_port(hote, port)
    resultats[port] = resultat


def scan_tous_ports_thread(hote, port_debut, port_fin):
    resultats = {}
    threads = []
    for port in range(port_debut, port_fin + 1):
        t = threading.Thread(target=scan_port_thread, args=(hote, port, resultats))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return resultats


if __name__ == '__main__':
    menu_scan()