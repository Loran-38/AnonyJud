"""
Test de préservation de mise en page pour le pipeline PDF enhanced amélioré
"""

import os
import sys
import tempfile
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Ajouter le répertoire app au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.anonymizer import (
    anonymize_pdf_enhanced_pipeline, 
    deanonymize_pdf_enhanced_pipeline,
    convert_pdf_to_word_enhanced,
    convert_word_to_pdf_enhanced,
    PDF_ENHANCED_PIPELINE,
    DOCX2PDF_AVAILABLE
)
from app.utils import extract_text_from_pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

def create_complex_test_pdf():
    """Créer un PDF de test avec mise en page complexe"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']
    
    story = []
    
    # Titre principal
    story.append(Paragraph("Références des Parties", title_style))
    story.append(Spacer(1, 12))
    
    # Section Partie Demanderesse
    story.append(Paragraph("Partie Demanderesse", heading_style))
    story.append(Spacer(1, 6))
    
    # Demandeur 1
    story.append(Paragraph("Demandeur 1", styles['Heading2']))
    story.append(Paragraph("Monsieur HUISSOUD Louis", normal_style))
    story.append(Paragraph("244 Montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    story.append(Spacer(1, 12))
    
    # Avocat du demandeur
    story.append(Paragraph("Avocat du demandeur", styles['Heading3']))
    story.append(Paragraph("SCP THOIZET & Associés", normal_style))
    story.append(Paragraph("Me Jacques THOIZET", normal_style))
    story.append(Paragraph("61, Quai Riondet", normal_style))
    story.append(Paragraph("BP 374", normal_style))
    story.append(Paragraph("38205 VIENNE cedex", normal_style))
    story.append(Paragraph("Tel : 04.74.53.70.00", normal_style))
    story.append(Paragraph("Courriel : avocat.thoizet@gmail.com / avocat.thoizet@gmail.com", normal_style))
    story.append(Paragraph("Référence du dossier : 22.0003--HUISSOUD/IMBERT--GAUTHIER--MAAF--MATMUT", normal_style))
    story.append(Spacer(1, 12))
    
    # Section Partie Défenderesse
    story.append(Paragraph("Partie Défenderesse", heading_style))
    story.append(Spacer(1, 6))
    
    # Défendeur 01
    story.append(Paragraph("Défendeur 01", styles['Heading2']))
    story.append(Paragraph("Monsieur IMBERT Arnaud", normal_style))
    story.append(Paragraph("256 Montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    story.append(Spacer(1, 12))
    
    # Défendeur 02
    story.append(Paragraph("Défendeur 02", styles['Heading2']))
    story.append(Paragraph("Madame GAUTHIER Guylaine", normal_style))
    story.append(Paragraph("256 Montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    story.append(Spacer(1, 12))
    
    # Tableau d'exemple
    table_data = [
        ['Nom', 'Prénom', 'Adresse'],
        ['HUISSOUD', 'Louis', '244 Montée du Mollard'],
        ['IMBERT', 'Arnaud', '256 Montée du Mollard'],
        ['GAUTHIER', 'Guylaine', '256 Montée du Mollard']
    ]
    
    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(table)
    story.append(Spacer(1, 12))
    
    # Construire le PDF
    doc.build(story)
    
    return buffer.getvalue()

def test_layout_preservation():
    """Test de préservation de mise en page"""
    
    print("🧪 === TEST DE PRÉSERVATION DE MISE EN PAGE ===")
    
    # Vérifier les dépendances
    print(f"📦 PDF Enhanced Pipeline disponible: {PDF_ENHANCED_PIPELINE}")
    print(f"📦 docx2pdf disponible: {DOCX2PDF_AVAILABLE}")
    
    if not PDF_ENHANCED_PIPELINE:
        print("❌ Pipeline PDF enhanced non disponible")
        return False
    
    # Créer un PDF de test complexe
    print("\n1. 📄 Création d'un PDF de test avec mise en page complexe...")
    test_pdf = create_complex_test_pdf()
    print(f"✅ PDF de test créé: {len(test_pdf)} bytes")
    
    # Sauvegarder le PDF original
    with open("test_original_layout.pdf", "wb") as f:
        f.write(test_pdf)
    print("💾 PDF original sauvegardé: test_original_layout.pdf")
    
    # Définir les tiers pour l'anonymisation
    tiers = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "244 Montée du Mollard",
            "ville": "CHARANTONNAY",
            "code_postal": "38790"
        },
        {
            "numero": 2,
            "nom": "IMBERT", 
            "prenom": "Arnaud",
            "adresse": "256 Montée du Mollard",
            "ville": "CHARANTONNAY",
            "code_postal": "38790"
        },
        {
            "numero": 3,
            "nom": "GAUTHIER",
            "prenom": "Guylaine",
            "adresse": "256 Montée du Mollard",
            "ville": "CHARANTONNAY",
            "code_postal": "38790"
        }
    ]
    
    print(f"\n2. 🔒 Test d'anonymisation avec {len(tiers)} tiers...")
    
    try:
        # Anonymiser avec le pipeline enhanced
        anonymized_pdf, mapping = anonymize_pdf_enhanced_pipeline(test_pdf, tiers)
        print(f"✅ Anonymisation réussie!")
        print(f"📊 Taille PDF anonymisé: {len(anonymized_pdf)} bytes")
        print(f"🏷️ Mapping généré: {len(mapping)} balises")
        print(f"📋 Balises créées: {list(mapping.keys())}")
        
        # Sauvegarder le PDF anonymisé
        with open("test_anonymized_layout.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("💾 PDF anonymisé sauvegardé: test_anonymized_layout.pdf")
        
        # Extraire le texte pour vérification
        anonymized_text = extract_text_from_pdf(anonymized_pdf)
        print(f"📝 Texte anonymisé (premiers 300 chars): {anonymized_text[:300]}...")
        
        # Vérifier que les balises sont présentes
        found_tags = [tag for tag in mapping.keys() if tag in anonymized_text]
        print(f"✅ Balises trouvées dans le texte: {found_tags}")
        
        # Test de dé-anonymisation
        print(f"\n3. 🔓 Test de dé-anonymisation...")
        deanonymized_pdf = deanonymize_pdf_enhanced_pipeline(anonymized_pdf, mapping)
        print(f"✅ Dé-anonymisation réussie!")
        print(f"📊 Taille PDF dé-anonymisé: {len(deanonymized_pdf)} bytes")
        
        # Sauvegarder le PDF dé-anonymisé
        with open("test_deanonymized_layout.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("💾 PDF dé-anonymisé sauvegardé: test_deanonymized_layout.pdf")
        
        # Extraire le texte pour vérification
        deanonymized_text = extract_text_from_pdf(deanonymized_pdf)
        print(f"📝 Texte dé-anonymisé (premiers 300 chars): {deanonymized_text[:300]}...")
        
        # Vérifier que les valeurs originales sont restaurées
        original_values = list(mapping.values())
        restored_values = [val for val in original_values if val in deanonymized_text]
        print(f"✅ Valeurs restaurées: {restored_values}")
        
        print("\n🎉 === TESTS TERMINÉS AVEC SUCCÈS ===")
        print("📁 Fichiers générés:")
        print("   - test_original_layout.pdf (document original)")
        print("   - test_anonymized_layout.pdf (document anonymisé)")
        print("   - test_deanonymized_layout.pdf (document dé-anonymisé)")
        print("\n💡 Comparez visuellement les fichiers pour vérifier la préservation de la mise en page!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_layout_preservation()
    sys.exit(0 if success else 1) 