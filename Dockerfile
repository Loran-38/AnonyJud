# Dockerfile optimisé pour Railway avec LibreOffice
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
    # Polices système pour une meilleure compatibilité
    fonts-liberation \
    fonts-dejavu \
    fonts-noto \
    # Outils système nécessaires
    curl \
    wget \
    unzip \
    # Nettoyage pour réduire la taille de l'image
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances Python
COPY anonyjud-backend/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copier le code de l'application
COPY anonyjud-backend/ .

# Créer un répertoire pour les fichiers temporaires
RUN mkdir -p /tmp/anonyjud

# Vérifier que LibreOffice est bien installé et accessible
RUN soffice --version || echo "LibreOffice installé avec succès"
RUN which soffice || echo "LibreOffice trouvé dans le PATH"
RUN ls -la /usr/bin/soffice || echo "LibreOffice dans /usr/bin"

# Exposer le port (à adapter selon ta configuration)
EXPOSE 8000

# Commande de démarrage
CMD ["python", "anonyjud-backend/start_backend.py"] 