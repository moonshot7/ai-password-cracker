import hashlib

def crack_hash(hash_value, wordlist, hash_type="sha256"):
    hash_func = getattr(hashlib, hash_type)
    total = len(wordlist)

    for i, password in enumerate(wordlist):
        hashed = hash_func(password.encode()).hexdigest()
        progress = (i + 1) / total * 100
        yield progress, password if hashed == hash_value else None
