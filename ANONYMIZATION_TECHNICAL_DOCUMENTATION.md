# Documentation technique - Onglet Anonymiser

## Vue d'ensemble

L'onglet anonymiser permet de traiter des textes et documents Word (.docx) pour remplacer les informations personnelles par des balises anonymisées, puis de les dé-anonymiser en restaurant les données originales.

## Architecture générale

### Frontend (React)
- **Composant principal** : `AnonymizationPanel.jsx`
- **Localisation** : `anonyjud-app/src/components/AnonymizationPanel.jsx`
- **Responsabilités** : Interface utilisateur, gestion des fichiers, appels API

### Backend (FastAPI)
- **Fichier principal** : `main.py`
- **Modules spécialisés** : `anonymizer.py`, `deanonymizer.py`, `models.py`
- **Localisation** : `anonyjud-backend/app/`
- **Responsabilités** : Traitement des données, logique métier, gestion des fichiers

## Fonctionnement Frontend

### Structure du composant AnonymizationPanel

```jsx
// État principal
const [tiers, setTiers] = useState([]);
const [anonymizedText, setAnonymizedText] = useState('');
const [deanonymizedText, setDeanonymizedText] = useState('');
const [manualText, setManualText] = useState('');
const [anonymizedManualText, setAnonymizedManualText] = useState('');
```

### Zones d'interface

1. **Zone d'anonymisation (bleue)**
   - Drag & drop pour fichiers Word
   - Textarea pour texte manuel
   - Bouton "Anonymiser"
   - Zone de résultat d'anonymisation

2. **Zone de dé-anonymisation (verte)**
   - Drag & drop pour fichiers Word anonymisés
   - Textarea pour texte anonymisé
   - Bouton "Dé-anonymiser"
   - Zone de résultat de dé-anonymisation

### Gestion des fichiers (Drag & Drop)

```jsx
const handleFileDrop = (acceptedFiles, isForDeanonymization = false) => {
  const file = acceptedFiles[0];
  if (file && file.name.endsWith('.docx')) {
    if (isForDeanonymization) {
      handleDeanonymizeFile(file);
    } else {
      handleAnonymizeFile(file);
    }
  }
};
```

### Appels API

#### Anonymisation de texte
```jsx
const handleAnonymizeText = async () => {
  const response = await fetch(`${API_BASE_URL}/anonymize-text`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text: manualText,
      tiers: tiers
    })
  });
};
```

#### Anonymisation de fichier Word
```jsx
const handleAnonymizeFile = async (file) => {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('tiers', JSON.stringify(tiers));
  
  const response = await fetch(`${API_BASE_URL}/anonymize-docx`, {
    method: 'POST',
    body: formData
  });
};
```

## Fonctionnement Backend

### Modèles de données (models.py)

```python
class TiersModel(BaseModel):
    numero: int
    nom: str
    prenom: str
    adresse: str
    ville: str
    code_postal: str
    telephone: str
    email: str

class AnonymizeTextRequest(BaseModel):
    text: str
    tiers: List[TiersModel]
```

### Endpoints API (main.py)

#### POST /anonymize-text
- **Entrée** : Texte + liste des tiers
- **Sortie** : Texte anonymisé + mapping des remplacements
- **Traitement** : Appel à `anonymize_text()` du module `anonymizer`

#### POST /anonymize-docx
- **Entrée** : Fichier Word + liste des tiers (FormData)
- **Sortie** : Fichier Word anonymisé + mapping
- **Traitement** : Appel à `anonymize_docx_file()` du module `anonymizer`

#### POST /deanonymize-text
- **Entrée** : Texte anonymisé + mapping des remplacements
- **Sortie** : Texte dé-anonymisé
- **Traitement** : Appel à `deanonymize_text()` du module `deanonymizer`

#### POST /deanonymize-docx
- **Entrée** : Fichier Word anonymisé + mapping
- **Sortie** : Fichier Word dé-anonymisé
- **Traitement** : Appel à `deanonymize_docx_file()` du module `deanonymizer`

### Module d'anonymisation (anonymizer.py)

#### Fonction `anonymize_text(text, tiers)`

```python
def anonymize_text(text: str, tiers: List[dict]) -> Tuple[str, dict]:
    """
    Anonymise un texte en remplaçant les informations personnelles par des balises
    
    Args:
        text: Texte à anonymiser
        tiers: Liste des tiers avec leurs informations
        
    Returns:
        Tuple (texte_anonymisé, mapping_des_remplacements)
    """
```

**Logique de traitement :**
1. Parcours de chaque tiers dans la liste
2. Remplacement des informations personnelles par des balises :
   - `nom` → `NOM{numero}`
   - `prenom` → `PRENOM{numero}`
   - `adresse` → `ADRESSE{numero}`
   - etc.
3. Création d'un mapping pour la dé-anonymisation
4. Utilisation d'expressions régulières pour les remplacements précis

#### Fonction `anonymize_docx_file(file_path, tiers)`

