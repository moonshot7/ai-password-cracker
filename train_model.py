import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pickle
import os

# Charger les mots de passe
df = pd.read_csv("data/cleaned_passwords.csv")

# Créer des labels : vrais mots de passe = 1, mots aléatoires = 0
real_passwords = df["password"].dropna().unique().tolist()

# Générer des faux mots de passe aléatoires (mêmes longueurs)
import random
import string

def generate_random_password(length):
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    return ''.join(random.choices(chars, k=length))

fake_passwords = [generate_random_password(len(p)) for p in real_passwords]

# Construire dataset complet
all_passwords = real_passwords + fake_passwords
labels = [1] * len(real_passwords) + [0] * len(fake_passwords)

# Vectorisation
vectorizer = CountVectorizer(analyzer='char', ngram_range=(2, 4))
X = vectorizer.fit_transform(all_passwords)
y = labels

# Entraînement
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# Évaluation
y_pred = model.predict(X_test)
print("\n✅ Classification Report :\n")
print(classification_report(y_test, y_pred))

# Sauvegarder modèle et vectorizer
os.makedirs("ai", exist_ok=True)
with open("ai/password_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("ai/vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("✅ Modèle sauvegardé dans ai/password_model.pkl")
