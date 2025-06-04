import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from threading import Thread
from app.universal_cracker import launch_attack

def browse_file(entry):
    path = filedialog.askopenfilename()
    if path:
        entry.delete(0, tk.END)
        entry.insert(0, path)

def update_progress(percent):
    progress_var.set(percent)
    progress_bar.update_idletasks()

def log(message):
    log_area.insert(tk.END, message + "\n")
    log_area.see(tk.END)

def clear_logs():
    log_area.delete("1.0", tk.END)

def run_attack_thread():
    mode = mode_var.get()
    target_type = target_type_var.get()
    target = target_entry.get()
    username = username_entry.get()
    wordlist_path = wordlist_entry.get()
    use_ai = ai_var.get()

    if not mode:
        messagebox.showwarning("Missing Mode", "Select attack mode.")
        return

    if mode != "Offline Hash Cracking" and not all([target_type, target, username]):
        messagebox.showwarning("Missing Fields", "Please fill in all required fields.")
        return

    if mode in ["Dictionary", "Both", "Offline Hash Cracking"] and not wordlist_path:
        messagebox.showwarning("Missing Wordlist", "Wordlist is required.")
        return

    progress_bar["value"] = 0
    log_area.delete("1.0", tk.END)
    progress_label.config(text="Running...")

    def run():
        try:
            result = None
            for progress, found_password in launch_attack(mode, target_type, target, username, wordlist_path, use_ai=use_ai):
                update_progress(progress)
                if found_password:
                    result = found_password
                    break
            if result:
                log(f"[✔] Password found: {result}")
                messagebox.showinfo("Success", f"Password found: {result}")
            else:
                log("[✘] No password found.")
                messagebox.showwarning("Failure", "No password was found.")
        except Exception as e:
            log(f"[!] Error: {str(e)}")
        progress_label.config(text="")

    Thread(target=run).start()

# --- GUI SETUP ---
root = tk.Tk()
root.title("AI Password Cracker")
root.geometry("700x500")

tk.Label(root, text="Attack Mode").pack()
mode_var = tk.StringVar(value="Dictionary")
tk.OptionMenu(root, mode_var, "Brute-force", "Dictionary", "Both", "Offline Hash Cracking").pack()

tk.Label(root, text="Target Type").pack()
target_type_var = tk.StringVar(value="Web Form")
tk.OptionMenu(root, target_type_var, "Web Form", "WordPress", "IMAP Email").pack()

tk.Label(root, text="Target (URL / IP / Hash)").pack()
target_entry = tk.Entry(root, width=80)
target_entry.pack()

tk.Label(root, text="Username / Email (if needed)").pack()
username_entry = tk.Entry(root, width=50)
username_entry.pack()

tk.Label(root, text="Wordlist File").pack()
wordlist_entry = tk.Entry(root, width=50)
wordlist_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(wordlist_entry)).pack()

ai_var = tk.BooleanVar()
tk.Checkbutton(root, text="Enable AI model (coming soon)", variable=ai_var).pack()

tk.Button(root, text="Start Attack", command=run_attack_thread, bg="green", fg="white").pack(pady=10)

tk.Button(root, text="Clear Logs", command=clear_logs, bg="gray").pack(pady=5)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=500, mode="determinate", variable=progress_var)
progress_bar.pack()

progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack()

log_area = tk.Text(root, height=10, width=80, bg="black", fg="lime", font=("Courier", 10))
log_area.pack(pady=10)

root.mainloop()
