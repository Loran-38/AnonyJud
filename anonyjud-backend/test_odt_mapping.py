#!/usr/bin/env python3
"""
Test pour vérifier le mapping des fichiers ODT
"""

import os
import tempfile
from odf.opendocument import OpenDocumentText
from odf.text import P
from odf.style import Style, TextProperties, ParagraphProperties
from odf import text as odf_text, teletype
from odf.opendocument import load

# Importer les fonctions depuis notre app
from app.anonymizer import anonymize_text
from app.deanonymizer import deanonymize_text

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
    return temp_path

def read_odt_text(file_path):
    """Lire le texte d'un fichier ODT"""
    doc = load(file_path)
    text = ""
    for paragraph in doc.getElementsByType(odf_text.P):
        text += teletype.extractText(paragraph) + "\n"
    return text.strip()

def test_odt_mapping():
    """Test principal pour vérifier le mapping ODT"""
    
    print("🚀 Test du mapping ODT - Début")
    
    # Créer un fichier ODT de test
    test_file = create_test_odt_file()
    print(f"📁 Fichier ODT de test créé: {test_file}")
    
    try:
        # Lire le contenu original
        original_text = read_odt_text(test_file)
        print(f"📝 Texte original:")
        print(original_text)
        print("-" * 50)
        
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
        
        # Test 1: Anonymisation du texte
        print("\n🔄 Test 1: Anonymisation du texte")
        anonymized_text, mapping = anonymize_text(original_text, tiers)
        
        print(f"📝 Texte anonymisé:")
        print(anonymized_text)
        print(f"🗂️ Mapping généré:")
        for key, value in mapping.items():
            print(f"  {key} -> {value}")
        
        # Vérifications de l'anonymisation
        print("\n✅ Vérifications de l'anonymisation:")
        
        # Vérifier que les noms sont anonymisés
        if "HUISSOUD" not in anonymized_text:
            print("  ✅ Nom HUISSOUD correctement anonymisé")
        else:
            print("  ❌ Nom HUISSOUD toujours présent")
        
        if "Louis" not in anonymized_text:
            print("  ✅ Prénom Louis correctement anonymisé")
        else:
            print("  ❌ Prénom Louis toujours présent")
        
        if "MARTIN" not in anonymized_text:
            print("  ✅ Nom MARTIN correctement anonymisé")
        else:
            print("  ❌ Nom MARTIN toujours présent")
        
        if "Sophie" not in anonymized_text:
            print("  ✅ Prénom Sophie correctement anonymisé")
        else:
            print("  ❌ Prénom Sophie toujours présent")
        
        # Vérifier que les balises sont présentes
        expected_tags = ["NOM1", "PRENOM1", "NOM2", "PRENOM2", "ADRESSE1", "ADRESSE2", "TELEPHONE1", "TELEPHONE2", "EMAIL1"]
        for tag in expected_tags:
            if tag in anonymized_text:
                print(f"  ✅ Balise {tag} présente")
            else:
                print(f"  ❌ Balise {tag} manquante")
        
        # Test 2: Dé-anonymisation du texte
        print("\n🔄 Test 2: Dé-anonymisation du texte")
        deanonymized_text = deanonymize_text(anonymized_text, mapping)
        
        print(f"📝 Texte dé-anonymisé:")
        print(deanonymized_text)
        
        # Vérifications de la dé-anonymisation
        print("\n✅ Vérifications de la dé-anonymisation:")
        
        # Vérifier que les noms sont restaurés
        if "HUISSOUD" in deanonymized_text:
            print("  ✅ Nom HUISSOUD correctement restauré")
        else:
            print("  ❌ Nom HUISSOUD non restauré")
        
        if "Louis" in deanonymized_text:
            print("  ✅ Prénom Louis correctement restauré")
        else:
            print("  ❌ Prénom Louis non restauré")
        
        if "MARTIN" in deanonymized_text:
            print("  ✅ Nom MARTIN correctement restauré")
        else:
            print("  ❌ Nom MARTIN non restauré")
        
        if "Sophie" in deanonymized_text:
            print("  ✅ Prénom Sophie correctement restauré")
        else:
            print("  ❌ Prénom Sophie non restauré")
        
        # Vérifier qu'aucune balise ne reste
        remaining_tags = []
        for tag in expected_tags:
            if tag in deanonymized_text:
                remaining_tags.append(tag)
        
        if not remaining_tags:
            print("  ✅ Aucune balise résiduelle")
        else:
            print(f"  ❌ Balises résiduelles: {remaining_tags}")
        
        # Test 3: Comparaison avec l'original
        print("\n🔄 Test 3: Comparaison avec l'original")
        
        # Nettoyer les textes pour la comparaison (supprimer les espaces en trop)
        original_clean = " ".join(original_text.split())
        deanonymized_clean = " ".join(deanonymized_text.split())
        
        if original_clean == deanonymized_clean:
            print("  ✅ Texte parfaitement restauré")
        else:
            print("  ❌ Différences détectées")
            print(f"    Original: {original_clean}")
            print(f"    Restauré: {deanonymized_clean}")
        
        # Test 4: Vérification du mapping
        print("\n🔄 Test 4: Vérification du mapping")
        
        # Vérifier que le mapping utilise les bons numéros
        expected_mapping = {
            "NOM1": "HUISSOUD",
            "PRENOM1": "Louis",
            "ADRESSE1": "123 Rue de la Paix",
            "TELEPHONE1": "01.23.45.67.89",
            "EMAIL1": "louis.huissoud@example.com",
            "NOM2": "MARTIN",
            "PRENOM2": "Sophie",
            "ADRESSE2": "456 Avenue des Fleurs",
            "TELEPHONE2": "06.11.22.33.44"
        }
        
        mapping_ok = True
        for key, expected_value in expected_mapping.items():
            if key in mapping:
                if mapping[key] == expected_value:
                    print(f"  ✅ {key} -> {expected_value}")
                else:
                    print(f"  ❌ {key} -> {mapping[key]} (attendu: {expected_value})")
                    mapping_ok = False
            else:
                print(f"  ❌ {key} manquant dans le mapping")
                mapping_ok = False
        
        if mapping_ok:
            print("  ✅ Mapping conforme aux attentes")
        else:
            print("  ❌ Problèmes détectés dans le mapping")
        
        print("\n🎉 Test terminé avec succès!")
        
    finally:
        # Nettoyer le fichier temporaire
        if os.path.exists(test_file):
            os.unlink(test_file)
            print(f"🧹 Fichier temporaire supprimé: {test_file}")

if __name__ == "__main__":
    test_odt_mapping() 