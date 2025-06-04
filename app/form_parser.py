import requests
from bs4 import BeautifulSoup

def auto_detect_form_fields_and_success(url, test_user="admin", test_password="wrongpass"):
    try:
        # Étape 1 : Récupérer et parser le formulaire
        response = requests.get(url, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')

        form = soup.find('form')
        if not form:
            raise Exception("Aucun formulaire trouvé sur la page.")

        inputs = form.find_all('input')
        user_field = None
        pass_field = None

        for input_tag in inputs:
            name = input_tag.get('name', '').lower()
            if 'user' in name or 'email' in name:
                user_field = input_tag['name']
            elif 'pass' in name:
                pass_field = input_tag['name']

        form_action = form.get('action') or url
        if not form_action.startswith("http"):
            form_action = requests.compat.urljoin(url, form_action)

        method = form.get('method', 'post').lower()

        if not user_field or not pass_field:
            raise Exception("Champs utilisateur/mot de passe non détectés.")

        # Étape 2 : Faire une fausse tentative pour capturer une erreur
        data = {
            user_field: test_user,
            pass_field: test_password
        }

        fake = requests.post(form_action, data=data, timeout=5) if method == "post" else requests.get(form_action, params=data, timeout=5)
        content = fake.text.lower()

        # Étape 3 : Rechercher des indicateurs d'échec ou de succès
        common_failures = ["invalid", "incorrect", "wrong", "failed", "unauthorized"]
        common_success = ["welcome", "dashboard", "token", "logged", "redirect"]

        found = None
        for keyword in common_success:
            if keyword in content:
                found = keyword
                break

        # Retourner tout
        return user_field, pass_field, form_action, method, found or "dashboard"

    except Exception as e:
        print(f"[!] Erreur dans l'analyse automatique : {e}")
        return None, None, None, None, "dashboard"
