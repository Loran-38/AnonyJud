#!/usr/bin/env python3
"""
Script pour créer un PDF de test avec formatage (gras, couleur) et descenders
"""

import fitz  # PyMuPDF
import sys
import os

def create_test_pdf_with_formatting():
    """
    Crée un PDF de test avec le contenu fourni par l'utilisateur et différents formatages
    """
    # Créer un nouveau document PDF
    doc = fitz.open()
    
    # Ajouter une page
    page = doc.new_page()
    
    # Définir les polices et styles
    font_normal = "helv"
    font_bold = "helv-bold"
    font_italic = "helv-italic"
    
    # Couleurs
    black = (0, 0, 0)
    blue = (0, 0, 1)
    red = (1, 0, 0)
    
    # Position de départ
    x = 50
    y = 50
    line_height = 20
    
    # Contenu du document avec formatage
    content = [
        ("Avocat du demandeur", font_bold, 14, black),
        ("SCP THOIZET & Associés", font_normal, 12, black),
        ("Me Jacques THOIZET", font_normal, 12, black),
        ("61, Quai Riondet", font_normal, 12, black),
        ("BP 374", font_normal, 12, black),
        ("38205 VIENNE cedex", font_normal, 12, black),
        ("Tel : 04.74.53.70.00", font_normal, 12, black),
        ("Courriel : avocat.thoizet@gmail.com / avocat.thoizet@gmail.com", font_normal, 12, blue),
        ("Référence du dossier : 22.0003—HUISSOUD/IMBERT-GAUTHIER-MAAF-MATMUT", font_normal, 12, black),
        ("", font_normal, 12, black),  # Ligne vide
        ("Avocat du demandeur", font_bold, 14, black),
        ("SCP THOIZET & Associés", font_normal, 12, black),
        ("Me Jacques THOIZET", font_normal, 12, black),
        ("61, Quai Riondet", font_normal, 12, black),
        ("BP 374", font_normal, 12, black),
        ("38205 VIENNE Cedex", font_normal, 12, black),
        ("Tel : 04.74.53.70.00", font_normal, 12, black),
        ("Courriel : avocat.thoizet@gmail.com / avocat.thoizet@gmail.com", font_normal, 12, blue),
        ("Référence du dossier : 22.0003 HUISSOUD/IMBERT GAUTHIER MAAF MATMUT", font_normal, 12, black),
        ("", font_normal, 12, black),  # Ligne vide
        ("Test avec des descenders: gjpqy", font_normal, 12, red),
        ("HUISSOUD Louis (nom en gras)", font_bold, 12, black),
        ("Texte avec descenders en italique: gjpqy", font_italic, 12, black),
    ]
    
    # Insérer le contenu
    for line_text, font, size, color in content:
        if line_text.strip():  # Seulement si la ligne n'est pas vide
            try:
                page.insert_text(
                    (x, y),
                    line_text,
                    fontname=font,
                    fontsize=size,
                    color=color
                )
            except Exception as e:
                print(f"Erreur insertion ligne '{line_text}': {e}")
                # Fallback avec police par défaut
                page.insert_text(
                    (x, y),
                    line_text,
                    fontname="helv",
                    fontsize=size,
                    color=color
                )
        
        y += line_height
    
    # Sauvegarder le PDF
    output_path = "test_formatage_original.pdf"
    doc.save(output_path)
    doc.close()
    
    print(f"✅ PDF de test créé: {output_path}")
    return output_path

def main():
    """Fonction principale"""
    print("🚀 Création d'un PDF de test avec formatage...")
    
    try:
        pdf_path = create_test_pdf_with_formatting()
        
        # Vérifier que le fichier existe
        if os.path.exists(pdf_path):
            size = os.path.getsize(pdf_path)
            print(f"📊 Taille du fichier: {size} bytes")
            print(f"📄 Fichier créé: {pdf_path}")
        else:
            print("❌ Erreur: Le fichier n'a pas été créé")
            
    except Exception as e:
        print(f"❌ Erreur lors de la création du PDF: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 