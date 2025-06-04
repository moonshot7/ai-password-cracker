import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
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

def run_attack_thread():
    mode = mode_var.get()
    target_type = target_type_var.get()
    target = target_entry.get()
    username = username_entry.get()
    wordlist_path = wordlist_entry.get()

    if not all([mode, target_type, target, username]):
        messagebox.showwarning("Missing Fields", "Please fill in all required fields.")
        return

    if mode in ["Dictionary", "Both"] and not wordlist_path:
        messagebox.showwarning("Missing Wordlist", "Wordlist is required for dictionary-based modes.")
        return

    progress_label.config(text="Attack running...")
    progress_bar["value"] = 0

    def run():
        result = None
        for progress, found_password in launch_attack(mode, target_type, target, username, wordlist_path):
            update_progress(progress)
            if found_password:
                result = found_password
                break

        if result:
            messagebox.showinfo("Success", f"Password found: {result}")
        else:
            messagebox.showwarning("Failure", "No password was found.")
        progress_label.config(text="")

    Thread(target=run).start()

# GUI setup
root = tk.Tk()
root.title("AI Password Cracker")
root.geometry("600x400")

tk.Label(root, text="Attack Mode").pack()
mode_var = tk.StringVar(value="Dictionary")
tk.OptionMenu(root, mode_var, "Brute-force", "Dictionary", "Both").pack()

tk.Label(root, text="Target Type").pack()
target_type_var = tk.StringVar(value="Web Form")
tk.OptionMenu(root, target_type_var, "Web Form", "WordPress", "IMAP Email").pack()

tk.Label(root, text="Target (URL or IP)").pack()
target_entry = tk.Entry(root, width=80)
target_entry.pack()

tk.Label(root, text="Username or Email").pack()
username_entry = tk.Entry(root, width=50)
username_entry.pack()

tk.Label(root, text="Wordlist File").pack()
wordlist_entry = tk.Entry(root, width=50)
wordlist_entry.pack()
tk.Button(root, text="Browse", command=lambda: browse_file(wordlist_entry)).pack()

tk.Button(root, text="Start Attack", command=run_attack_thread, bg="green", fg="white").pack(pady=10)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
progress_bar.pack(pady=10)

progress_label = tk.Label(root, text="", fg="blue")
progress_label.pack()

root.mainloop()
