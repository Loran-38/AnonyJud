# Configuration des Emails Personnalisés Firebase Auth

## Vue d'ensemble

Ce guide explique comment configurer des emails personnalisés pour la réinitialisation de mot de passe dans Firebase Auth avec le design AnonyJud.

## 🎯 Objectif

Remplacer l'email Firebase par défaut par un email personnalisé avec :
- Design cohérent avec AnonyJud
- Couleurs bleues du site
- Logo et branding
- Informations sur l'IA Act/RGPD
- Template HTML responsive

## 📋 Étapes de Configuration

### 1. Accéder à la Console Firebase

1. Allez sur [Firebase Console](https://console.firebase.google.com/)
2. Sélectionnez votre projet "AnonyJud"
3. Cliquez sur "Authentication" dans le menu latéral
4. Allez dans l'onglet "Templates"

### 2. Configurer le Template de Réinitialisation

1. Sélectionnez "Réinitialisation du mot de passe"
2. Cliquez sur "Modifier le template"
3. Configurez les paramètres suivants :

#### Paramètres de Base
```
Nom de l'expéditeur: AnonyJud
Adresse de réponse: support@anonyjud.com (optionnel)
Objet: Réinitialisation de votre mot de passe AnonyJud
```

#### Template HTML
Copiez le contenu du template HTML depuis `src/services/emailService.js` (variable `customEmailTemplate.html`)

### 3. Variables Disponibles

Firebase remplace automatiquement ces variables :
- `%LINK%` → Lien de réinitialisation
- `%EMAIL%` → Email de l'utilisateur
- `%DISPLAY_NAME%` → Nom d'affichage (si disponible)

### 4. Domaine Personnalisé (Optionnel)

Pour utiliser votre propre domaine pour les liens :

1. Allez dans "Settings" → "Project settings"
2. Onglet "General"
3. Section "Public-facing name"
4. Ajoutez votre domaine personnalisé

## 🎨 Template HTML Personnalisé

Le template inclut :

### Design Features
- **Header** : Logo AnonyJud avec dégradé bleu
- **Bouton CTA** : Style cohérent avec le site
- **Section sécurité** : Conseils et informations importantes
- **Footer** : Liens vers le site et informations légales
- **Responsive** : Adapté mobile et desktop

### Couleurs Utilisées
- Bleu principal : `#2563eb`
- Bleu foncé : `#1d4ed8`
- Gris texte : `#6b7280`
- Arrière-plan : `#f8fafc`

### Éléments Inclus
- ✅ Logo avec icône bouclier
- ✅ Message personnalisé
- ✅ Bouton de réinitialisation stylisé
- ✅ Conseils de sécurité
- ✅ Information sur l'IA Act/RGPD
- ✅ Liens vers le site
- ✅ Design responsive

## 🔧 Configuration Technique

### Action Code Settings
```javascript
const actionCodeSettings = {
  url: `${window.location.origin}/login`,
  handleCodeInApp: false,
};
```

### Service Email
Le service `emailService.js` gère :
- Envoi d'emails avec paramètres personnalisés
- Gestion d'erreurs spécifiques
- Messages d'erreur en français
- Redirection après réinitialisation

## 📱 Test de l'Email

### 1. Test Local
```bash
npm start
# Aller sur /forgot-password
# Entrer un email valide
# Vérifier la réception
```

### 2. Test de Production
1. Déployer sur Railway
2. Utiliser la fonction mot de passe oublié
3. Vérifier l'email reçu

## 🚨 Points Importants

### Sécurité
- Les liens expirent après 1 heure
- Un seul lien actif par utilisateur
- Validation côté serveur Firebase

### Limitations Firebase
- Pas de HTML avancé (JavaScript interdit)
- Taille limitée du template
- Variables limitées disponibles

### Bonnes Pratiques
- Tester sur différents clients email
- Vérifier les dossiers spam
- Utiliser des images hébergées (pas de pièces jointes)

## 🔄 Mise à Jour du Template

Pour modifier le template :

1. Éditer `src/services/emailService.js`
2. Copier le nouveau HTML dans Firebase Console
3. Tester avec un email de test
4. Déployer les changements

## 📧 Exemple d'Email Final

L'email final aura :
- Header bleu avec logo AnonyJud
- Message personnalisé en français
- Bouton "Réinitialiser mon mot de passe"
- Section sécurité avec conseils
- Footer avec liens vers le site
- Design responsive et professionnel

## 🆘 Dépannage

### Email non reçu
- Vérifier les spams
- Attendre 5-10 minutes
- Vérifier l'adresse email
- Réessayer la demande

### Lien expiré
- Demander un nouveau lien
- Vérifier la date/heure
- Utiliser rapidement après réception

### Erreurs courantes
- Email invalide → Vérifier le format
- Utilisateur non trouvé → Compte inexistant
- Trop de tentatives → Attendre avant réessayer

## 📝 Notes de Développement

- Le template est stocké dans `src/services/emailService.js`
- La configuration est dans Firebase Console
- Les tests se font via `/forgot-password`
- Le design suit la charte graphique AnonyJud 