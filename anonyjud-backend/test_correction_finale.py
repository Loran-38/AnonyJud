#!/usr/bin/env python3
"""
Script de test final pour démontrer la correction du problème de formatage gras lors de l'anonymisation.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

import fitz
import logging
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging détaillé
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_problematic_pdf():
    """Crée un PDF avec différents types de formatage qui pourraient poser problème"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Titre
    page.insert_text((50, 50), "DOCUMENT JURIDIQUE - TEST DE FORMATAGE", fontname="Times-Bold", fontsize=16)
    
    # Cas 1: Texte normal qui doit rester normal
    page.insert_text((50, 100), "Texte normal: Jean DUPONT habite à Paris", fontname="Times-Roman", fontsize=11)
    
    # Cas 2: Nom en gras qui DOIT rester en gras après anonymisation
    page.insert_text((50, 130), "Défendeur: ", fontname="Times-Roman", fontsize=11)
    page.insert_text((120, 130), "Marie MARTIN", fontname="Times-Bold", fontsize=11)
    page.insert_text((200, 130), " représentée par...", fontname="Times-Roman", fontsize=11)
    
    # Cas 3: Nom en gras et couleur qui DOIT rester en gras et coloré
    page.insert_text((50, 160), "IMPORTANT: ", fontname="Times-Bold", fontsize=12, color=(1, 0, 0))
    page.insert_text((130, 160), "Pierre DURAND", fontname="Times-Bold", fontsize=12, color=(1, 0, 0))
    page.insert_text((230, 160), " doit comparaître", fontname="Times-Roman", fontsize=12)
    
    # Cas 4: Différentes polices en gras
    page.insert_text((50, 200), "Helvetica gras: Sophie LEROY", fontname="Helvetica-Bold", fontsize=11)
    page.insert_text((50, 230), "Courier gras: Thomas BERNARD", fontname="Courier-Bold", fontsize=10)
    
    # Cas 5: Texte avec police système (potentiellement problématique)
    try:
        page.insert_text((50, 260), "Arial gras: Anne PETIT", fontname="Arial-Bold", fontsize=11)
    except:
        # Fallback si Arial n'est pas disponible
        page.insert_text((50, 260), "Times gras: Anne PETIT", fontname="Times-Bold", fontsize=11)
    
    # Cas 6: Texte italique
    page.insert_text((50, 290), "Texte italique: Marc ROUX", fontname="Times-Italic", fontsize=11)
    
    # Cas 7: Texte avec flags de formatage mais police normale (cas problématique)
    page.insert_text((50, 320), "Cas spécial: Lucie SIMON", fontname="Times-Roman", fontsize=11)
    
    pdf_bytes = doc.tobytes()
    doc.close()
    return pdf_bytes

