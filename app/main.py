# main.py

from utils import load_wordlist
from web_attack import web_login_brute_force
from pdf_cracker import crack_pdf
from imap_cracker import imap_brute_force
from wordpress_cracker import wp_login_brute_force

def menu():
    print("\n=== AI-Password Cracking Tool 🔐 ===")
    print("1. Web Login (formulaire POST)")
    print("2. PDF protégé")
    print("3. Email (IMAP)")
    print("4. WordPress Login")
    print("0. Quitter")
    return input("Sélectionnez un scénario [0–4] : ")

def main():
    wordlist = load_wordlist("data/rockyou.txt")

    while True:
        choix = menu()
        if choix == "1":
            # === Web Login ===
            url = input("URL du formulaire : ")
            username = input("Nom d'utilisateur : ")
            user_field = input("Nom du champ utilisateur (ex: email) : ")
            pass_field = input("Nom du champ mot de passe (ex: password) : ")
            success_check = input("Texte indicateur de succès (ex: 'token' ou 'Welcome') : ")
            web_login_brute_force(url, username, wordlist, user_field, pass_field, success_check)

        elif choix == "2":
            # === PDF Crack ===
            pdf_path = input("Chemin vers le PDF protégé : ")
            crack_pdf(pdf_path, wordlist)

        elif choix == "3":
            # === Email (IMAP) ===
            imap_server = input("Adresse du serveur IMAP (ex: imap.mail.local) : ")
            username = input("Nom d'utilisateur mail : ")
            imap_brute_force(imap_server, username, wordlist)

        elif choix == "4":
            # === WordPress ===
            wp_url = input("URL de la page wp-login.php : ")
            username = input("Nom d'utilisateur WordPress : ")
            wp_login_brute_force(wp_url, username, wordlist)

        elif choix == "0":
            print("Fermeture du programme.")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
