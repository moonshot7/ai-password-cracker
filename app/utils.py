# utils.py

import csv
from datetime import datetime

def load_wordlist(path):
    """
    Charge une wordlist sans modifier le contenu original.
    Supprime simplement les lignes vides et doublons.
    """
    wordlist = set()

    with open(path, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            word = line.strip()
            if word:
                wordlist.add(word)

    return list(wordlist)

def save_wordlist(wordlist, output_path):
    """
    Enregistre une wordlist dans un fichier texte.
    """
    with open(output_path, 'w', encoding='utf-8') as f:
        for word in wordlist:
            f.write(f"{word}\n")

def log_attempt(target, username, mode, result, path="logs/results.csv"):
    """Enregistre une tentative dans un fichier CSV"""
    try:
        with open(path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([datetime.now(), target, username, mode, result])
    except Exception as e:
        print(f"[!] Erreur en loggant la tentative : {e}")
