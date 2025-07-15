# 🩺 Guide de Diagnostic - Gros Fichiers PDF

## ✅ Corrections Appliquées

### Backend (Railway déployé)
- **Logs détaillés** dans `/anonymize/file` pour diagnostiquer l'erreur 500
- **Gestion d'erreurs robuste** avec traceback complet
- **Diagnostic taille fichier** et avertissements automatiques
- **Messages d'erreur informatifs** selon le contexte

### Frontend (Production déployé)
- **Correction erreur React** : `style jsx` → `style` (attribut non-booléen)
- **Logs détaillés console** pour debugging
- **Messages d'erreur améliorés** selon type (500, timeout, réseau)
- **Affichage taille fichier** et warnings pour gros fichiers

## 🔍 Comment Diagnostiquer

### 1. Côté Frontend (Console Navigateur)
```javascript
// Ouvrir F12 → Console avant d'uploader le fichier
// Logs automatiques:
🚀 FRONTEND - Début traitement fichier
📁 Fichier: document.pdf
📊 Taille: 4,745,728 bytes (4.5 MB)
⚠️ GROS FICHIER DÉTECTÉ: 4.5 MB
📡 Envoi requête vers backend...
❌ Erreur HTTP: 500 Internal Server Error
```

### 2. Côté Backend (Logs Railway)
```bash
# Dans les logs Railway :
🚀 ANONYMIZE_FILE - Début du traitement
📁 Fichier reçu: document.pdf
📦 Taille du fichier: 4,745,728 bytes (4.5 MB)
⚠️ GROS FICHIER DÉTECTÉ: 4.5 MB - Traitement peut être lent
📄 Traitement PDF avec pipeline sécurisé PDF → Word → PDF...
❌ Erreur pipeline PDF: [Erreur détaillée]
📄 Traceback complet: [Stack trace]
```

## 🚨 Types d'Erreurs Identifiées

### Erreur 500 - Fichier Trop Volumineux
**Symptômes:**
- Fichier > 100 MB
- Erreur mémoire dans les logs
- Timeout de traitement

**Solutions:**
1. Utiliser l'endpoint `/anonymize/pdf/auto` (sélection automatique)
2. Segmenter le fichier en parties plus petites
3. Réduire la qualité/résolution des images

### Erreur 500 - Fichier Corrompu/Complexe
**Symptômes:**
- PDF avec structure complexe
- Erreurs PyMuPDF ou pdf2docx
- Images lourdes, tableaux complexes

**Solutions:**
1. Essayer différentes méthodes via `/anonymize/pdf/auto`
2. Convertir le PDF vers un format plus simple
3. Utiliser un PDF/A optimisé

## 📊 Endpoints Recommandés

### Pour Gros Fichiers (> 100 MB)
```bash
POST /anonymize/pdf/auto
- force_method: "auto" (recommandé)
- force_method: "direct" (si pipeline échoue)
- force_method: "pipeline" (pour qualité optimale)
```

### Pour Fichiers Standards (< 100 MB)
```bash
POST /anonymize/file  # Méthode classique
```

## 🔧 Paramètres de Test

### Limites Actuelles
- **< 100 MB**: Traitement optimal
- **100-500 MB**: Traitement lent mais possible
- **500 MB-1 GB**: Risque d'erreur mémoire
- **> 1 GB**: Échec probable, segmentation requise

### Variables à Surveiller
- Taille fichier (bytes)
- Nombre de pages
- Complexité (images, tableaux)
- Mémoire serveur disponible
- Timeout réseau/serveur

## 🎯 Test de Votre Fichier 4.5 MB

Votre fichier de **4745 KB** devrait maintenant fonctionner car :
1. ✅ Taille < 100 MB (limite de sécurité)
2. ✅ Logs détaillés pour identifier le problème exact
3. ✅ Gestion d'erreur améliorée
4. ✅ Fallback automatique si nécessaire

## 📞 Support

Si le problème persiste :
1. **Copier les logs console** (F12)
2. **Vérifier les logs Railway** (backend)
3. **Noter la taille exacte** du fichier
4. **Essayer `/anonymize/pdf/auto`** avec `force_method=direct`

---
*Mis à jour le $(date) - Corrections déployées* 