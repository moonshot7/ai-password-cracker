import tkinter as tk
from tkinter import ttk, messagebox
from utils import load_wordlist, log_attempt
from universal_cracker import analyze_target, launch_attack
import threading

class UniversalCrackerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Universal Password Cracker GUI")
        self.root.geometry("650x500")
        self.build_interface()

    def build_interface(self):
        # Type de cible
        ttk.Label(self.root, text="🎯 Type de cible :", font=("Arial", 12)).pack(pady=5)
        self.target_type = tk.StringVar(value="web")
        self.type_menu = ttk.Combobox(self.root, textvariable=self.target_type, state="readonly")
        self.type_menu['values'] = ["web", "wordpress", "imap", "pdf"]
        self.type_menu.pack(pady=5)

        # Champ URL/email/chemin
        ttk.Label(self.root, text="🔗 URL / Email / Chemin fichier :").pack()
        self.target_entry = ttk.Entry(self.root, width=60)
        self.target_entry.pack(pady=5)

        # Username (optionnel)
        ttk.Label(self.root, text="👤 Nom d'utilisateur (facultatif) :").pack()
        self.username_entry = ttk.Entry(self.root, width=40)
        self.username_entry.pack(pady=5)

        # Mode d'attaque
        ttk.Label(self.root, text="⚙️ Méthode d'attaque :").pack()
        self.mode_var = tk.StringVar(value="dictionary")
        ttk.Radiobutton(self.root, text="Dictionnaire", variable=self.mode_var, value="dictionary").pack()
        ttk.Radiobutton(self.root, text="Brute-force", variable=self.mode_var, value="brute").pack()

        # Bruteforce options
        charset_frame = ttk.Frame(self.root)
        charset_frame.pack(pady=5)
        self.charset_entry = ttk.Entry(charset_frame, width=20)
        self.charset_entry.insert(0, "abc123")
        self.min_len_entry = ttk.Entry(charset_frame, width=5)
        self.min_len_entry.insert(0, "4")
        self.max_len_entry = ttk.Entry(charset_frame, width=5)
        self.max_len_entry.insert(0, "6")

        ttk.Label(charset_frame, text="Charset:").pack(side="left")
        self.charset_entry.pack(side="left", padx=5)
        ttk.Label(charset_frame, text="Min:").pack(side="left")
        self.min_len_entry.pack(side="left")
        ttk.Label(charset_frame, text="Max:").pack(side="left")
        self.max_len_entry.pack(side="left")

        # Lancer + Résultat
        self.launch_btn = ttk.Button(self.root, text="🚀 Lancer l'attaque", command=self.run_attack)
        self.launch_btn.pack(pady=15)

        self.result_label = ttk.Label(self.root, text="", font=("Courier", 11), foreground="green")
        self.result_label.pack(pady=10)

    def run_attack(self):
        self.result_label.config(text="⏳ Attaque en cours...")
        self.launch_btn.config(state="disabled")

        def attack():
            try:
                target_type = self.target_type.get()
                target = self.target_entry.get().strip()
                username = self.username_entry.get().strip() or target
                mode = self.mode_var.get()
                charset = self.charset_entry.get().strip()
                min_len = int(self.min_len_entry.get())
                max_len = int(self.max_len_entry.get())

                wordlist = load_wordlist("data/rockyou.txt") if mode == "dictionary" else []

                found = launch_attack(
                    target_type, target, username, wordlist, mode, charset, min_len, max_len
                )

                log_attempt(target, username, mode, found if found else "Not found")

                self.result_label.config(
                    text=f"[✔] Mot de passe : {found}" if found else "[✘] Aucun mot de passe trouvé."
                )
            except Exception as e:
                self.result_label.config(text=f"[!] Erreur : {e}")
            finally:
                self.launch_btn.config(state="normal")

        threading.Thread(target=attack).start()

if __name__ == "__main__":
    root = tk.Tk()
    app = UniversalCrackerGUI(root)
    root.mainloop()
