# Fonctions utilitaires pour la gestion des fichiers, chiffrement, etc.

def lire_fichier(path):
    """Lit le contenu d'un fichier."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def ecrire_fichier(path, contenu):
    """Écrit du contenu dans un fichier."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(contenu) 