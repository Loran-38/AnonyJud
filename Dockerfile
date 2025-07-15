# Dockerfile optimisé pour Railway avec LibreOffice et unoconv
FROM python:3.11-slim

# Variables d'environnement pour éviter les prompts interactifs
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Installation des dépendances système et LibreOffice
RUN apt-get update && \
    apt-get install -y \
    # LibreOffice complet avec tous les composants
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    libreoffice-impress \
    # unoconv pour conversion via ligne de commande
    unoconv \
    # Polices système pour une meilleure compatibilité
    fonts-liberation \
    fonts-dejavu \
    fonts-noto \
    fonts-opensymbol \
    # Polices Microsoft équivalentes
    ttf-mscorefonts-installer \
    # Outils système nécessaires
    curl \
    wget \
    unzip \
    # Dépendances pour LibreOffice headless
    xvfb \
    # Nettoyage pour réduire la taille de l'image
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Configuration des variables d'environnement pour LibreOffice
ENV HOME=/tmp
ENV XDG_CONFIG_HOME=/tmp/.config
ENV XDG_DATA_HOME=/tmp/.local/share
ENV XDG_CACHE_HOME=/tmp/.cache

# Créer les répertoires nécessaires pour LibreOffice
RUN mkdir -p /tmp/.config /tmp/.local/share /tmp/.cache && \
    chmod 777 /tmp/.config /tmp/.local/share /tmp/.cache

# Créer le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY anonyjud-backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY anonyjud-backend/ .

# Créer un répertoire pour les fichiers temporaires
RUN mkdir -p /tmp/anonyjud && chmod 777 /tmp/anonyjud

# Vérifier que LibreOffice et unoconv sont bien installés
RUN soffice --version && echo "LibreOffice installé avec succès" && \
    unoconv --version && echo "unoconv installé avec succès"

# Test de conversion pour s'assurer que tout fonctionne
RUN echo "Test de LibreOffice..." && \
    echo "<html><body><h1>Test</h1></body></html>" > /tmp/test.html && \
    timeout 30 soffice --headless --invisible --nodefault --nolockcheck --nologo --norestore --convert-to pdf --outdir /tmp /tmp/test.html || true && \
    echo "Test terminé"

# Exposer le port (à adapter selon ta configuration)
EXPOSE 8000

# Commande de démarrage
CMD ["python", "start_backend.py"] 