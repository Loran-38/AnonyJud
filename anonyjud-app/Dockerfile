# Dockerfile optimisé pour Railway
FROM node:18-alpine AS builder

# Optimisations pour Alpine
RUN apk add --no-cache libc6-compat

WORKDIR /app

# Copier les fichiers de dépendances
COPY package*.json ./

# Installation des dépendances avec cache
RUN npm ci --only=production --cache /tmp/.npm && npm cache clean --force

# Copier le code source
COPY . .

# Build optimisé
ENV GENERATE_SOURCEMAP=false
ENV DISABLE_ESLINT_PLUGIN=true
RUN npm run build

# Stage de production
FROM node:18-alpine AS runner

WORKDIR /app

# Installer serve
RUN npm install -g serve

# Copier les fichiers buildés
COPY --from=builder /app/build ./build

EXPOSE $PORT

CMD ["serve", "-s", "build", "-l", "$PORT"] 