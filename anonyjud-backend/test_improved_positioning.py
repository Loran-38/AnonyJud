#!/usr/bin/env python3
"""
Test du positionnement amélioré pour l'anonymisation PDF directe
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_improved_positioning():
    """Test l'amélioration du positionnement du texte"""
    print("🧪 Test du positionnement amélioré pour l'anonymisation PDF directe")
    print("=" * 70)
    
    # Données de test
    tiers_test = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "244 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        },
        {
            "numero": 2,
            "nom": "IMBERT",
            "prenom": "Arnaud",
            "adresse": "256 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        },
        {
            "numero": 3,
            "nom": "GAUTHIER",
            "prenom": "Guylaine",
            "adresse": "256 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        }
    ]
    
    # Chercher un fichier PDF de test
    test_files = [
        "test_data.pdf",
        "document_test.pdf",
        "sample.pdf"
    ]
    
    pdf_file = None
    for filename in test_files:
        if os.path.exists(filename):
            pdf_file = filename
            break
    
    if not pdf_file:
        print("❌ Aucun fichier PDF de test trouvé")
        print("Créez un fichier PDF de test avec du texte contenant les noms/prénoms des tiers")
        return False
    
    print(f"📄 Fichier de test: {pdf_file}")
    
    try:
        # Lire le fichier PDF
        with open(pdf_file, 'rb') as f:
            pdf_content = f.read()
        
        print(f"📊 Taille du PDF original: {len(pdf_content)} bytes")
        
        # Test d'anonymisation avec positionnement amélioré
        print("\n🔄 Anonymisation avec positionnement amélioré...")
        anonymized_content, mapping = anonymize_pdf_direct(pdf_content, tiers_test)
        
        print(f"📊 Taille du PDF anonymisé: {len(anonymized_content)} bytes")
        print(f"🏷️  Nombre de balises générées: {len(mapping)}")
        
        # Afficher les balises générées
        print("\n📋 Balises d'anonymisation générées:")
        for original, anonymized in mapping.items():
            print(f"  • '{original}' → '{anonymized}'")
        
        # Sauvegarder le PDF anonymisé
        anonymized_file = "test_anonymized_improved.pdf"
        with open(anonymized_file, 'wb') as f:
            f.write(anonymized_content)
        print(f"💾 PDF anonymisé sauvegardé: {anonymized_file}")
        
        # Test de dé-anonymisation
        print("\n🔄 Dé-anonymisation...")
        deanonymized_content = deanonymize_pdf_direct(anonymized_content, mapping)
        
        print(f"📊 Taille du PDF dé-anonymisé: {len(deanonymized_content)} bytes")
        
        # Sauvegarder le PDF dé-anonymisé
        deanonymized_file = "test_deanonymized_improved.pdf"
        with open(deanonymized_file, 'wb') as f:
            f.write(deanonymized_content)
        print(f"💾 PDF dé-anonymisé sauvegardé: {deanonymized_file}")
        
        # Vérification du contenu
        print("\n🔍 Vérification du contenu...")
        
        # Extraire le texte pour vérification
        try:
            import fitz
            
            # Texte original
            doc_original = fitz.open(stream=pdf_content, filetype="pdf")
            text_original = ""
            for page in doc_original:
                text_original += page.get_text()
            doc_original.close()
            
            # Texte anonymisé
            doc_anonymized = fitz.open(stream=anonymized_content, filetype="pdf")
            text_anonymized = ""
            for page in doc_anonymized:
                text_anonymized += page.get_text()
            doc_anonymized.close()
            
            # Texte dé-anonymisé
            doc_deanonymized = fitz.open(stream=deanonymized_content, filetype="pdf")
            text_deanonymized = ""
            for page in doc_deanonymized:
                text_deanonymized += page.get_text()
            doc_deanonymized.close()
            
            # Vérifier que les balises sont présentes dans le texte anonymisé
            balises_trouvees = 0
            for balise in mapping.values():
                if balise in text_anonymized:
                    balises_trouvees += 1
            
            print(f"✅ {balises_trouvees}/{len(mapping)} balises trouvées dans le texte anonymisé")
            
            # Vérifier que les valeurs originales sont restaurées
            valeurs_restaurees = 0
            for original_value in mapping.keys():
                if original_value in text_deanonymized:
                    valeurs_restaurees += 1
            
            print(f"✅ {valeurs_restaurees}/{len(mapping)} valeurs restaurées dans le texte dé-anonymisé")
            
            # Afficher des extraits pour vérification visuelle
            print("\n📝 Extraits de texte (premiers 200 caractères):")
            print(f"Original: {text_original[:200]}...")
            print(f"Anonymisé: {text_anonymized[:200]}...")
            print(f"Dé-anonymisé: {text_deanonymized[:200]}...")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification du contenu: {str(e)}")
        
        print("\n🎯 Test du positionnement amélioré terminé!")
        print("📋 Vérifiez visuellement les fichiers générés:")
        print(f"   • {anonymized_file} (anonymisé)")
        print(f"   • {deanonymized_file} (dé-anonymisé)")
        print("   • Le texte doit être correctement aligné sans décalages")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_improved_positioning()
    sys.exit(0 if success else 1) 