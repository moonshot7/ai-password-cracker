from app.web_attack import web_login_brute_force
from app.web_attack import json_login_brute_force
from app.wordpress_cracker import wp_login_brute_force
from app.imap_cracker import imap_brute_force
from app.utils import load_wordlist
from app.form_parser import auto_detect_form_fields_and_success
from app.offline_cracker import crack_hash

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
MIN_LEN = 4
MAX_LEN = 12

def launch_attack(mode, target_type, target, username, wordlist_path, hash_type="sha256", use_ai=False):
    wordlist = load_wordlist(wordlist_path) if wordlist_path else []

    if mode == "Offline Hash Cracking":
        return crack_hash(target, wordlist, hash_type)

    def run_dictionary():
        if target_type == "Web Form":
            user_field, pass_field, action_url, method, success_check = auto_detect_form_fields_and_success(target)
            return web_login_brute_force(
                url=target,
                username=username,
                wordlist=wordlist,
                user_field=user_field,
                pass_field=pass_field,
                success_check=success_check
            )
        elif target_type == "WordPress":
            return wp_login_brute_force(target, username, wordlist)
        elif target_type == "IMAP Email":
            return imap_brute_force(target, username, wordlist)
        elif target_type == "JSON Web Login":
            return json_login_brute_force(target, username, wordlist)

        else:
            yield 100, None

    def run_bruteforce():
        from app.brute_force import brute_force
        return brute_force(target, username, CHARSET, MIN_LEN, MAX_LEN)

    if mode == "Dictionary":
        return run_dictionary()
    elif mode == "Brute-force":
        return run_bruteforce()
    elif mode == "Both":
        for step in run_dictionary():
            yield step
            if step[1]: return
        for step in run_bruteforce():
            yield step
            if step[1]: return
    else:
        yield 100, None
