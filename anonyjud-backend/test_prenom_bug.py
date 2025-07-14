#!/usr/bin/env python3
"""
Test pour reproduire et corriger le bug de scission du prénom
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
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_prenom_bug():
    """Test pour reproduire le bug de scission du prénom"""
    print("🐛 Test du bug de scission du prénom")
    print("=" * 50)
    
    # Données de test qui reproduisent le problème
    tiers_test = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "244 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        }
    ]
    
    # Texte de test qui contient le nom et le prénom
    test_text = """
    Références des Parties
    
    Partie Demanderesse
    Demandeur 1
    Monsieur HUISSOUD Louis
    244 Montée du Mollard
    38790 CHARANTONNAY
    """
    
    print(f"📝 Texte original:")
    print(test_text)
    
    # Test d'anonymisation
    print("\n🔄 Anonymisation...")
    anonymized_text, mapping = anonymize_text(test_text, tiers_test)
    
    print(f"📋 Mapping généré: {mapping}")
    print(f"📝 Texte anonymisé:")
    print(anonymized_text)
    
    # Test de dé-anonymisation
    print("\n🔄 Dé-anonymisation...")
    from app.deanonymizer import deanonymize_text
    
    deanonymized_text = deanonymize_text(anonymized_text, mapping)
    
    print(f"📝 Texte dé-anonymisé:")
    print(deanonymized_text)
    
    # Vérifier si le bug est présent
    print("\n🔍 Vérification du bug...")
    
    # Vérifier que "Louis" est correctement restauré
    if "Louis" in deanonymized_text:
        print("✅ Prénom 'Louis' correctement restauré")
    else:
        print("❌ Prénom 'Louis' NON restauré")
    
    # Vérifier qu'il n'y a pas de concatenation incorrecte
    if "PREHUISSOUD" in deanonymized_text:
        print("❌ Bug détecté: PREHUISSOUD trouvé dans le texte")
    else:
        print("✅ Pas de concatenation incorrecte détectée")
    
    # Vérifier que HUISSOUD est correctement restauré
    if "HUISSOUD" in deanonymized_text:
        print("✅ Nom 'HUISSOUD' correctement restauré")
    else:
        print("❌ Nom 'HUISSOUD' NON restauré")
    
    # Analyser le mapping pour comprendre le problème
    print("\n🔍 Analyse du mapping:")
    for tag, value in mapping.items():
        print(f"  {tag} → {value}")
        
        # Vérifier si une balise contient une autre
        for other_tag, other_value in mapping.items():
            if tag != other_tag and other_value in value:
                print(f"  ⚠️ Conflit potentiel: '{other_value}' dans '{value}'")
    
    return deanonymized_text, mapping


def test_prenom_bug_pdf():
    """Test du bug sur un fichier PDF"""
    print("\n🐛 Test du bug de scission du prénom sur PDF")
    print("=" * 50)
    
    # Données de test
    tiers_test = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "244 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
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
        
        print(f"📄 Fichier PDF lu: {len(pdf_content)} bytes")
        
        # Test d'anonymisation PDF
        print("\n🔄 Anonymisation PDF...")
        anonymized_content, mapping = anonymize_pdf_direct(pdf_content, tiers_test)
        
        print(f"📋 Mapping généré: {mapping}")
        
        # Test de dé-anonymisation PDF
        print("\n🔄 Dé-anonymisation PDF...")
        deanonymized_content = deanonymize_pdf_direct(anonymized_content, mapping)
        
        # Extraire le texte pour vérification
        import fitz
        
        # Texte dé-anonymisé
        doc_deanonymized = fitz.open(stream=deanonymized_content, filetype="pdf")
        text_deanonymized = ""
        for page in doc_deanonymized:
            text_deanonymized += page.get_text()
        doc_deanonymized.close()
        
        print(f"📝 Texte dé-anonymisé extrait:")
        print(text_deanonymized[:500])
        
        # Vérifier le bug
        print("\n🔍 Vérification du bug sur PDF...")
        
        if "Louis" in text_deanonymized:
            print("✅ Prénom 'Louis' correctement restauré dans le PDF")
        else:
            print("❌ Prénom 'Louis' NON restauré dans le PDF")
        
        if "PREHUISSOUD" in text_deanonymized:
            print("❌ Bug détecté dans le PDF: PREHUISSOUD trouvé")
        else:
            print("✅ Pas de concatenation incorrecte dans le PDF")
        
        if "HUISSOUD" in text_deanonymized:
            print("✅ Nom 'HUISSOUD' correctement restauré dans le PDF")
        else:
            print("❌ Nom 'HUISSOUD' NON restauré dans le PDF")
        
        # Sauvegarder pour inspection visuelle
        with open("test_bug_prenom_anonymized.pdf", 'wb') as f:
            f.write(anonymized_content)
        
        with open("test_bug_prenom_deanonymized.pdf", 'wb') as f:
            f.write(deanonymized_content)
        
        print("\n💾 Fichiers sauvegardés:")
        print("  - test_bug_prenom_anonymized.pdf")
        print("  - test_bug_prenom_deanonymized.pdf")
        
        return text_deanonymized, mapping
        
    except Exception as e:
        print(f"❌ Erreur lors du test PDF: {str(e)}")
        import traceback
        traceback.print_exc()
        return None, None


if __name__ == "__main__":
    print("🧪 Test du bug de scission du prénom")
    print("=" * 60)
    
    # Test sur texte simple
    deanonymized_text, mapping = test_prenom_bug()
    
    # Test sur PDF
    pdf_text, pdf_mapping = test_prenom_bug_pdf()
    
    print("\n📊 Résumé des tests:")
    print("=" * 60)
    print("Les tests ci-dessus permettent de reproduire le bug de scission du prénom.")
    print("Si le bug est présent, vous verrez 'PREHUISSOUD' au lieu de 'Louis'.")
    print("La correction nécessite l'utilisation d'expressions régulières avec limites de mots.") 