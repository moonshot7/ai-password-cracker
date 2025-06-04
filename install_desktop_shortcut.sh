#!/bin/bash

# === Paramètres ===
BIN_PATH="$HOME/ai-password-cracker/dist/gui_cracker"
DESKTOP_FILE="$HOME/.local/share/applications/PasswordCracker.desktop"
ICON_PATH="$HOME/ai-password-cracker/icon.png" # <- facultatif

# === Vérification du binaire ===
if [ ! -f "$BIN_PATH" ]; then
    echo "[❌] L'exécutable $BIN_PATH est introuvable."
    echo "➡️  Lance d'abord ./build_app.sh pour le générer."
    exit 1
fi

# === Créer le dossier des raccourcis si besoin ===
mkdir -p ~/.local/share/applications

# === Générer le fichier .desktop ===
echo "[Desktop Entry]
Name=AI Password Cracker
Exec=$BIN_PATH
Icon=${ICON_PATH:-utilities-terminal}
Type=Application
Categories=Utility;
Terminal=false
" > "$DESKTOP_FILE"

# === Donner les droits ===
chmod +x "$DESKTOP_FILE"

echo "[✅] Raccourci créé : $DESKTOP_FILE"
echo "[🚀] Tu peux maintenant lancer ton outil depuis le menu (Rechercher 'AI Password Cracker')."
