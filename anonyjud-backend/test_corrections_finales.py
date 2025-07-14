#!/usr/bin/env python3
"""
Test et correction des problèmes finaux d'anonymisation PDF:
1. Marge droite non respectée
2. Caractères mal définis
3. Formatage gras et couleur non retranscrit lors de la déanonymisation
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
import fitz  # PyMuPDF
import logging

# Configuration du logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def create_simple_test_pdf():
    """Crée un PDF de test simple avec du texte de base"""
    doc = fitz.open()
    page = doc.new_page()
    
    # Obtenir les dimensions de la page
    page_rect = page.rect
    print(f"📄 Dimensions de la page: {page_rect}")
    
    # Insérer du texte simple avec des polices de base
    page.insert_text((50, 100), "Texte normal: HUISSOUD Louis", fontsize=12)
    page.insert_text((50, 130), "Texte normal: IMBERT Arnaud", fontsize=12)
    page.insert_text((50, 160), "Texte normal: GAUTHIER Guylaine", fontsize=12)
    page.insert_text((50, 190), "Texte normal: RIBEIRO Marie", fontsize=12)
    
    # Insérer du texte près de la marge droite (problématique)
    long_text = "Texte très long qui dépasse la marge droite: MARTIN Jean-Pierre avec une adresse très longue"
    page.insert_text((page_rect.x1 - 200, 220), long_text, fontsize=12)
    
    # Insérer du texte avec caractères spéciaux
    page.insert_text((50, 250), "Caractères spéciaux: FRANÇOIS Marie-Hélène", fontsize=12)
    
    # Sauvegarder le PDF de test
    pdf_bytes = doc.tobytes()
    doc.close()
    
    return pdf_bytes

def test_with_existing_pdf():
    """Test avec un PDF existant si disponible"""
    # Chercher un PDF existant dans le répertoire
    for file in os.listdir("."):
        if file.endswith(".pdf"):
            print(f"📄 Utilisation du PDF existant: {file}")
            with open(file, "rb") as f:
                return f.read()
    
    # Si aucun PDF existant, créer un PDF simple
    print("📄 Création d'un PDF de test simple...")
    return create_simple_test_pdf()

def test_anonymization_issues():
    """Test les problèmes d'anonymisation et de déanonymisation"""
    print("🧪 === TEST DES PROBLÈMES D'ANONYMISATION ===")
    
    # Obtenir un PDF de test
    try:
        pdf_content = test_with_existing_pdf()
    except Exception as e:
        print(f"❌ Erreur création PDF: {str(e)}")
        return
    
    # Sauvegarder le PDF original pour inspection
    with open("test_original_formatage.pdf", "wb") as f:
        f.write(pdf_content)
    print("✅ PDF original sauvegardé: test_original_formatage.pdf")
    
    # Tiers de test
    tiers = [
        {"numero": 1, "nom": "HUISSOUD", "prenom": "Louis", "adresse": "123 rue de la Paix"},
        {"numero": 2, "nom": "IMBERT", "prenom": "Arnaud", "adresse": "456 avenue Victor Hugo"},
        {"numero": 3, "nom": "GAUTHIER", "prenom": "Guylaine", "adresse": "789 boulevard Saint-Michel"},
        {"numero": 4, "nom": "RIBEIRO", "prenom": "Marie", "adresse": "321 rue des Lilas"},
        {"numero": 5, "nom": "MARTIN", "prenom": "Jean-Pierre", "adresse": "654 avenue de la République"},
        {"numero": 6, "nom": "FRANÇOIS", "prenom": "Marie-Hélène", "adresse": "987 rue du Commerce"}
    ]
    
    print(f"👥 Tiers de test: {len(tiers)} personnes")
    
    # Test d'anonymisation
    print("\n🔒 Test d'anonymisation...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie - Taille: {len(anonymized_pdf)} bytes")
        print(f"📊 Mapping: {mapping}")
        
        # Sauvegarder le PDF anonymisé
        with open("test_anonymized_formatage.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("✅ PDF anonymisé sauvegardé: test_anonymized_formatage.pdf")
        
        # Test de déanonymisation
        print("\n🔓 Test de déanonymisation...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print(f"✅ Déanonymisation réussie - Taille: {len(deanonymized_pdf)} bytes")
        
        # Sauvegarder le PDF déanonymisé
        with open("test_deanonymized_formatage.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("✅ PDF déanonymisé sauvegardé: test_deanonymized_formatage.pdf")
        
        # Analyser les problèmes
        print("\n🔍 Analyse des problèmes...")
        analyze_pdf_issues("test_original_formatage.pdf", "test_anonymized_formatage.pdf", "test_deanonymized_formatage.pdf")
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()

def analyze_pdf_issues(original_path, anonymized_path, deanonymized_path):
    """Analyse les problèmes dans les PDFs générés"""
    print("\n📊 === ANALYSE DES PROBLÈMES ===")
    
    files = [
        ("Original", original_path),
        ("Anonymisé", anonymized_path),
        ("Déanonymisé", deanonymized_path)
    ]
    
    for name, path in files:
        print(f"\n📄 Analyse du PDF {name}:")
        try:
            doc = fitz.open(path)
            page = doc[0]
            
            # Analyser les propriétés du texte
            text_dict = page.get_text("dict")
            
            for block in text_dict["blocks"]:
                if "lines" in block:
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                font = span["font"]
                                size = span["size"]
                                flags = span["flags"]
                                color = span["color"]
                                bbox = span["bbox"]
                                
                                # Vérifier les problèmes de marge
                                page_rect = page.rect
                                if bbox[2] > page_rect.x1 - 50:  # x1 (right) trop proche du bord
                                    print(f"⚠️ MARGE DROITE: '{text}' dépasse (x1={bbox[2]:.1f}, limite={page_rect.x1 - 50:.1f})")
                                
                                # Vérifier le formatage
                                is_bold = bool(flags & 16)
                                is_italic = bool(flags & 32)
                                
                                if is_bold or is_italic or color != 0:
                                    print(f"🎨 FORMATAGE: '{text}' - Police: {font}, Gras: {is_bold}, Italique: {is_italic}, Couleur: {color}")
                                
                                # Vérifier les caractères spéciaux
                                special_chars = any(ord(c) > 127 for c in text)
                                if special_chars:
                                    print(f"🔤 CARACTÈRES SPÉCIAUX: '{text}' - Police: {font}")
            
            doc.close()
            
        except Exception as e:
            print(f"❌ Erreur analyse {name}: {str(e)}")

if __name__ == "__main__":
    test_anonymization_issues()
    
    # Nettoyer les fichiers de test
    import os
    test_files = [
        "test_original_formatage.pdf",
        "test_anonymized_formatage.pdf", 
        "test_deanonymized_formatage.pdf"
    ]
    
    print("\n🧹 Nettoyage des fichiers de test...")
    for file in test_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Supprimé: {file}") 