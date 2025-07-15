#!/usr/bin/env python3
"""
Script de test pour reproduire et corriger le problème de formatage gras lors de l'anonymisation PDF.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import fitz
import logging
from app.anonymizer import anonymize_pdf_direct

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_test_pdf_with_bold_text():
    """Crée un PDF de test avec du texte en gras"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Ajouter du texte normal
    page.insert_text((50, 100), "Texte normal: Jean Dupont", fontname="Helvetica", fontsize=12)
    
    # Ajouter du texte en gras
    page.insert_text((50, 150), "Texte en gras: Marie Martin", fontname="Helvetica-Bold", fontsize=12)
    
    # Ajouter du texte en couleur
    page.insert_text((50, 200), "Texte en couleur: Pierre Durand", fontname="Helvetica", fontsize=12, color=(1, 0, 0))
    
    # Ajouter du texte en gras et couleur
    page.insert_text((50, 250), "Texte gras et couleur: Sophie Leroy", fontname="Helvetica-Bold", fontsize=12, color=(0, 0, 1))
    
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def analyze_pdf_text_formatting(pdf_bytes):
    """Analyse le formatage du texte dans un PDF"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    print("=== ANALYSE DU FORMATAGE PDF ===")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_blocks = page.get_text("dict")
        
        print(f"\nPage {page_num + 1}:")
        
        for block in text_blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text:
                            font_name = span["font"]
                            font_size = span["size"]
                            font_flags = span["flags"]
                            color = span["color"]
                            
                            # Détecter le formatage
                            is_bold = bool(font_flags & 16)  # 2^4
                            is_italic = bool(font_flags & 32)  # 2^5
                            
                            print(f"  Texte: '{text}'")
                            print(f"    Police: {font_name}, Taille: {font_size}")
                            print(f"    Gras: {is_bold}, Italique: {is_italic}")
                            print(f"    Couleur: {color}, Flags: {font_flags}")
                            print()
    
    doc.close()

def test_anonymization_formatting():
    """Test l'anonymisation avec préservation du formatage"""
    print("🚀 DÉBUT DU TEST D'ANONYMISATION AVEC FORMATAGE")
    
    # Créer un PDF de test
    print("\n1. Création du PDF de test...")
    pdf_bytes = create_test_pdf_with_bold_text()
    
    # Analyser le formatage original
    print("\n2. Analyse du formatage original:")
    analyze_pdf_text_formatting(pdf_bytes)
    
    # Définir les tiers pour l'anonymisation
    tiers = [
        {"numero": 1, "nom": "Dupont", "prenom": "Jean"},
        {"numero": 2, "nom": "Martin", "prenom": "Marie"},
        {"numero": 3, "nom": "Durand", "prenom": "Pierre"},
        {"numero": 4, "nom": "Leroy", "prenom": "Sophie"}
    ]
    
    # Anonymiser le PDF
    print("\n3. Anonymisation du PDF...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_bytes, tiers)
        print(f"✅ Anonymisation réussie. Mapping: {mapping}")
        
        # Analyser le formatage après anonymisation
        print("\n4. Analyse du formatage après anonymisation:")
        analyze_pdf_text_formatting(anonymized_pdf)
        
        # Sauvegarder les fichiers pour inspection visuelle
        with open("test_original.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        with open("test_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        
        print("\n✅ Fichiers sauvegardés:")
        print("  - test_original.pdf (original)")
        print("  - test_anonymized.pdf (anonymisé)")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'anonymisation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_anonymization_formatting() 