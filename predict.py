import sys
import pickle
from sklearn.feature_extraction.text import CountVectorizer

if len(sys.argv) != 2:
    print("❌ Usage: python predict.py <password>")
    exit()

password = sys.argv[1]

# Charger modèle et vectorizer
with open("ai/password_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("ai/vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# Vectoriser et prédire
X = vectorizer.transform([password])
pred = model.predict(X)[0]
proba = model.predict_proba(X)[0][pred]

label = "✅ Likely Real" if pred == 1 else "⚠️ Likely Fake"
print(f"\n🔐 Password: {password}")
print(f"Prediction: {label} (Confidence: {proba:.2%})")
