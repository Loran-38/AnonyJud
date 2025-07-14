#!/usr/bin/env python3
"""
Test complet de la correction du bug de scission du prénom
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent))

from app.anonymizer import anonymize_text, anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_prenom_fix_complete():
    """Test complet de la correction du bug de scission du prénom"""
    print("🧪 Test complet de la correction du bug de scission du prénom")
    print("=" * 70)
    
    # Cas de test multiples pour vérifier la robustesse
    test_cases = [
        {
            "name": "Cas simple: HUISSOUD Louis",
            "tiers": [
                {
                    "numero": 1,
                    "nom": "HUISSOUD",
                    "prenom": "Louis",
                    "adresse": "244 Montée du Mollard"
                }
            ],
            "text": "Monsieur HUISSOUD Louis habite au 244 Montée du Mollard"
        },
        {
            "name": "Cas multiple: Plusieurs tiers",
            "tiers": [
                {
                    "numero": 1,
                    "nom": "HUISSOUD",
                    "prenom": "Louis",
                    "adresse": "244 Montée du Mollard"
                },
                {
                    "numero": 2,
                    "nom": "IMBERT", 
                    "prenom": "Arnaud",
                    "adresse": "256 Montée du Mollard"
                },
                {
                    "numero": 3,
                    "nom": "GAUTHIER",
                    "prenom": "Guylaine",
                    "adresse": "256 Montée du Mollard"
                }
            ],
            "text": """
            Demandeur: HUISSOUD Louis
            Défendeur 1: IMBERT Arnaud  
            Défendeur 2: GAUTHIER Guylaine
            """
        },
        {
            "name": "Cas piège: Mots contenant les balises",
            "tiers": [
                {
                    "numero": 1,
                    "nom": "NOM",
                    "prenom": "PRENOM",
                    "adresse": "123 Rue Test"
                }
            ],
            "text": "Monsieur NOM PRENOM habite PRENOMINAL street avec NOMINAL address"
        }
    ]
    
    all_tests_passed = True
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n🔍 Test {i}: {test_case['name']}")
        print("-" * 50)
        
        # Test d'anonymisation
        print("📝 Texte original:")
        print(test_case['text'])
        
        anonymized_text, mapping = anonymize_text(test_case['text'], test_case['tiers'])
        
        print(f"📋 Mapping: {mapping}")
        print("📝 Texte anonymisé:")
        print(anonymized_text)
        
        # Test de dé-anonymisation
        from app.deanonymizer import deanonymize_text
        deanonymized_text = deanonymize_text(anonymized_text, mapping)
        
        print("📝 Texte dé-anonymisé:")
        print(deanonymized_text)
        
        # Vérifications
        test_passed = True
        
        # Vérifier que tous les prénoms sont correctement restaurés
        for tiers in test_case['tiers']:
            prenom = tiers.get('prenom', '')
            nom = tiers.get('nom', '')
            
            if prenom and prenom not in deanonymized_text:
                print(f"❌ Prénom '{prenom}' NON restauré")
                test_passed = False
            elif prenom:
                print(f"✅ Prénom '{prenom}' correctement restauré")
            
            if nom and nom not in deanonymized_text:
                print(f"❌ Nom '{nom}' NON restauré")
                test_passed = False
            elif nom:
                print(f"✅ Nom '{nom}' correctement restauré")
        
        # Vérifier qu'il n'y a pas de concatenation incorrecte
        problematic_patterns = [
            "PREHUISSOUD", "PRENOMHUI", "LOUISHUI", "PREARNAUD", "PREGUYLAINE"
        ]
        
        for pattern in problematic_patterns:
            if pattern in deanonymized_text:
                print(f"❌ Concatenation incorrecte détectée: {pattern}")
                test_passed = False
        
        if test_passed:
            print(f"✅ Test {i} RÉUSSI")
        else:
            print(f"❌ Test {i} ÉCHOUÉ")
            all_tests_passed = False
    
    # Test PDF complet
    print(f"\n🔍 Test PDF complet")
    print("-" * 50)
    
    pdf_test_passed = test_pdf_complete()
    
    # Résumé final
    print(f"\n📊 RÉSUMÉ FINAL")
    print("=" * 70)
    
    if all_tests_passed and pdf_test_passed:
        print("🎉 TOUS LES TESTS RÉUSSIS!")
        print("✅ Le bug de scission du prénom est complètement corrigé")
        print("✅ Les expressions régulières avec limites de mots fonctionnent parfaitement")
        print("✅ Aucune concatenation incorrecte détectée")
        return True
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        if not all_tests_passed:
            print("❌ Problèmes dans les tests texte")
        if not pdf_test_passed:
            print("❌ Problèmes dans le test PDF")
        return False


def test_pdf_complete():
    """Test complet sur PDF"""
    
    # Données de test avec plusieurs tiers
    tiers_test = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "244 Montée du Mollard"
        },
        {
            "numero": 2,
            "nom": "IMBERT",
            "prenom": "Arnaud", 
            "adresse": "256 Montée du Mollard"
        },
        {
            "numero": 3,
            "nom": "GAUTHIER",
            "prenom": "Guylaine",
            "adresse": "256 Montée du Mollard"
        }
    ]
    
    # Créer un fichier PDF de test si nécessaire
    pdf_file = "test_data.pdf"
    if not os.path.exists(pdf_file):
        print("📄 Création d'un fichier PDF de test...")
        from create_test_pdf import create_test_pdf
        create_test_pdf()
    
    try:
        # Lire le fichier PDF
        with open(pdf_file, 'rb') as f:
            pdf_content = f.read()
        
        # Anonymisation PDF
        anonymized_content, mapping = anonymize_pdf_direct(pdf_content, tiers_test)
        
        # Dé-anonymisation PDF
        deanonymized_content = deanonymize_pdf_direct(anonymized_content, mapping)
        
        # Extraire le texte pour vérification
        import fitz
        
        doc_deanonymized = fitz.open(stream=deanonymized_content, filetype="pdf")
        text_deanonymized = ""
        for page in doc_deanonymized:
            text_deanonymized += page.get_text()
        doc_deanonymized.close()
        
        # Vérifications
        test_passed = True
        
        # Vérifier que tous les prénoms sont présents
        prenoms_attendus = ["Louis", "Arnaud", "Guylaine"]
        for prenom in prenoms_attendus:
            if prenom in text_deanonymized:
                print(f"✅ Prénom '{prenom}' correctement restauré dans le PDF")
            else:
                print(f"❌ Prénom '{prenom}' NON restauré dans le PDF")
                test_passed = False
        
        # Vérifier que tous les noms sont présents
        noms_attendus = ["HUISSOUD", "IMBERT", "GAUTHIER"]
        for nom in noms_attendus:
            if nom in text_deanonymized:
                print(f"✅ Nom '{nom}' correctement restauré dans le PDF")
            else:
                print(f"❌ Nom '{nom}' NON restauré dans le PDF")
                test_passed = False
        
        # Vérifier l'absence de concatenations incorrectes
        problematic_patterns = [
            "PREHUISSOUD", "PREIMBERT", "PREGAUTHIER",
            "PRENOMHUI", "PRENOMIMB", "PRENOMGAU",
            "LOUISHUISSOUD", "ARNAUDIMBERT", "GUYLAINEGAUTHIER"
        ]
        
        for pattern in problematic_patterns:
            if pattern in text_deanonymized:
                print(f"❌ Concatenation incorrecte détectée dans le PDF: {pattern}")
                test_passed = False
        
        if test_passed:
            print("✅ Test PDF complet RÉUSSI")
        
        # Sauvegarder pour inspection
        with open("test_fix_complete_anonymized.pdf", 'wb') as f:
            f.write(anonymized_content)
        
        with open("test_fix_complete_deanonymized.pdf", 'wb') as f:
            f.write(deanonymized_content)
        
        print("💾 Fichiers sauvegardés:")
        print("  - test_fix_complete_anonymized.pdf")
        print("  - test_fix_complete_deanonymized.pdf")
        
        return test_passed
        
    except Exception as e:
        print(f"❌ Erreur lors du test PDF: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_prenom_fix_complete()
    sys.exit(0 if success else 1) 