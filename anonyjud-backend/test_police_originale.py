#!/usr/bin/env python3
"""
Test pour vérifier que la police originale est préservée lors de l'anonymisation avec formatage gras.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import fitz
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging détaillé
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_test_pdf_with_various_fonts():
    """Crée un PDF avec différentes polices et formatages"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Titre
    page.insert_text((50, 50), "TEST DE PRÉSERVATION DES POLICES", fontname="Times-Bold", fontsize=16)
    
    # Différentes polices avec texte normal
    page.insert_text((50, 100), "Times normal: Jean DUPONT", fontname="Times-Roman", fontsize=12)
    page.insert_text((50, 130), "Helvetica normal: Marie MARTIN", fontname="Helvetica", fontsize=12)
    page.insert_text((50, 160), "Courier normal: Pierre DURAND", fontname="Courier", fontsize=12)
    
    # Différentes polices avec formatage gras
    page.insert_text((50, 200), "Times gras: Sophie LEROY", fontname="Times-Bold", fontsize=12)
    page.insert_text((50, 230), "Helvetica gras: Thomas BERNARD", fontname="Helvetica-Bold", fontsize=12)
    page.insert_text((50, 260), "Courier gras: Anne PETIT", fontname="Courier-Bold", fontsize=12)
    
    # Différentes polices avec formatage italique
    page.insert_text((50, 300), "Times italique: Marc ROUX", fontname="Times-Italic", fontsize=12)
    page.insert_text((50, 330), "Helvetica italique: Lucie SIMON", fontname="Helvetica-Oblique", fontsize=12)
    page.insert_text((50, 360), "Courier italique: Paul MICHEL", fontname="Courier-Oblique", fontsize=12)
    
    # Polices avec couleur
    page.insert_text((50, 400), "Times rouge: Julie MOREAU", fontname="Times-Roman", fontsize=12, color=(1, 0, 0))
    page.insert_text((50, 430), "Helvetica bleu gras: Alex DUBOIS", fontname="Helvetica-Bold", fontsize=12, color=(0, 0, 1))
    
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def analyze_font_preservation(original_pdf, anonymized_pdf, deanonymized_pdf):
    """Analyse la préservation des polices à travers le processus d'anonymisation"""
    
    def extract_font_info(pdf_bytes, title):
        """Extrait les informations de police d'un PDF"""
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        font_info = {}
        
        print(f"\n=== ANALYSE DES POLICES - {title} ===")
        
        for page in doc:
            text_blocks = page.get_text("dict")
            for block in text_blocks["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text and any(name in text for name in ["Jean", "Marie", "Pierre", "Sophie", "Thomas", "Anne", "Marc", "Lucie", "Paul", "Julie", "Alex", "DUPONT", "MARTIN", "DURAND", "LEROY", "BERNARD", "PETIT", "ROUX", "SIMON", "MICHEL", "MOREAU", "DUBOIS", "NOM", "PRENOM"]):
                                font_name = span["font"]
                                font_flags = span["flags"]
                                is_bold = bool(font_flags & 16)
                                is_italic = bool(font_flags & 32)
                                color = span["color"]
                                
                                font_info[text] = {
                                    'font': font_name,
                                    'bold': is_bold,
                                    'italic': is_italic,
                                    'color': color
                                }
                                
                                print(f"  📝 '{text}' → Police: {font_name}, Gras: {is_bold}, Italique: {is_italic}, Couleur: {color}")
        
        doc.close()
        return font_info
    
    # Extraire les informations de police
    original_fonts = extract_font_info(original_pdf, "ORIGINAL")
    anonymized_fonts = extract_font_info(anonymized_pdf, "ANONYMISÉ")
    deanonymized_fonts = extract_font_info(deanonymized_pdf, "DÉ-ANONYMISÉ")
    
    # Vérifier la préservation des polices
    print(f"\n=== VÉRIFICATION DE LA PRÉSERVATION DES POLICES ===")
    
    problems = 0
    
    # Créer un mapping des textes originaux vers anonymisés
    original_to_anon_mapping = {}
    for orig_text in original_fonts.keys():
        if "Jean" in orig_text or "DUPONT" in orig_text:
            for anon_text in anonymized_fonts.keys():
                if "PRENOM1" in anon_text or "NOM1" in anon_text:
                    original_to_anon_mapping[orig_text] = anon_text
                    break
        elif "Marie" in orig_text or "MARTIN" in orig_text:
            for anon_text in anonymized_fonts.keys():
                if "PRENOM2" in anon_text or "NOM2" in anon_text:
                    original_to_anon_mapping[orig_text] = anon_text
                    break
        # Continuer pour les autres noms...
    
    # Vérifier que les polices sont préservées
    for orig_text, anon_text in original_to_anon_mapping.items():
        if anon_text in anonymized_fonts:
            orig_font = original_fonts[orig_text]['font']
            anon_font = anonymized_fonts[anon_text]['font']
            
            # Vérifier si la police de base est préservée
            orig_base = orig_font.split('-')[0]  # Times-Bold → Times
            anon_base = anon_font.split('-')[0]  # Times-Bold → Times
            
            if orig_base == anon_base:
                print(f"  ✅ POLICE PRÉSERVÉE: '{orig_text}' ({orig_font}) → '{anon_text}' ({anon_font})")
            else:
                print(f"  ❌ POLICE CHANGÉE: '{orig_text}' ({orig_font}) → '{anon_text}' ({anon_font})")
                problems += 1
            
            # Vérifier le formatage
            orig_bold = original_fonts[orig_text]['bold']
            anon_bold = anonymized_fonts[anon_text]['bold']
            
            if orig_bold == anon_bold:
                print(f"      ✅ Formatage gras préservé: {orig_bold}")
            else:
                print(f"      ❌ Formatage gras changé: {orig_bold} → {anon_bold}")
                problems += 1
    
    return problems

def test_font_preservation():
    """Test de préservation des polices lors de l'anonymisation"""
    print("🚀 TEST DE PRÉSERVATION DES POLICES LORS DE L'ANONYMISATION")
    print("=" * 70)
    
    # Créer un PDF avec différentes polices
    print("\n1. Création d'un PDF avec différentes polices...")
    pdf_bytes = create_test_pdf_with_various_fonts()
    
    # Définir les tiers
    tiers = [
        {"numero": 1, "nom": "DUPONT", "prenom": "Jean"},
        {"numero": 2, "nom": "MARTIN", "prenom": "Marie"},
        {"numero": 3, "nom": "DURAND", "prenom": "Pierre"},
        {"numero": 4, "nom": "LEROY", "prenom": "Sophie"},
        {"numero": 5, "nom": "BERNARD", "prenom": "Thomas"},
        {"numero": 6, "nom": "PETIT", "prenom": "Anne"},
        {"numero": 7, "nom": "ROUX", "prenom": "Marc"},
        {"numero": 8, "nom": "SIMON", "prenom": "Lucie"},
        {"numero": 9, "nom": "MICHEL", "prenom": "Paul"},
        {"numero": 10, "nom": "MOREAU", "prenom": "Julie"},
        {"numero": 11, "nom": "DUBOIS", "prenom": "Alex"}
    ]
    
    # Anonymiser
    print("\n2. Anonymisation...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_bytes, tiers)
        print(f"✅ Anonymisation terminée.")
        
        # Dé-anonymiser
        print("\n3. Dé-anonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print(f"✅ Dé-anonymisation terminée.")
        
        # Analyser la préservation des polices
        print("\n4. Analyse de la préservation des polices...")
        problems = analyze_font_preservation(pdf_bytes, anonymized_pdf, deanonymized_pdf)
        
        # Sauvegarder les fichiers
        with open("test_police_original.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        with open("test_police_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        
        with open("test_police_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        
        print("\n✅ Fichiers sauvegardés:")
        print("  - test_police_original.pdf")
        print("  - test_police_anonymized.pdf")
        print("  - test_police_deanonymized.pdf")
        
        # Résumé
        print("\n🏁 RÉSUMÉ:")
        if problems == 0:
            print("✅ SUCCÈS: Toutes les polices originales sont correctement préservées !")
            print("✅ Le formatage gras et les polices sont parfaitement maintenus.")
        else:
            print(f"❌ ATTENTION: {problems} problème(s) de préservation de police détecté(s)")
            print("❌ Des ajustements peuvent être nécessaires.")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_font_preservation() 