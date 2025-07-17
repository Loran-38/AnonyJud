# Instructions pour ajouter le logo Anonym-IA

## Étape 1 : Préparer votre logo
- **Nom du fichier** : `logo-anonym-ia.png` (ou `.svg`, `.jpg`)
- **Taille recommandée** : 32x32 pixels minimum, format carré de préférence
- **Format** : PNG avec fond transparent recommandé, ou SVG

## Étape 2 : Placer le logo
1. Copiez votre fichier logo dans le dossier : `anonyjud-app/public/`
2. Renommez-le exactement : `logo-anonym-ia.png`

## Étape 3 : Si vous utilisez un autre format
Si votre logo est en `.svg` ou `.jpg`, modifiez les fichiers suivants :

### Dans `anonyjud-app/src/components/Navbar.jsx` :
Remplacez `src="/logo-anonym-ia.png"` par `src="/logo-anonym-ia.svg"`

### Dans `anonyjud-app/src/components/Sidebar.jsx` :
Remplacez `src="/logo-anonym-ia.png"` par `src="/logo-anonym-ia.svg"`

## Étape 4 : Tester
1. Redémarrez le serveur de développement
2. Le logo devrait apparaître dans la barre de navigation et la sidebar
3. Si le logo ne s'affiche pas, une icône de fallback apparaîtra automatiquement

## Note
- Le code inclut déjà une gestion d'erreur qui affiche une icône par défaut si le logo n'est pas trouvé
- Assurez-vous que le nom du fichier correspond exactement à celui spécifié dans le code 