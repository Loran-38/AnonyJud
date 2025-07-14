#!/usr/bin/env python3
"""
Script de diagnostic pour les problèmes de formatage et erreurs MuPDF
"""

import sys
import os
sys.path.append('.')

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
import fitz
import logging

def test_formatage_debug():
    """Test détaillé du formatage et diagnostic des erreurs"""
    
    # Configuration des logs
    logging.basicConfig(level=logging.DEBUG, format='%(levelname)s: %(message)s')
    
    # Créer un PDF de test simple avec formatage
    print("🚀 Création d'un PDF de test avec formatage...")
    
    doc = fitz.open()
    page = doc.new_page()
    
    # Insérer du texte avec différents formatages
    try:
        # Texte normal
        page.insert_text((50, 50), "Texte normal: HUISSOUD Louis", fontname="helv", fontsize=12, color=(0, 0, 0))
        
        # Texte en gras
        page.insert_text((50, 80), "Texte gras: HUISSOUD Louis", fontname="helv-bold", fontsize=12, color=(0, 0, 0))
        
        # Texte en couleur
        page.insert_text((50, 110), "Texte couleur: HUISSOUD Louis", fontname="helv", fontsize=12, color=(0, 0, 1))
        
        # Texte avec descenders
        page.insert_text((50, 140), "Descenders: gjpqy HUISSOUD Louis", fontname="helv", fontsize=12, color=(0, 0, 0))
        
        # Test des marges - texte près du bord droit
        page.insert_text((400, 170), "Marge droite: HUISSOUD Louis test long texte", fontname="helv", fontsize=12, color=(0, 0, 0))
        
    except Exception as e:
        print(f"❌ Erreur création PDF: {e}")
        return False
    
    # Sauvegarder le PDF de test
    test_pdf_path = "test_formatage_debug.pdf"
    doc.save(test_pdf_path)
    doc.close()
    
    print(f"✅ PDF de test créé: {test_pdf_path}")
    
    # Lire le PDF créé
    with open(test_pdf_path, 'rb') as f:
        pdf_content = f.read()
    
    print(f"📊 Taille PDF original: {len(pdf_content)} bytes")
    
    # Analyser le contenu du PDF avant anonymisation
    print("\n🔍 ANALYSE DU PDF ORIGINAL:")
    doc = fitz.open(stream=pdf_content, filetype="pdf")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        print(f"\n📄 Page {page_num + 1}:")
        
        # Obtenir les informations détaillées sur les blocs de texte
        text_blocks = page.get_text("dict")
        
        for block_num, block in enumerate(text_blocks["blocks"]):
            if "lines" in block:
                print(f"  📦 Bloc {block_num}:")
                for line_num, line in enumerate(block["lines"]):
                    print(f"    📝 Ligne {line_num}:")
                    for span_num, span in enumerate(line["spans"]):
                        print(f"      🔤 Span {span_num}:")
                        print(f"        Texte: '{span['text']}'")
                        print(f"        Police: {span['font']}")
                        print(f"        Taille: {span['size']}")
                        print(f"        Flags: {span['flags']} (binaire: {bin(span['flags'])})")
                        print(f"        Couleur: {span['color']}")
                        print(f"        BBox: {span['bbox']}")
    
    doc.close()
    
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
    
    print("\n🚀 TEST ANONYMISATION:")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie")
        print(f"📊 Mapping: {mapping}")
        
        # Sauvegarder le PDF anonymisé
        with open("test_formatage_debug_anonymized.pdf", 'wb') as f:
            f.write(anonymized_pdf)
        
        print("\n🔍 ANALYSE DU PDF ANONYMISÉ:")
        doc = fitz.open(stream=anonymized_pdf, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            print(f"\n📄 Page {page_num + 1}:")
            
            text_blocks = page.get_text("dict")
            
            for block_num, block in enumerate(text_blocks["blocks"]):
                if "lines" in block:
                    print(f"  📦 Bloc {block_num}:")
                    for line_num, line in enumerate(block["lines"]):
                        print(f"    📝 Ligne {line_num}:")
                        for span_num, span in enumerate(line["spans"]):
                            print(f"      🔤 Span {span_num}:")
                            print(f"        Texte: '{span['text']}'")
                            print(f"        Police: {span['font']}")
                            print(f"        Taille: {span['size']}")
                            print(f"        Flags: {span['flags']} (binaire: {bin(span['flags'])})")
                            print(f"        Couleur: {span['color']}")
        
        doc.close()
        
        print("\n🔓 TEST DÉ-ANONYMISATION:")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        
        # Sauvegarder le PDF dé-anonymisé
        with open("test_formatage_debug_deanonymized.pdf", 'wb') as f:
            f.write(deanonymized_pdf)
        
        print("✅ Tests terminés avec succès!")
        
    except Exception as e:
        print(f"❌ Erreur pendant les tests: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        # Nettoyer les fichiers temporaires
        for file in [test_pdf_path]:
            if os.path.exists(file):
                os.unlink(file)
    
    return True

if __name__ == "__main__":
    success = test_formatage_debug()
    sys.exit(0 if success else 1) 