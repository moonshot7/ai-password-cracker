import tkinter as tk
from tkinter import messagebox
import joblib
import os

# Charger le modèle et le vectorizer
MODEL_PATH = "ai/password_model.pkl"
VECTORIZER_PATH = "ai/vectorizer.pkl"

if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
    raise FileNotFoundError("Modèle ou vectorizer introuvable.")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

def predict_password_strength():
    password = entry.get().strip()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return
    
    X = vectorizer.transform([password])
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0][prediction] * 100

    if prediction == 1:
        result_label.config(text=f"✅ Likely Real ({proba:.2f}%)", fg="green")
    else:
        result_label.config(text=f"⚠ Likely Fake ({proba:.2f}%)", fg="red")

# Interface Tkinter
root = tk.Tk()
root.title("AI Password Predictor")
root.geometry("400x200")
root.config(bg="#222")

tk.Label(root, text="Enter Password:", bg="#222", fg="white", font=("Arial", 12)).pack(pady=10)
entry = tk.Entry(root, show="*", width=30, font=("Arial", 12))
entry.pack()

tk.Button(root, text="Check", command=predict_password_strength, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)
result_label = tk.Label(root, text="", bg="#222", fg="white", font=("Arial", 12))
result_label.pack()

root.mainloop()
