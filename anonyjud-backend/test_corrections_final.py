#!/usr/bin/env python3
"""
Test des corrections finales pour formatage, erreurs MuPDF et marges
"""

import sys
import os
sys.path.append('.')

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
import fitz
import logging

def test_corrections():
    """Test simple des corrections"""
    
    # Configuration des logs
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
    
    print("🚀 Test des corrections finales")
    
    # Créer un PDF de test simple
    doc = fitz.open()
    page = doc.new_page()
    
    # Insérer du texte simple
    page.insert_text((50, 50), "Texte normal: HUISSOUD Louis", fontname="helv", fontsize=12, color=(0, 0, 0))
    page.insert_text((50, 80), "Adresse: 61, Quai Riondet", fontname="helv", fontsize=12, color=(0, 0, 0))
    page.insert_text((400, 110), "Marge droite: HUISSOUD Louis test", fontname="helv", fontsize=12, color=(0, 0, 0))
    
    # Sauvegarder
    test_pdf_path = "test_corrections.pdf"
    doc.save(test_pdf_path)
    doc.close()
    
    # Lire le PDF
    with open(test_pdf_path, 'rb') as f:
        pdf_content = f.read()
    
    print(f"📊 PDF créé: {len(pdf_content)} bytes")
    
    # Tiers de test
    tiers = [
        {
            'numero': 1,
            'nom': 'HUISSOUD',
            'prenom': 'Louis',
            'adresse': '61, Quai Riondet',
            'customFields': []
        }
    ]
    
    try:
        # Test anonymisation
        print("\n🔒 Test anonymisation...")
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie - Mapping: {mapping}")
        
        # Sauvegarder
        with open("test_corrections_anonymized.pdf", 'wb') as f:
            f.write(anonymized_pdf)
        
        # Test dé-anonymisation
        print("\n🔓 Test dé-anonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print("✅ Dé-anonymisation réussie")
        
        # Sauvegarder
        with open("test_corrections_deanonymized.pdf", 'wb') as f:
            f.write(deanonymized_pdf)
        
        print("\n✅ Tests terminés avec succès!")
        print("📄 Fichiers créés:")
        print("- test_corrections_anonymized.pdf")
        print("- test_corrections_deanonymized.pdf")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer
        if os.path.exists(test_pdf_path):
            os.unlink(test_pdf_path)

if __name__ == "__main__":
    success = test_corrections()
    sys.exit(0 if success else 1) 