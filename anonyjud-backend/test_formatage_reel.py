#!/usr/bin/env python3
"""
Script de test réaliste pour tester l'anonymisation avec différents types de formatage.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import fitz
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging détaillé
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_realistic_test_pdf():
    """Crée un PDF de test réaliste avec différents formatages"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Simuler un document juridique avec différents formatages
    page.insert_text((50, 50), "TRIBUNAL DE GRANDE INSTANCE", fontname="Times-Bold", fontsize=14)
    page.insert_text((50, 80), "Affaire n° 2024-001234", fontname="Times-Roman", fontsize=12)
    page.insert_text((50, 110), "Parties:", fontname="Times-Bold", fontsize=12)
    
    # Texte avec noms à anonymiser
    page.insert_text((70, 140), "Demandeur: Jean DUPONT", fontname="Times-Roman", fontsize=11)
    page.insert_text((70, 160), "Défendeur: Marie MARTIN", fontname="Times-Bold", fontsize=11)
    page.insert_text((70, 180), "Avocat: Pierre DURAND", fontname="Times-Italic", fontsize=11)
    
    # Texte avec formatage mixte
    page.insert_text((50, 220), "Considérant que le demandeur ", fontname="Times-Roman", fontsize=11)
    page.insert_text((200, 220), "Jean DUPONT", fontname="Times-Bold", fontsize=11)
    page.insert_text((280, 220), " a saisi le tribunal...", fontname="Times-Roman", fontsize=11)
    
    # Texte en couleur
    page.insert_text((50, 250), "IMPORTANT:", fontname="Times-Bold", fontsize=12, color=(1, 0, 0))
    page.insert_text((130, 250), "Sophie LEROY", fontname="Times-Bold", fontsize=12, color=(1, 0, 0))
    page.insert_text((220, 250), " doit comparaître", fontname="Times-Roman", fontsize=12)
    
    # Différentes polices
    page.insert_text((50, 300), "Helvetica normal: Thomas BERNARD", fontname="Helvetica", fontsize=11)
    page.insert_text((50, 320), "Helvetica gras: Anne PETIT", fontname="Helvetica-Bold", fontsize=11)
    page.insert_text((50, 340), "Helvetica italique: Marc ROUX", fontname="Helvetica-Oblique", fontsize=11)
    
    # Courier (police monospace)
    page.insert_text((50, 380), "Courier: CODE-123-Paul-MICHEL", fontname="Courier", fontsize=10)
    page.insert_text((50, 400), "Courier gras: REF-456-Lucie-SIMON", fontname="Courier-Bold", fontsize=10)
    
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def analyze_pdf_formatting_detailed(pdf_bytes, title="PDF"):
    """Analyse détaillée du formatage du texte dans un PDF"""
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    
    print(f"\n=== ANALYSE DÉTAILLÉE DU FORMATAGE - {title} ===")
    
    for page_num in range(len(doc)):
        page = doc[page_num]
        text_blocks = page.get_text("dict")
        
        print(f"\nPage {page_num + 1}:")
        
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
                            
                            # Détecter le formatage
                            is_bold = bool(font_flags & 16)  # 2^4
                            is_italic = bool(font_flags & 32)  # 2^5
                            
                            # Identifier si c'est un nom à anonymiser
                            is_name = any(name in text for name in ["DUPONT", "MARTIN", "DURAND", "LEROY", "BERNARD", "PETIT", "ROUX", "MICHEL", "SIMON", "Jean", "Marie", "Pierre", "Sophie", "Thomas", "Anne", "Marc", "Paul", "Lucie"])
                            
                            prefix = "🎯 NOM DÉTECTÉ" if is_name else "   "
                            
                            print(f"  {prefix} [{block_num}.{line_num}.{span_num}] '{text}'")
                            print(f"      Police: {font_name}, Taille: {font_size}")
                            print(f"      Gras: {is_bold}, Italique: {is_italic}")
                            print(f"      Couleur: {color}, Flags: {font_flags}")
                            print()
    
    doc.close()

def test_realistic_anonymization():
    """Test l'anonymisation avec un PDF réaliste"""
    print("🚀 DÉBUT DU TEST D'ANONYMISATION RÉALISTE")
    
    # Créer un PDF de test réaliste
    print("\n1. Création du PDF de test réaliste...")
    pdf_bytes = create_realistic_test_pdf()
    
    # Analyser le formatage original
    print("\n2. Analyse du formatage original:")
    analyze_pdf_formatting_detailed(pdf_bytes, "ORIGINAL")
    
    # Définir les tiers pour l'anonymisation
    tiers = [
        {"numero": 1, "nom": "DUPONT", "prenom": "Jean"},
        {"numero": 2, "nom": "MARTIN", "prenom": "Marie"},
        {"numero": 3, "nom": "DURAND", "prenom": "Pierre"},
        {"numero": 4, "nom": "LEROY", "prenom": "Sophie"},
        {"numero": 5, "nom": "BERNARD", "prenom": "Thomas"},
        {"numero": 6, "nom": "PETIT", "prenom": "Anne"},
        {"numero": 7, "nom": "ROUX", "prenom": "Marc"},
        {"numero": 8, "nom": "MICHEL", "prenom": "Paul"},
        {"numero": 9, "nom": "SIMON", "prenom": "Lucie"}
    ]
    
    # Anonymiser le PDF
    print("\n3. Anonymisation du PDF...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_bytes, tiers)
        print(f"✅ Anonymisation réussie.")
        print(f"📊 Mapping généré: {mapping}")
        
        # Analyser le formatage après anonymisation
        print("\n4. Analyse du formatage après anonymisation:")
        analyze_pdf_formatting_detailed(anonymized_pdf, "ANONYMISÉ")
        
        # Test de dé-anonymisation
        print("\n5. Test de dé-anonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        
        # Analyser le formatage après dé-anonymisation
        print("\n6. Analyse du formatage après dé-anonymisation:")
        analyze_pdf_formatting_detailed(deanonymized_pdf, "DÉ-ANONYMISÉ")
        
        # Sauvegarder les fichiers pour inspection visuelle
        with open("test_reel_original.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        with open("test_reel_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        
        with open("test_reel_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        
        print("\n✅ Fichiers sauvegardés:")
        print("  - test_reel_original.pdf (original)")
        print("  - test_reel_anonymized.pdf (anonymisé)")
        print("  - test_reel_deanonymized.pdf (dé-anonymisé)")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'anonymisation: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_realistic_anonymization() 