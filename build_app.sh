#!/bin/bash

# === Script pour créer une app exécutable depuis gui_cracker.py ===

echo "[🔧] Construction de l'exécutable avec PyInstaller..."

# Nettoyage des anciennes builds
rm -rf build dist gui_cracker.spec

# Création de l'exécutable (mode GUI : pas de terminal qui s'affiche)
pyinstaller --noconfirm --onefile --windowed gui_cracker.py

# Vérification
if [[ -f dist/gui_cracker ]]; then
    echo "[✅] Fichier exécutable généré : dist/gui_cracker"
    echo "[💡] Tu peux maintenant le lancer directement par double-clic ou via un raccourci."
else
    echo "[❌] Échec de la génération."
fi
