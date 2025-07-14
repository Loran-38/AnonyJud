#!/usr/bin/env python3
"""
Test de débogage détaillé pour les corrections d'anonymisation PDF
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
import fitz  # PyMuPDF
import logging

# Configuration du logging détaillé
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_debug_test_pdf():
    """Crée un PDF de test spécifique pour déboguer"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Obtenir les dimensions de la page
    page_rect = page.rect
    print(f"📄 Dimensions de la page: {page_rect}")
    
    # Insérer du texte avec formatage pour tester
    page.insert_text((50, 100), "Test simple: HUISSOUD Louis", fontsize=12)
    page.insert_text((50, 130), "Test gras: IMBERT Arnaud", fontname="helv-bold", fontsize=12)
    page.insert_text((50, 160), "Test couleur: GAUTHIER Guylaine", fontsize=12, color=(1, 0, 0))
    
    # Texte près de la marge droite
    long_text = "Texte marge droite: MARTIN Jean-Pierre adresse longue"
    page.insert_text((page_rect.x1 - 250, 220), long_text, fontsize=12)
    
    # Sauvegarder le PDF de test
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def test_debug_anonymization():
    """Test de débogage détaillé"""
    print("🐛 === TEST DE DÉBOGAGE DÉTAILLÉ ===")
    
    # Créer un PDF de test
    pdf_content = create_debug_test_pdf()
    
    # Sauvegarder le PDF original
    with open("debug_original.pdf", "wb") as f:
        f.write(pdf_content)
    print("✅ PDF original sauvegardé: debug_original.pdf")
    
    # Tiers de test réduits
    tiers = [
        {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
        {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"},
        {"numero": 3, "nom": "GAUTHIER", "prenom": "Guylaine", "adresse": "789 boulevard Saint-Michel"},
        {"numero": 5, "nom": "MARTIN", "prenom": "Jean-Pierre", "adresse": "654 avenue de la République"}
    ]
    
    print(f"👥 Tiers de test: {len(tiers)} personnes")
    
    # Test d'anonymisation avec logs détaillés
    print("\n🔒 Test d'anonymisation avec logs détaillés...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie")
        print(f"📊 Mapping complet: {mapping}")
        
        # Sauvegarder le PDF anonymisé
        with open("debug_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("✅ PDF anonymisé sauvegardé: debug_anonymized.pdf")
        
        # Test de déanonymisation avec logs détaillés
        print("\n🔓 Test de déanonymisation avec logs détaillés...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print(f"✅ Déanonymisation réussie")
        
        # Sauvegarder le PDF déanonymisé
        with open("debug_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("✅ PDF déanonymisé sauvegardé: debug_deanonymized.pdf")
        
        # Analyser les trois PDFs
        print("\n🔍 Analyse détaillée des trois PDFs...")
        analyze_debug_pdfs()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

def analyze_debug_pdfs():
    """Analyse détaillée des PDFs de débogage"""
    files = [
        ("Original", "debug_original.pdf"),
        ("Anonymisé", "debug_anonymized.pdf"),
        ("Déanonymisé", "debug_deanonymized.pdf")
    ]
    
    for name, path in files:
        print(f"\n📄 === ANALYSE {name.upper()} ===")
        try:
            doc = fitz.open(path)
            page = doc[0]
            
            # Extraire le texte simple
            simple_text = page.get_text()
            print(f"📝 Texte simple: {repr(simple_text)}")
            
            # Analyser les propriétés détaillées
            text_dict = page.get_text("dict")
            
            for block_num, block in enumerate(text_dict["blocks"]):
                if "lines" in block:
                    print(f"\n🔍 Bloc {block_num}:")
                    for line_num, line in enumerate(block["lines"]):
                        print(f"  📏 Ligne {line_num}: bbox={line['bbox']}")
                        for span_num, span in enumerate(line["spans"]):
                            text = span["text"]
                            if text.strip():
                                font = span["font"]
                                size = span["size"]
                                flags = span["flags"]
                                color = span["color"]
                                bbox = span["bbox"]
                                
                                # Analyser le formatage
                                is_bold = bool(flags & 16)
                                is_italic = bool(flags & 32)
                                
                                print(f"    📝 Span {span_num}: '{text}'")
                                print(f"        Police: {font}, Taille: {size}")
                                print(f"        Gras: {is_bold}, Italique: {is_italic}, Couleur: {color}")
                                print(f"        BBox: {bbox}")
                                
                                # Vérifier les problèmes de marge
                                page_rect = page.rect
                                if bbox[2] > page_rect.x1 - 50:
                                    print(f"        ⚠️ PROBLÈME MARGE DROITE: {bbox[2]:.1f} > {page_rect.x1 - 50:.1f}")
            
            doc.close()
            
        except Exception as e:
            print(f"❌ Erreur analyse {name}: {str(e)}")

if __name__ == "__main__":
    test_debug_anonymization()
    
    # Garder les fichiers de test pour inspection manuelle
    print("\n📋 Fichiers de test conservés pour inspection:")
    print("  - debug_original.pdf")
    print("  - debug_anonymized.pdf")
    print("  - debug_deanonymized.pdf") 