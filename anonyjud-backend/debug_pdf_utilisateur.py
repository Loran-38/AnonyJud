#!/usr/bin/env python3
"""
Script de debug pour analyser un PDF utilisateur spécifique et identifier les problèmes de formatage.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import fitz
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging très détaillé
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def analyze_user_pdf(pdf_path):
    """Analyse un PDF utilisateur pour identifier les problèmes de formatage"""
    print(f"🔍 ANALYSE DU PDF UTILISATEUR: {pdf_path}")
    
    try:
        # Lire le PDF
        with open(pdf_path, 'rb') as f:
            pdf_bytes = f.read()
        
        print(f"📄 Taille du PDF: {len(pdf_bytes)} bytes")
        
        # Analyser le formatage original
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        
        print(f"📄 Nombre de pages: {len(doc)}")
        
        # Analyser chaque page
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_blocks = page.get_text("dict")
            
            print(f"\n=== PAGE {page_num + 1} ===")
            
            for block_num, block in enumerate(text_blocks["blocks"]):
                if "lines" in block:
                    for line_num, line in enumerate(block["lines"]):
                        for span_num, span in enumerate(line["spans"]):
                            text = span["text"].strip()
                            if text:
                                font_name = span["font"]
                                font_size = span["size"]
                                font_flags = span["flags"]
                                color = span["color"]
                                bbox = span["bbox"]
                                
                                # Détecter le formatage
                                is_bold = bool(font_flags & 16)  # 2^4
                                is_italic = bool(font_flags & 32)  # 2^5
                                
                                # Identifier si c'est potentiellement un nom
                                contains_caps = any(c.isupper() for c in text)
                                
                                if is_bold or contains_caps:
                                    print(f"  🎯 TEXTE IMPORTANT [{block_num}.{line_num}.{span_num}]")
                                    print(f"     Texte: '{text}'")
                                    print(f"     Police: {font_name}, Taille: {font_size}")
                                    print(f"     Gras: {is_bold}, Italique: {is_italic}")
                                    print(f"     Couleur: {color}, Flags: {font_flags}")
                                    print(f"     Position: {bbox}")
                                    
                                    # Analyser la police
                                    if "-Bold" in font_name or "-bold" in font_name:
                                        print(f"     ✅ Police intrinsèquement en gras")
                                    elif is_bold:
                                        print(f"     ⚠️ Gras détecté par flags mais pas dans le nom de police")
                                    
                                    print()
        
        doc.close()
        return pdf_bytes
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def test_anonymization_on_user_pdf(pdf_bytes):
    """Test l'anonymisation sur le PDF utilisateur"""
    print("\n🧪 TEST D'ANONYMISATION SUR PDF UTILISATEUR")
    
    # Tiers de test - adaptez selon votre PDF
    tiers = [
        {"numero": 1, "nom": "DUPONT", "prenom": "Jean"},
        {"numero": 2, "nom": "MARTIN", "prenom": "Marie"},
        {"numero": 3, "nom": "DURAND", "prenom": "Pierre"},
        {"numero": 4, "nom": "LEROY", "prenom": "Sophie"},
        {"numero": 5, "nom": "BERNARD", "prenom": "Thomas"},
        # Ajoutez d'autres tiers selon votre PDF
    ]
    
    try:
        # Anonymiser
        print("\n1. Anonymisation...")
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_bytes, tiers)
        print(f"✅ Anonymisation terminée. Mapping: {mapping}")
        
        # Analyser le résultat
        print("\n2. Analyse du PDF anonymisé...")
        doc = fitz.open(stream=anonymized_pdf, filetype="pdf")
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text_blocks = page.get_text("dict")
            
            print(f"\n=== PAGE ANONYMISÉE {page_num + 1} ===")
            
            for block_num, block in enumerate(text_blocks["blocks"]):
                if "lines" in block:
                    for line_num, line in enumerate(block["lines"]):
                        for span_num, span in enumerate(line["spans"]):
                            text = span["text"].strip()
                            if text and ("NOM" in text or "PRENOM" in text):
                                font_name = span["font"]
                                font_size = span["size"]
                                font_flags = span["flags"]
                                color = span["color"]
                                
                                # Détecter le formatage
                                is_bold = bool(font_flags & 16)  # 2^4
                                is_italic = bool(font_flags & 32)  # 2^5
                                
                                print(f"  🎯 TEXTE ANONYMISÉ [{block_num}.{line_num}.{span_num}]")
                                print(f"     Texte: '{text}'")
                                print(f"     Police: {font_name}, Taille: {font_size}")
                                print(f"     Gras: {is_bold}, Italique: {is_italic}")
                                print(f"     Couleur: {color}, Flags: {font_flags}")
                                
                                if not is_bold and ("NOM" in text or "PRENOM" in text):
                                    print(f"     ❌ PROBLÈME: Texte anonymisé sans formatage gras !")
                                elif is_bold:
                                    print(f"     ✅ Formatage gras préservé")
                                print()
        
        doc.close()
        
        # Sauvegarder pour inspection
        with open("debug_user_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        
        print("✅ PDF anonymisé sauvegardé: debug_user_anonymized.pdf")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'anonymisation: {str(e)}")
        import traceback
        traceback.print_exc()

def main():
    """Fonction principale"""
    print("🚀 SCRIPT DE DEBUG POUR PDF UTILISATEUR")
    print("=" * 50)
    
    # Demander le chemin du PDF
    pdf_path = input("Entrez le chemin vers votre PDF (ou 'test' pour créer un PDF de test): ")
    
    if pdf_path.lower() == 'test':
        # Créer un PDF de test avec problème potentiel
        print("📝 Création d'un PDF de test avec problème potentiel...")
        doc = fitz.open()
        page = doc.new_page()
        
        # Texte avec police système qui pourrait poser problème
        try:
            page.insert_text((50, 100), "Demandeur: Jean DUPONT", fontname="Arial", fontsize=12)
            page.insert_text((50, 130), "Défendeur: Marie MARTIN", fontname="Arial-Bold", fontsize=12)
        except:
            # Fallback si Arial n'est pas disponible
            page.insert_text((50, 100), "Demandeur: Jean DUPONT", fontname="Times-Roman", fontsize=12)
            page.insert_text((50, 130), "Défendeur: Marie MARTIN", fontname="Times-Bold", fontsize=12)
        
        pdf_bytes = doc.tobytes()
        doc.close()
        
        with open("test_debug.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        pdf_path = "test_debug.pdf"
        print(f"✅ PDF de test créé: {pdf_path}")
    
    # Analyser le PDF
    pdf_bytes = analyze_user_pdf(pdf_path)
    
    if pdf_bytes:
        # Tester l'anonymisation
        test_anonymization_on_user_pdf(pdf_bytes)
    
    print("\n🏁 DEBUG TERMINÉ")

if __name__ == "__main__":
    main() 