# 🔍 Guide Google Search Console - Anonym-IA

## 📋 Étape 1 : Accès à Google Search Console

1. **Allez sur** : https://search.google.com/search-console/
2. **Connectez-vous** avec votre compte Google
3. **Cliquez** "Ajouter une propriété"

## 🌐 Étape 2 : Ajouter votre domaine

### **Option A : Propriété de domaine (Recommandée)**
```
Type: Domaine
URL: anonym-ia.com
```

### **Option B : Préfixe d'URL**
```
Type: Préfixe d'URL  
URL: https://www.anonym-ia.com/
```

## 🔐 Étape 3 : Vérification du domaine

### **Méthode DNS (Recommandée pour Option A)**
1. Google vous donnera un **enregistrement TXT**
2. **Ajoutez-le dans OVH** :
   ```
   Type: TXT
   Nom: anonym-ia.com (ou @)
   Valeur: [code fourni par Google]
   TTL: 3600
   ```
3. **Attendez 1-24h** pour la propagation
4. **Cliquez "Vérifier"** dans Google

### **Méthode HTML (Pour Option B)**
1. **Téléchargez** le fichier de vérification Google
2. **Placez-le** dans `/anonyjud-app/public/`
3. **Commitez et pushez** sur Railway
4. **Vérifiez** que `https://www.anonym-ia.com/googleXXXXXX.html` est accessible

## 📄 Étape 4 : Soumettre le Sitemap

1. **Dans Google Search Console** → Sitemaps
2. **Saisissez** : `sitemap.xml`
3. **URL complète** : `https://www.anonym-ia.com/sitemap.xml`
4. **Cliquez** "Envoyer"

## 🎯 Étape 5 : Configuration avancée

### **URL à inspecter :**
- `https://www.anonym-ia.com/`
- `https://www.anonym-ia.com/anonymize`
- `https://www.anonym-ia.com/resources`

### **Mots-clés cibles pour le SEO :**
- "anonymisation documents juridiques"
- "pseudonymisation RGPD"
- "IA juridique conformité"
- "anonymisation PDF Word"
- "RGPD avocat"

## 📊 Étape 6 : Surveillance

**Surveillez dans Google Search Console :**
- **Performance** : clics, impressions, CTR
- **Couverture** : pages indexées/erreurs
- **Ergonomie mobile** : compatibilité mobile
- **Données structurées** : erreurs de balisage

## 🚨 Points d'attention

### **URLs à exclure de l'indexation :**
- `/api/*` (APIs backend)
- `/*?*` (paramètres de requête)
- Pages de développement

### **URLs prioritaires :**
- `/` (page d'accueil)
- `/anonymize` (fonctionnalité principale)
- `/resources` (contenu informatif)

## 🔧 Fichiers créés

✅ **`/public/sitemap.xml`** - Plan du site
✅ **`/public/robots.txt`** - Instructions pour les robots

## 📈 Optimisations SEO supplémentaires

### **Meta descriptions manquantes :**
- Ajoutez des meta descriptions pour chaque page
- Titre unique pour chaque page (balise `<title>`)
- Balises Open Graph pour les réseaux sociaux

### **Données structurées :**
- Schema.org pour les services juridiques
- JSON-LD pour les données de l'entreprise

---

**🎯 Prochaine étape :** Une fois le domaine vérifié, l'indexation commence dans 1-7 jours. 