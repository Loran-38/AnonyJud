#!/usr/bin/env python3
"""
Test simple des corrections d'anonymisation PDF
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct, anonymize_text
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_text_anonymization():
    """Test simple de l'anonymisation de texte"""
    print("🧪 === TEST SIMPLE D'ANONYMISATION DE TEXTE ===")
    
    # Texte de test
    text = """
    Texte normal: HUISSOUD Louis habitant 123 rue de la Paix
    Texte gras: IMBERT Arnaud habitant 456 avenue Victor Hugo
    Texte couleur: GAUTHIER Guylaine habitant 789 boulevard Saint-Michel
    Texte marge droite: MARTIN Jean-Pierre habitant 654 avenue de la République avec une adresse très longue
    Caractères spéciaux: FRANÇOIS Marie-Hélène habitant 987 rue du Commerce
    """
    
    # Tiers de test
    tiers = [
        {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
        {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"},
        {"numero": 3, "nom": "GAUTHIER", "prenom": "Guylaine", "adresse": "789 boulevard Saint-Michel"},
        {"numero": 5, "nom": "MARTIN", "prenom": "Jean-Pierre", "adresse": "654 avenue de la République"},
        {"numero": 6, "nom": "FRANÇOIS", "prenom": "Marie-Hélène", "adresse": "987 rue du Commerce"}
    ]
    
    print(f"📝 Texte original:")
    print(text)
    print(f"👥 Tiers: {len(tiers)} personnes")
    
    # Test d'anonymisation
    print("\n🔒 Test d'anonymisation...")
    try:
        anonymized_text, mapping = anonymize_text(text, tiers)
        print(f"✅ Anonymisation réussie")
        print(f"📝 Texte anonymisé:")
        print(anonymized_text)
        print(f"📊 Mapping: {mapping}")
        
        # Test de déanonymisation
        print("\n🔓 Test de déanonymisation...")
        deanonymized_text = anonymized_text
        
        # Appliquer le mapping inverse
        for tag, original_value in mapping.items():
            if tag in deanonymized_text:
                deanonymized_text = deanonymized_text.replace(tag, original_value)
                print(f"🔄 Remplacé {tag} par {original_value}")
        
        print(f"✅ Déanonymisation réussie")
        print(f"📝 Texte déanonymisé:")
        print(deanonymized_text)
        
        # Vérifier que tous les noms sont bien restaurés
        print("\n🔍 Vérification des restaurations:")
        for tiers_item in tiers:
            nom = tiers_item["nom"]
            prenom = tiers_item["prenom"]
            adresse = tiers_item["adresse"]
            
            nom_found = nom in deanonymized_text
            prenom_found = prenom in deanonymized_text
            adresse_found = adresse in deanonymized_text
            
            print(f"  👤 {nom} {prenom}: Nom={nom_found}, Prénom={prenom_found}, Adresse={adresse_found}")
            
            if not (nom_found and prenom_found and adresse_found):
                print(f"    ⚠️ Problème de restauration pour {nom} {prenom}")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_mapping_logic():
    """Test de la logique de mapping"""
    print("\n🧪 === TEST DE LA LOGIQUE DE MAPPING ===")
    
    # Test simple
    text = "HUISSOUD Louis IMBERT Arnaud GAUTHIER Guylaine"
    tiers = [
        {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
        {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"},
        {"numero": 3, "nom": "GAUTHIER", "prenom": "Guylaine", "adresse": "789 boulevard Saint-Michel"}
    ]
    
    anonymized_text, mapping = anonymize_text(text, tiers)
    
    print(f"📝 Texte original: {text}")
    print(f"📝 Texte anonymisé: {anonymized_text}")
    print(f"📊 Mapping: {mapping}")
    
    # Vérifier que le mapping est cohérent [[memory:2869951]]
    expected_mappings = []
    for tiers_item in tiers:
        numero = tiers_item["numero"]
        expected_mappings.extend([
            f"NOM{numero}",
            f"PRENOM{numero}",
            f"ADRESSE{numero}"
        ])
    
    print(f"📊 Mappings attendus: {expected_mappings}")
    
    # Vérifier que tous les mappings attendus sont présents
    for expected in expected_mappings:
        if expected in mapping:
            print(f"  ✅ {expected} trouvé: {mapping[expected]}")
        else:
            print(f"  ❌ {expected} manquant")

if __name__ == "__main__":
    test_text_anonymization()
    test_mapping_logic() 