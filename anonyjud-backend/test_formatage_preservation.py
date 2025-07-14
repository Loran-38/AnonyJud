#!/usr/bin/env python3
"""
Test spécifique pour la préservation du formatage gras et couleur dès l'anonymisation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
import fitz  # PyMuPDF
import logging

# Configuration du logging pour voir les détails du formatage
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_formatted_test_pdf():
    """Crée un PDF de test avec formatage gras et couleur"""
    doc = fitz.open()
    page = doc.new_page()
    
    print("📄 Création d'un PDF avec formatage gras et couleur...")
    
    # Texte normal en noir
    page.insert_text((50, 100), "Texte normal: HUISSOUD Louis", fontsize=12)
    
    # Texte en gras (utiliser la police système)
    page.insert_text((50, 130), "Texte gras: IMBERT Arnaud", fontsize=12, fontname="helv-bold")
    
    # Texte en couleur rouge
    page.insert_text((50, 160), "Texte rouge: GAUTHIER Guylaine", fontsize=12, color=(1, 0, 0))
    
    # Texte en gras ET rouge
    page.insert_text((50, 190), "Texte gras rouge: RIBEIRO Marie", fontsize=12, fontname="helv-bold", color=(1, 0, 0))
    
    # Texte en bleu
    page.insert_text((50, 220), "Texte bleu: MARTIN Jean-Pierre", fontsize=12, color=(0, 0, 1))
    
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def analyze_pdf_formatting(pdf_path, description):
    """Analyse le formatage d'un PDF"""
    print(f"\n📊 === ANALYSE {description.upper()} ===")
    
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        
        text_dict = page.get_text("dict")
        
        for block_num, block in enumerate(text_dict["blocks"]):
            if "lines" in block:
                for line_num, line in enumerate(block["lines"]):
                    for span_num, span in enumerate(line["spans"]):
                        text = span["text"].strip()
                        if text:
                            font = span["font"]
                            size = span["size"]
                            flags = span["flags"]
                            color = span["color"]
                            
                            # Analyser le formatage
                            is_bold = bool(flags & 16)
                            is_italic = bool(flags & 32)
                            
                            # Déterminer si c'est coloré
                            is_colored = color != 0
                            
                            print(f"📝 '{text}':")
                            print(f"    Police: {font}, Taille: {size:.1f}")
                            print(f"    Gras: {is_bold}, Italique: {is_italic}")
                            print(f"    Couleur: {color} ({'Coloré' if is_colored else 'Noir'})")
                            print(f"    Flags: {flags}")
                            print()
        
        doc.close()
        
    except Exception as e:
        print(f"❌ Erreur analyse {description}: {str(e)}")

def test_formatting_preservation():
    """Test principal de préservation du formatage"""
    print("🧪 === TEST DE PRÉSERVATION DU FORMATAGE ===")
    
    # Créer un PDF avec formatage
    pdf_content = create_formatted_test_pdf()
    
    # Sauvegarder le PDF original
    with open("test_format_original.pdf", "wb") as f:
        f.write(pdf_content)
    print("✅ PDF original sauvegardé: test_format_original.pdf")
    
    # Analyser le formatage du PDF original
    analyze_pdf_formatting("test_format_original.pdf", "PDF ORIGINAL")
    
    # Tiers de test
    tiers = [
        {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
        {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"},
        {"numero": 3, "nom": "GAUTHIER", "prenom": "Guylaine", "adresse": "789 boulevard Saint-Michel"},
        {"numero": 4, "nom": "RIBEIRO", "prenom": "Marie", "adresse": "321 rue des Lilas"},
        {"numero": 5, "nom": "MARTIN", "prenom": "Jean-Pierre", "adresse": "654 avenue de la République"}
    ]
    
    print(f"👥 Tiers de test: {len(tiers)} personnes")
    
    # Test d'anonymisation
    print("\n🔒 Test d'anonymisation avec préservation du formatage...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie")
        
        # Sauvegarder le PDF anonymisé
        with open("test_format_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("✅ PDF anonymisé sauvegardé: test_format_anonymized.pdf")
        
        # Analyser le formatage du PDF anonymisé
        analyze_pdf_formatting("test_format_anonymized.pdf", "PDF ANONYMISÉ")
        
        # Test de déanonymisation
        print("\n🔓 Test de déanonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print(f"✅ Déanonymisation réussie")
        
        # Sauvegarder le PDF déanonymisé
        with open("test_format_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("✅ PDF déanonymisé sauvegardé: test_format_deanonymized.pdf")
        
        # Analyser le formatage du PDF déanonymisé
        analyze_pdf_formatting("test_format_deanonymized.pdf", "PDF DÉANONYMISÉ")
        
        # Vérifications finales
        print("\n🔍 === VÉRIFICATIONS FINALES ===")
        check_formatting_preservation()
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

def check_formatting_preservation():
    """Vérifie que le formatage est bien préservé"""
    files = [
        ("Original", "test_format_original.pdf"),
        ("Anonymisé", "test_format_anonymized.pdf"),
        ("Déanonymisé", "test_format_deanonymized.pdf")
    ]
    
    formatting_stats = {}
    
    for name, path in files:
        try:
            doc = fitz.open(path)
            page = doc[0]
            text_dict = page.get_text("dict")
            
            bold_count = 0
            colored_count = 0
            total_spans = 0
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                total_spans += 1
                                flags = span["flags"]
                                color = span["color"]
                                
                                if bool(flags & 16):  # Gras
                                    bold_count += 1
                                if color != 0:  # Couleur
                                    colored_count += 1
            
            formatting_stats[name] = {
                'bold': bold_count,
                'colored': colored_count,
                'total': total_spans
            }
            
            doc.close()
            
        except Exception as e:
            print(f"❌ Erreur vérification {name}: {str(e)}")
    
    # Afficher les statistiques
    print("📊 Statistiques de formatage:")
    for name, stats in formatting_stats.items():
        print(f"  {name}: {stats['bold']} gras, {stats['colored']} colorés, {stats['total']} total")
    
    # Vérifier la préservation
    if 'Original' in formatting_stats and 'Anonymisé' in formatting_stats:
        orig = formatting_stats['Original']
        anon = formatting_stats['Anonymisé']
        
        if anon['bold'] >= orig['bold'] and anon['colored'] >= orig['colored']:
            print("✅ FORMATAGE PRÉSERVÉ lors de l'anonymisation!")
        else:
            print("❌ FORMATAGE PERDU lors de l'anonymisation!")
            print(f"   Gras: {orig['bold']} → {anon['bold']}")
            print(f"   Couleur: {orig['colored']} → {anon['colored']}")

if __name__ == "__main__":
    test_formatting_preservation()
    
    print("\n📋 Fichiers de test créés:")
    print("  - test_format_original.pdf")
    print("  - test_format_anonymized.pdf")
    print("  - test_format_deanonymized.pdf")
    print("\nVous pouvez les ouvrir pour vérifier visuellement le formatage.") 