```python
def anonymize_docx_file(file_path: str, tiers: List[dict]) -> Tuple[str, dict]:
    """
    Anonymise un fichier Word (.docx) en préservant le formatage
    
    Args:
        file_path: Chemin vers le fichier Word
        tiers: Liste des tiers avec leurs informations
        
    Returns:
        Tuple (chemin_fichier_anonymisé, mapping_des_remplacements)
    """
```

**Logique de traitement :**
1. Ouverture du document Word avec `python-docx`
2. Parcours de tous les paragraphes
3. Pour chaque paragraphe, traitement des "runs" (portions de texte avec formatage)
4. Remplacement des informations tout en préservant le formatage original
5. Sauvegarde du document anonymisé

### Module de dé-anonymisation (deanonymizer.py)

#### Fonction `deanonymize_text(text, mapping)`

```python
def deanonymize_text(text: str, mapping: dict) -> str:
    """
    Dé-anonymise un texte en restaurant les informations originales
    
    Args:
        text: Texte anonymisé
        mapping: Mapping des remplacements (balise → valeur originale)
        
    Returns:
        Texte dé-anonymisé
    """
```

**Logique de traitement :**
1. Tri des balises par longueur décroissante (évite les remplacements partiels)
2. Utilisation d'expressions régulières avec limites de mots (`\b`)
3. Remplacement sécurisé : `PRENOM1` traité avant `NOM1`
4. Fallback avec remplacement simple si regex échoue

#### Fonction `deanonymize_docx_file(file_path, mapping)`

```python
def deanonymize_docx_file(file_path: str, mapping: dict) -> str:
    """
    Dé-anonymise un fichier Word en préservant le formatage
    
    Args:
        file_path: Chemin vers le fichier Word anonymisé
        mapping: Mapping des remplacements
        
    Returns:
        Chemin vers le fichier dé-anonymisé
    """
```

**Logique de traitement :**
1. Ouverture du document Word anonymisé
2. Parcours de tous les paragraphes et runs
3. Application des mêmes règles de remplacement que pour le texte
4. Préservation du formatage original (police, style, couleur)
5. Sauvegarde du document dé-anonymisé

## Gestion des erreurs et sécurité

### Validation des données
- Validation des modèles Pydantic côté backend
- Vérification des types de fichiers (.docx uniquement)
- Validation de la structure des tiers

### Sécurité RGPD
- Aucune sauvegarde permanente des données personnelles
- Traitement en mémoire uniquement
- Suppression automatique des fichiers temporaires
- Chiffrement des communications (HTTPS)

### Gestion des erreurs
- Try-catch sur tous les appels API
- Messages d'erreur explicites pour l'utilisateur
- Logs détaillés côté backend pour le débogage

## Conformité à la numérotation des tiers

Le système utilise le champ `numero` fixe de chaque tiers pour maintenir la cohérence :

```python
# Exemple de mapping
mapping = {
    "NOM3": "HUISSOUD",
    "PRENOM3": "Louis",
    "ADRESSE3": "123 Rue de la Paix"
}
```

Cette approche garantit que :
- Le tiers affiché comme "3" produit des balises `nom3`, `prenom3`, etc.
- La numérotation reste cohérente même après suppression d'autres tiers
- La dé-anonymisation fonctionne correctement avec les bons mappings

## Flux de données complet

### Anonymisation
1. **Frontend** : Utilisateur saisit texte/fichier + configure tiers
2. **API** : Envoi des données vers `/anonymize-text` ou `/anonymize-docx`
3. **Backend** : Traitement par `anonymizer.py`
4. **Retour** : Texte/fichier anonymisé + mapping
5. **Frontend** : Affichage du résultat + stockage du mapping

### Dé-anonymisation
1. **Frontend** : Utilisateur fournit texte/fichier anonymisé
2. **API** : Envoi vers `/deanonymize-text` ou `/deanonymize-docx` avec mapping
3. **Backend** : Traitement par `deanonymizer.py`
4. **Retour** : Texte/fichier dé-anonymisé
5. **Frontend** : Affichage du résultat restauré

## Technologies utilisées

### Frontend
- **React** : Framework principal
- **JavaScript** : Langage de programmation
- **Fetch API** : Communication avec le backend
- **File API** : Gestion des fichiers drag & drop

### Backend
- **FastAPI** : Framework web Python
- **Pydantic** : Validation des données
- **python-docx** : Manipulation des fichiers Word
- **Uvicorn** : Serveur ASGI

## Déploiement

### Frontend
- **Plateforme** : Railway
- **Build** : Create React App
- **Commande** : `npm run build`

### Backend
- **Plateforme** : Railway
- **Runtime** : Python 3.9+
- **Commande** : `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Maintenance et évolution

### Points d'attention
- Mise à jour des dépendances (sécurité)
- Tests de régression sur les formats Word
- Optimisation des performances pour gros fichiers
- Amélioration de la gestion d'erreurs

### Possibles améliorations
- Support d'autres formats (PDF, ODT)
- Anonymisation par IA/NLP
- Interface de prévisualisation
- Historique des anonymisations 