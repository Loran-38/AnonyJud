# Multi-stage build pour optimiser les performances du backend
FROM python:3.11-slim AS base

# Variables d'environnement pour optimiser Python
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Installer les dépendances système
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Stage 1: Dependencies
FROM base AS deps
WORKDIR /app

# Copier les fichiers de requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: Runtime
FROM base AS runtime
WORKDIR /app

# Copier les dépendances installées
COPY --from=deps /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Créer un utilisateur non-root
RUN useradd --create-home --shell /bin/bash app

# Copier le code source
COPY --chown=app:app . .

# Exposer le port
EXPOSE 8000

# Utiliser l'utilisateur non-root
USER app

# Healthcheck pour Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Commande de démarrage optimisée
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--access-log", "--log-level", "info"] 