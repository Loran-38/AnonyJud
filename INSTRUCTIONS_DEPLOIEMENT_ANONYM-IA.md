# 🚀 Instructions de Déploiement - www.anonym-ia.com

## 📋 Phase 1 : Configuration DNS chez OVH

### **Dans votre interface OVH :**

1. **Connectez-vous à votre espace client OVH**
   - Allez sur manager.ovh.com
   - Connectez-vous avec vos identifiants

2. **Accédez à la gestion DNS :**
   - Menu de gauche → "Noms de domaine"
   - Cliquez sur "anonym-ia.com"
   - Onglet "Zone DNS"

3. **Configuration des enregistrements DNS :**

**✅ Enregistrement A (domaine racine) :**
```
Type: A
Sous-domaine: (vide ou @)
Cible: 134.195.196.26
TTL: 3600
```

**✅ Enregistrement CNAME (www) :**
```
Type: CNAME  
Sous-domaine: www
Cible: anonyjud-app-production.up.railway.app.
TTL: 3600
```

**✅ Supprimez tous les autres enregistrements A ou CNAME existants pour éviter les conflits**

4. **Sauvegardez les modifications** (peut prendre 24h pour se propager)

---

## 🚄 Phase 2 : Configuration Railway

### **Dans Railway :**

1. **Allez dans votre projet :**
   - Dashboard Railway → anonyjud-app-production

2. **Ajoutez le domaine personnalisé :**
   - Onglet "Settings" 
   - Section "Domains"
   - Cliquez "Add Domain"
   - Ajoutez : `www.anonym-ia.com`
   - Ajoutez aussi : `anonym-ia.com` (redirection)

3. **Variables d'environnement à ajouter :**
```bash
REACT_APP_CUSTOM_DOMAIN=true
REACT_APP_DOMAIN_NAME=www.anonym-ia.com
```

---

## 🔥 Phase 3 : Configuration Firebase

### **Dans Firebase Console :**

1. **Authentication → Settings → Authorized domains**
   - Ajoutez : `www.anonym-ia.com`
   - Ajoutez : `anonym-ia.com`
   - Gardez temporairement : `anonyjud-app-production.up.railway.app`

2. **Mettez à jour les templates email :**
   - Remplacez toutes les occurrences de l'ancienne URL
   - Par : `https://www.anonym-ia.com`

---

## ✅ Phase 4 : Test et Vérification

### **Tests à effectuer :**

1. **Connectivité DNS :**
   - Testez sur : https://www.whatsmydns.net/
   - Vérifiez que www.anonym-ia.com pointe vers Railway

2. **SSL Certificate :**
   - Railway génère automatiquement le certificat SSL
   - Vérifiez sur : https://www.ssllabs.com/ssltest/

3. **Fonctionnalités :**
   - Authentification
   - Anonymisation de documents
   - Toutes les pages

4. **Performance :**
   - Testez sur : https://pagespeed.web.dev/

---

## 📧 Phase 5 : Communication (Optionnel)

1. **Redirection temporaire :**
   - Gardez l'ancien domaine Railway actif pendant 1 mois
   - Informez les utilisateurs du changement

2. **SEO :**
   - Mise à jour des liens externes
   - Redirection 301 si possible

---

## 🚨 Plan de Rollback (en cas de problème)

**Si problème critique :**
```bash
# Dans Railway, supprimez :
REACT_APP_CUSTOM_DOMAIN=true

# Puis redéployez
```

---

## 📞 Support

**En cas de problème :**
- DNS : Support OVH
- Hébergement : Support Railway  
- SSL : Automatique avec Railway
- Code : Logs dans Railway Console

**Outils de diagnostic :**
- DNS : whatsmydns.net
- SSL : ssllabs.com  
- Performance : pagespeed.web.dev
- Uptime : uptimerobot.com

---

## 🎯 Résultat Attendu

**Avant :** https://anonyjud-app-production.up.railway.app  
**Après :** https://www.anonym-ia.com ✨

**Délai total :** 2-24h (propagation DNS)  
**Downtime :** 0 minute (migration transparente) 