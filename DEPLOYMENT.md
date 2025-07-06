# Déploiement sur Railway

## Étapes pour déployer AnonyJud sur Railway

### 1. Préparation du code
✅ **Déjà fait** : Les fichiers de configuration ont été créés
- `anonyjud-backend/Procfile` : Configuration du serveur backend
- `anonyjud-backend/railway.json` : Configuration Railway pour le backend
- `anonyjud-backend/requirements.txt` : Dépendances Python
- `anonyjud-app/nixpacks.toml` : Configuration Railway pour le frontend
- `anonyjud-app/src/config.js` : Configuration des URLs API

### 2. Déploiement du Backend

1. **Connectez-vous à Railway** : https://railway.app/
2. **Créez un nouveau projet** : "New Project"
3. **Déployez depuis GitHub** :
   - Connectez votre compte GitHub
   - Sélectionnez votre repository
   - Choisissez le dossier `anonyjud-backend`
4. **Configuration** :
   - Railway détectera automatiquement que c'est un projet Python
   - Les dépendances seront installées automatiquement
   - Le serveur démarrera sur le port défini par Railway

### 3. Déploiement du Frontend

1. **Créez un second service** dans le même projet Railway
2. **Déployez depuis GitHub** :
   - Sélectionnez le même repository
   - Choisissez le dossier `anonyjud-app`
3. **Variables d'environnement** :
   - Ajoutez `REACT_APP_API_URL` avec l'URL de votre backend Railway
   - Exemple : `https://votre-backend-production.railway.app`

### 4. Configuration post-déploiement

1. **Récupérez l'URL du backend** :
   - Allez dans les paramètres du service backend
   - Copiez l'URL publique (ex: `https://votre-backend-production.railway.app`)

2. **Mettez à jour la configuration du frontend** :
   - Ajoutez la variable d'environnement `REACT_APP_API_URL`
   - Ou modifiez directement le fichier `src/config.js`

3. **Redéployez le frontend** si nécessaire

### 5. Test de l'application

1. **Testez le backend** : `https://votre-backend-production.railway.app/`
2. **Testez le frontend** : `https://votre-frontend-production.railway.app/`
3. **Vérifiez la communication** entre frontend et backend

## URLs importantes

- **Backend** : `https://votre-backend-production.railway.app`
- **Frontend** : `https://votre-frontend-production.railway.app`
- **Documentation API** : `https://votre-backend-production.railway.app/docs`

## Commandes utiles

```bash
# Pour tester localement avant déploiement
cd anonyjud-backend
pip install -r requirements.txt
uvicorn app.main:app --reload

cd ../anonyjud-app
npm install
npm start
```

## Dépannage

- **Erreur CORS** : Vérifiez que l'URL du backend est correcte dans la configuration
- **Erreur 404** : Assurez-vous que les routes sont correctement configurées
- **Erreur de build** : Vérifiez les logs Railway pour identifier les problèmes

## Structure finale

```
Anonyjud/
├── anonyjud-backend/          # API FastAPI
│   ├── app/
│   ├── Procfile              # Configuration Railway
│   ├── railway.json          # Configuration Railway
│   └── requirements.txt      # Dépendances Python
├── anonyjud-app/             # Frontend React
│   ├── src/
│   ├── nixpacks.toml         # Configuration Railway
│   └── package.json          # Dépendances Node.js
└── DEPLOYMENT.md             # Ce fichier
``` 