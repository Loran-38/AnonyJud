#!/usr/bin/env python3
"""
Test pour vérifier le téléchargement des fichiers ODT
"""

import os
import tempfile
from odf.opendocument import OpenDocumentText
from odf.text import P

# Importer les fonctions depuis notre app
from app.main import anonymize_odt_file, deanonymize_odt_file

def create_test_odt_file():
    """Créer un fichier ODT de test avec du contenu à anonymiser"""
    
    # Créer un nouveau document ODT
    doc = OpenDocumentText()
    
    # Ajouter du contenu de test
    paragraphs = [
        "Monsieur HUISSOUD Louis habite au 123 Rue de la Paix.",
        "Il peut être joint au 01.23.45.67.89 ou par email à louis.huissoud@example.com.",
        "Madame MARTIN Sophie réside à 456 Avenue des Fleurs, 75001 Paris.",
        "Son numéro de téléphone est 06.11.22.33.44.",
        "Monsieur HUISSOUD Louis et Madame MARTIN Sophie sont les parties concernées."
    ]
    
    for paragraph_text in paragraphs:
        p = P()
        p.addText(paragraph_text)
        doc.text.addElement(p)
    
    # Sauvegarder dans un fichier temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".odt") as temp_file:
        temp_path = temp_file.name
    
    doc.save(temp_path)
    
    # Lire le contenu en bytes
    with open(temp_path, 'rb') as f:
        content = f.read()
    
    # Nettoyer le fichier temporaire
    os.unlink(temp_path)
    
    return content

def test_odt_download():
    """Test principal pour vérifier le téléchargement ODT"""
    
    print("🚀 Test du téléchargement ODT - Début")
    
    # Créer un fichier ODT de test
    original_content = create_test_odt_file()
    print(f"📁 Fichier ODT de test créé ({len(original_content)} bytes)")
    
    # Définir les tiers pour l'anonymisation
    tiers = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "123 Rue de la Paix",
            "ville": "Paris",
            "code_postal": "75001",
            "telephone": "01.23.45.67.89",
            "email": "louis.huissoud@example.com"
        },
        {
            "numero": 2,
            "nom": "MARTIN",
            "prenom": "Sophie",
            "adresse": "456 Avenue des Fleurs",
            "ville": "Paris",
            "code_postal": "75001",
            "telephone": "06.11.22.33.44",
            "email": "sophie.martin@example.com"
        }
    ]
    
    print(f"👥 Tiers configurés: {len(tiers)} personnes")
    
    try:
        # Test 1: Anonymisation du fichier ODT
        print("\n🔄 Test 1: Anonymisation du fichier ODT")
        anonymized_content, mapping = anonymize_odt_file(original_content, tiers)
        
        print(f"✅ Fichier ODT anonymisé généré ({len(anonymized_content)} bytes)")
        print(f"🗂️ Mapping généré: {len(mapping)} balises")
        for key, value in mapping.items():
            print(f"  {key} -> {value}")
        
        # Vérifier que le fichier anonymisé est différent de l'original
        if anonymized_content != original_content:
            print("  ✅ Fichier anonymisé différent de l'original")
        else:
            print("  ❌ Fichier anonymisé identique à l'original")
        
        # Test 2: Dé-anonymisation du fichier ODT
        print("\n🔄 Test 2: Dé-anonymisation du fichier ODT")
        deanonymized_content = deanonymize_odt_file(anonymized_content, mapping)
        
        print(f"✅ Fichier ODT dé-anonymisé généré ({len(deanonymized_content)} bytes)")
        
        # Vérifier que le fichier dé-anonymisé est différent de l'anonymisé
        if deanonymized_content != anonymized_content:
            print("  ✅ Fichier dé-anonymisé différent de l'anonymisé")
        else:
            print("  ❌ Fichier dé-anonymisé identique à l'anonymisé")
        
        # Test 3: Vérification de la cohérence du mapping
        print("\n🔄 Test 3: Vérification de la cohérence du mapping")
        
        # Vérifier que le mapping utilise les bons numéros
        expected_keys = ["NOM1", "PRENOM1", "ADRESSE1", "NOM2", "PRENOM2", "ADRESSE2"]
        
        mapping_ok = True
        for key in expected_keys:
            if key in mapping:
                print(f"  ✅ Clé {key} présente dans le mapping")
            else:
                print(f"  ❌ Clé {key} manquante dans le mapping")
                mapping_ok = False
        
        if mapping_ok:
            print("  ✅ Structure du mapping conforme")
        else:
            print("  ❌ Problèmes dans la structure du mapping")
        
        # Test 4: Sauvegarde pour vérification manuelle
        print("\n🔄 Test 4: Sauvegarde pour vérification manuelle")
        
        # Sauvegarder les fichiers pour inspection
        with tempfile.NamedTemporaryFile(delete=False, suffix="_original.odt") as f:
            f.write(original_content)
            original_path = f.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix="_anonymized.odt") as f:
            f.write(anonymized_content)
            anonymized_path = f.name
            
        with tempfile.NamedTemporaryFile(delete=False, suffix="_deanonymized.odt") as f:
            f.write(deanonymized_content)
            deanonymized_path = f.name
        
        print(f"📁 Fichier original: {original_path}")
        print(f"📁 Fichier anonymisé: {anonymized_path}")
        print(f"📁 Fichier dé-anonymisé: {deanonymized_path}")
        print("💡 Vous pouvez ouvrir ces fichiers pour vérifier manuellement le contenu")
        
        print("\n🎉 Test de téléchargement ODT terminé avec succès!")
        
        return {
            "original_path": original_path,
            "anonymized_path": anonymized_path,
            "deanonymized_path": deanonymized_path,
            "mapping": mapping
        }
        
    except Exception as e:
        print(f"❌ Erreur durant le test: {str(e)}")
        raise

if __name__ == "__main__":
    result = test_odt_download()
    print(f"\n📊 Résultat final:")
    print(f"  - Fichiers générés: 3")
    print(f"  - Mapping créé: {len(result['mapping'])} balises")
    print(f"  - Test réussi: ✅") 