def analyze_formatting_before_after(original_pdf, anonymized_pdf, title_prefix=""):
    """Compare le formatage avant et après anonymisation"""
    print(f"\n=== ANALYSE COMPARATIVE DU FORMATAGE {title_prefix} ===")
    
    # Analyser l'original
    print("\n📄 ORIGINAL:")
    doc_orig = fitz.open(stream=original_pdf, filetype="pdf")
    original_formatting = {}
    
    for page in doc_orig:
        text_blocks = page.get_text("dict")
        for block in text_blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text and any(name in text for name in ["Jean", "Marie", "Pierre", "Sophie", "Thomas", "Anne", "Marc", "Lucie", "DUPONT", "MARTIN", "DURAND", "LEROY", "BERNARD", "PETIT", "ROUX", "SIMON"]):
                            font_name = span["font"]
                            font_flags = span["flags"]
                            is_bold = bool(font_flags & 16)
                            color = span["color"]
                            
                            original_formatting[text] = {
                                'font': font_name,
                                'bold': is_bold,
                                'color': color,
                                'flags': font_flags
                            }
                            
                            print(f"  🎯 '{text}' - Police: {font_name}, Gras: {is_bold}, Couleur: {color}")
    
    doc_orig.close()
    
    # Analyser l'anonymisé
    print("\n📄 ANONYMISÉ:")
    doc_anon = fitz.open(stream=anonymized_pdf, filetype="pdf")
    anonymized_formatting = {}
    
    for page in doc_anon:
        text_blocks = page.get_text("dict")
        for block in text_blocks["blocks"]:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        text = span["text"].strip()
                        if text and ("NOM" in text or "PRENOM" in text):
                            font_name = span["font"]
                            font_flags = span["flags"]
                            is_bold = bool(font_flags & 16)
                            color = span["color"]
                            
                            anonymized_formatting[text] = {
                                'font': font_name,
                                'bold': is_bold,
                                'color': color,
                                'flags': font_flags
                            }
                            
                            print(f"  🎯 '{text}' - Police: {font_name}, Gras: {is_bold}, Couleur: {color}")
    
    doc_anon.close()
    
    # Vérifier la préservation du formatage
    print("\n📊 VÉRIFICATION DE LA PRÉSERVATION DU FORMATAGE:")
    
    problems_found = 0
    
    # Vérifier que les textes anonymisés ont le bon formatage
    for anon_text, anon_format in anonymized_formatting.items():
        if not anon_format['bold'] and ("NOM" in anon_text or "PRENOM" in anon_text):
            # Vérifier si le texte original était en gras
            for orig_text, orig_format in original_formatting.items():
                if orig_format['bold']:
                    print(f"  ❌ PROBLÈME: '{anon_text}' devrait être en gras (original '{orig_text}' était en gras)")
                    problems_found += 1
                    break
        elif anon_format['bold']:
            print(f"  ✅ CORRECT: '{anon_text}' est en gras comme attendu")
    
    if problems_found == 0:
        print("  ✅ TOUS LES FORMATAGES SONT CORRECTEMENT PRÉSERVÉS !")
    else:
        print(f"  ❌ {problems_found} problème(s) de formatage détecté(s)")
    
    return problems_found

def test_final_correction():
    """Test final de la correction du formatage gras"""
    print("🚀 TEST FINAL DE LA CORRECTION DU FORMATAGE GRAS")
    print("=" * 60)
    
    # Créer un PDF problématique
    print("\n1. Création d'un PDF avec différents cas de formatage...")
    pdf_bytes = create_problematic_pdf()
    
    # Définir les tiers
    tiers = [
        {"numero": 1, "nom": "DUPONT", "prenom": "Jean"},
        {"numero": 2, "nom": "MARTIN", "prenom": "Marie"},
        {"numero": 3, "nom": "DURAND", "prenom": "Pierre"},
        {"numero": 4, "nom": "LEROY", "prenom": "Sophie"},
        {"numero": 5, "nom": "BERNARD", "prenom": "Thomas"},
        {"numero": 6, "nom": "PETIT", "prenom": "Anne"},
        {"numero": 7, "nom": "ROUX", "prenom": "Marc"},
        {"numero": 8, "nom": "SIMON", "prenom": "Lucie"}
    ]
    
    # Anonymiser
    print("\n2. Anonymisation avec correction du formatage...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_bytes, tiers)
        print(f"✅ Anonymisation terminée. Mapping: {mapping}")
        
        # Analyser le formatage
        print("\n3. Analyse comparative du formatage...")
        problems = analyze_formatting_before_after(pdf_bytes, anonymized_pdf)
        
        # Test de dé-anonymisation
        print("\n4. Test de dé-anonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        
        # Sauvegarder les fichiers
        with open("test_final_original.pdf", "wb") as f:
            f.write(pdf_bytes)
        
        with open("test_final_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        
        with open("test_final_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        
        print("\n✅ Fichiers sauvegardés:")
        print("  - test_final_original.pdf")
        print("  - test_final_anonymized.pdf")
        print("  - test_final_deanonymized.pdf")
        
        # Résumé
        print("\n🏁 RÉSUMÉ:")
        if problems == 0:
            print("✅ SUCCÈS: Tous les formatages gras sont correctement préservés lors de l'anonymisation !")
            print("✅ La correction du problème de formatage gras fonctionne parfaitement.")
        else:
            print(f"❌ ATTENTION: {problems} problème(s) de formatage détecté(s)")
            print("❌ Des améliorations supplémentaires peuvent être nécessaires.")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_final_correction() 