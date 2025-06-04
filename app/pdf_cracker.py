# pdf_cracker.py

import pikepdf

def crack_pdf(pdf_path, wordlist):
    """
    Essaie d'ouvrir un PDF protégé avec une wordlist.
    
    - pdf_path : chemin vers le fichier PDF protégé
    - wordlist : liste de mots de passe à tester
    """
    for password in wordlist:
        try:
            with pikepdf.open(pdf_path, password=password):
                print(f"[✔] PDF ouvert avec : {password}")
                return password
        except pikepdf._qpdf.PasswordError:
            continue
        except Exception as e:
            print(f"[!] Erreur : {e}")
            break

    print("[✘] Aucun mot de passe trouvé pour ce PDF.")
    return None
