import pandas as pd
import os

input_path = "data/moroccan_passwords.txt"
output_path = "data/cleaned_passwords.csv"

# Vérifier si le fichier existe
if not os.path.exists(input_path):
    print(f"❌ Fichier non trouvé : {input_path}")
    exit()

# Lire les mots de passe
with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
    passwords = [line.strip() for line in f if line.strip()]

# Nettoyer (supprimer doublons, longueurs extrêmes)
df = pd.DataFrame(passwords, columns=["password"])
df = df.drop_duplicates()
df = df[df["password"].str.len().between(6, 20)]

# Sauvegarder
df.to_csv(output_path, index=False)
print(f"✅ Cleaned dataset saved as {output_path}")
