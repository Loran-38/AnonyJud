#!/usr/bin/env python3
"""
Test simple de préservation du formatage - utilise des PDFs existants ou crée un PDF basique
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
import fitz  # PyMuPDF
import logging

# Configuration du logging pour voir les détails du formatage
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_basic_test_pdf():
    """Crée un PDF de test basique sans problème de polices"""
    doc = fitz.open()
    page = doc.new_page()
    
    print("📄 Création d'un PDF de test basique...")
    
    # Texte simple sans spécification de police
    page.insert_text((50, 100), "Texte normal: HUISSOUD Louis", fontsize=12)
    page.insert_text((50, 130), "Texte normal: IMBERT Arnaud", fontsize=12)
    page.insert_text((50, 160), "Texte normal: GAUTHIER Guylaine", fontsize=12)
    page.insert_text((50, 190), "Texte normal: RIBEIRO Marie", fontsize=12)
    page.insert_text((50, 220), "Texte normal: MARTIN Jean-Pierre", fontsize=12)
    
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def analyze_pdf_text_details(pdf_path, description):
    """Analyse détaillée du texte d'un PDF"""
    print(f"\n📊 === ANALYSE DÉTAILLÉE {description.upper()} ===")
    
    try:
        doc = fitz.open(pdf_path)
        page = doc[0]
        
        # Extraire le texte simple
        simple_text = page.get_text()
        print(f"📝 Texte extrait: {repr(simple_text)}")
        
        # Analyser les détails de formatage
        text_dict = page.get_text("dict")
        
        for block_num, block in enumerate(text_dict["blocks"]):
            if "lines" in block:
                print(f"\n🔍 Bloc {block_num}:")
                for line_num, line in enumerate(block["lines"]):
                    print(f"  📏 Ligne {line_num}:")
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
                            
                            print(f"    📝 Span {span_num}: '{text}'")
                            print(f"        Police: {font}, Taille: {size:.1f}")
                            print(f"        Gras: {is_bold}, Italique: {is_italic}")
                            print(f"        Couleur: {color}, Flags: {flags}")
        
        doc.close()
        
    except Exception as e:
        print(f"❌ Erreur analyse {description}: {str(e)}")

def test_logs_formatting():
    """Test pour voir les logs de formatage en action"""
    print("🧪 === TEST DES LOGS DE FORMATAGE ===")
    
    # Créer ou utiliser un PDF de test
    pdf_content = create_basic_test_pdf()
    
    # Sauvegarder le PDF original
    with open("test_logs_original.pdf", "wb") as f:
        f.write(pdf_content)
    print("✅ PDF original sauvegardé: test_logs_original.pdf")
    
    # Analyser le PDF original
    analyze_pdf_text_details("test_logs_original.pdf", "PDF ORIGINAL")
    
    # Tiers de test réduits
    tiers = [
        {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
        {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"},
        {"numero": 3, "nom": "GAUTHIER", "prenom": "Guylaine", "adresse": "789 boulevard Saint-Michel"}
    ]
    
    print(f"\n👥 Tiers de test: {len(tiers)} personnes")
    
    # Test d'anonymisation avec logs détaillés
    print("\n🔒 Test d'anonymisation avec logs détaillés...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie")
        print(f"📊 Mapping: {mapping}")
        
        # Sauvegarder le PDF anonymisé
        with open("test_logs_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("✅ PDF anonymisé sauvegardé: test_logs_anonymized.pdf")
        
        # Analyser le PDF anonymisé
        analyze_pdf_text_details("test_logs_anonymized.pdf", "PDF ANONYMISÉ")
        
        # Test de déanonymisation
        print("\n🔓 Test de déanonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print(f"✅ Déanonymisation réussie")
        
        # Sauvegarder le PDF déanonymisé
        with open("test_logs_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("✅ PDF déanonymisé sauvegardé: test_logs_deanonymized.pdf")
        
        # Analyser le PDF déanonymisé
        analyze_pdf_text_details("test_logs_deanonymized.pdf", "PDF DÉANONYMISÉ")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

def test_with_existing_pdf():
    """Test avec un PDF existant si disponible"""
    print("\n🔍 Recherche de PDFs existants...")
    
    for file in os.listdir("."):
        if file.endswith(".pdf") and not file.startswith("test_"):
            print(f"📄 PDF trouvé: {file}")
            
            try:
                with open(file, "rb") as f:
                    pdf_content = f.read()
                
                print(f"📊 Taille: {len(pdf_content)} bytes")
                
                # Analyser ce PDF
                analyze_pdf_text_details(file, f"PDF EXISTANT ({file})")
                
                return pdf_content
                
            except Exception as e:
                print(f"❌ Erreur lecture {file}: {str(e)}")
    
    print("❌ Aucun PDF existant trouvé")
    return None

if __name__ == "__main__":
    # Essayer d'abord avec un PDF existant
    existing_pdf = test_with_existing_pdf()
    
    if existing_pdf:
        print("\n🧪 Test avec PDF existant...")
        # Test rapide avec PDF existant
        tiers = [
            {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
            {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"}
        ]
        
        try:
            anonymized_pdf, mapping = anonymize_pdf_direct(existing_pdf, tiers)
            print("✅ Anonymisation avec PDF existant réussie")
        except Exception as e:
            print(f"❌ Erreur avec PDF existant: {str(e)}")
    
    # Test avec PDF créé
    test_logs_formatting()
    
    print("\n📋 Fichiers de test créés:")
    print("  - test_logs_original.pdf")
    print("  - test_logs_anonymized.pdf")
    print("  - test_logs_deanonymized.pdf") 