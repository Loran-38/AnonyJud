# Multi-stage build pour optimiser les performances
FROM node:18-alpine AS deps
WORKDIR /app

# Installer les dépendances système nécessaires
RUN apk add --no-cache libc6-compat python3 make g++

# Copier les fichiers de dépendances
COPY package*.json ./
COPY tailwind.config.js ./
COPY postcss.config.js ./

# Installer uniquement les dépendances de production
RUN npm ci --only=production --no-audit --no-fund && npm cache clean --force

# Stage 2: Build
FROM node:18-alpine AS builder
WORKDIR /app

# Copier les dépendances depuis le stage précédent
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Variables d'environnement pour optimiser le build
ENV NODE_ENV=production
ENV GENERATE_SOURCEMAP=false
ENV DISABLE_ESLINT_PLUGIN=true
ENV CI=true

# Build l'application
RUN npm run build

# Stage 3: Runtime
FROM node:18-alpine AS runner
WORKDIR /app

# Installer serve globalement
RUN npm install -g serve@14.2.0

# Créer un utilisateur non-root pour la sécurité
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# Copier les fichiers buildés
COPY --from=builder --chown=nextjs:nodejs /app/build ./build
COPY --from=builder --chown=nextjs:nodejs /app/public ./public

# Exposer le port
EXPOSE 3000

# Utiliser l'utilisateur non-root
USER nextjs

# Healthcheck pour Railway
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:3000/ || exit 1

# Commande de démarrage optimisée
CMD ["serve", "-s", "build", "-l", "3000", "--no-clipboard", "--no-port-switching"] 