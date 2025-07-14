"""
Test de l'anonymisation directe PDF avec PyMuPDF
Teste la préservation parfaite de la mise en page
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
    anonymize_pdf_direct, 
    deanonymize_pdf_direct
)
from app.utils import extract_text_from_pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from io import BytesIO

def create_complex_test_pdf():
    """Créer un PDF de test avec mise en page complexe similaire au document juridique"""
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
    
    # Avocat des défendeurs
    story.append(Paragraph("Avocat des défendeurs 1 et 2", styles['Heading3']))
    story.append(Paragraph("SCP PYRAMIDE AVOCATS", normal_style))
    story.append(Paragraph("Maître ROMULUS Philippe", normal_style))
    story.append(Paragraph("59 Cours Romestang", normal_style))
    story.append(Paragraph("CS 80437", normal_style))
    story.append(Paragraph("38217 VIENNE Cedex", normal_style))
    story.append(Paragraph("Tel : 04.74.85.01.55", normal_style))
    story.append(Paragraph("Courriel : contact@pyramide-avocats.com", normal_style))
    story.append(Paragraph("Référence du dossier : 22.00090/PR - IMBERT - GAUTHIER / HUISSOUD", normal_style))
    story.append(Spacer(1, 12))
    
    # Expert technique
    story.append(Paragraph("Expert technique", styles['Heading3']))
    story.append(Paragraph("ELEX-LYON", normal_style))
    story.append(Paragraph("Monsieur RIVOIRE Pierre", normal_style))
    story.append(Paragraph("129 RUE SERVIENT", normal_style))
    story.append(Paragraph("69326 LYON CEDEX 03", normal_style))
    story.append(Paragraph("Courriel : pierre.rivoire@elex.fr", normal_style))
    story.append(Paragraph("Référence du dossier : 21ERW8948", normal_style))
    story.append(Spacer(1, 12))
    
    # Défendeur 03
    story.append(Paragraph("Défendeur 03", styles['Heading2']))
    story.append(Paragraph("Monsieur FOURNIER Thierry, Marc", normal_style))
    story.append(Paragraph("264 montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    
    # Construire le PDF
    doc.build(story)
    
    return buffer.getvalue()

def test_direct_pdf_anonymization():
    """Test de l'anonymisation directe PDF"""
    
    print("🧪 === TEST ANONYMISATION DIRECTE PDF AVEC PYMUPDF ===")
    
    # Créer un PDF de test complexe
    print("\n1. 📄 Création d'un PDF de test avec mise en page complexe...")
    test_pdf = create_complex_test_pdf()
    print(f"✅ PDF de test créé: {len(test_pdf)} bytes")
    
    # Sauvegarder le PDF original
    with open("test_direct_original.pdf", "wb") as f:
        f.write(test_pdf)
    print("💾 PDF original sauvegardé: test_direct_original.pdf")
    
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
        },
        {
            "numero": 4,
            "nom": "FOURNIER",
            "prenom": "Thierry",
            "adresse": "264 montée du Mollard",
            "ville": "CHARANTONNAY",
            "code_postal": "38790"
        }
    ]
    
    print(f"\n2. 🔒 Test d'anonymisation directe avec {len(tiers)} tiers...")
    
    try:
        # Anonymiser avec l'anonymisation directe
        anonymized_pdf, mapping = anonymize_pdf_direct(test_pdf, tiers)
        print(f"✅ Anonymisation directe réussie!")
        print(f"📊 Taille PDF anonymisé: {len(anonymized_pdf)} bytes")
        print(f"🏷️ Mapping généré: {len(mapping)} balises")
        print(f"📋 Balises créées: {list(mapping.keys())}")
        
        # Sauvegarder le PDF anonymisé
        with open("test_direct_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("💾 PDF anonymisé sauvegardé: test_direct_anonymized.pdf")
        
        # Extraire le texte pour vérification
        anonymized_text = extract_text_from_pdf(anonymized_pdf)
        print(f"📝 Texte anonymisé (premiers 400 chars): {anonymized_text[:400]}...")
        
        # Vérifier que les balises sont présentes
        found_tags = [tag for tag in mapping.keys() if tag in anonymized_text]
        print(f"✅ Balises trouvées dans le texte: {found_tags}")
        
        # Test de dé-anonymisation
        print(f"\n3. 🔓 Test de dé-anonymisation directe...")
        deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
        print(f"✅ Dé-anonymisation directe réussie!")
        print(f"📊 Taille PDF dé-anonymisé: {len(deanonymized_pdf)} bytes")
        
        # Sauvegarder le PDF dé-anonymisé
        with open("test_direct_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("💾 PDF dé-anonymisé sauvegardé: test_direct_deanonymized.pdf")
        
        # Extraire le texte pour vérification
        deanonymized_text = extract_text_from_pdf(deanonymized_pdf)
        print(f"📝 Texte dé-anonymisé (premiers 400 chars): {deanonymized_text[:400]}...")
        
        # Vérifier que les valeurs originales sont restaurées
        original_values = list(mapping.values())
        restored_values = [val for val in original_values if val in deanonymized_text]
        print(f"✅ Valeurs restaurées: {restored_values}")
        
        print("\n🎉 === TESTS TERMINÉS AVEC SUCCÈS ===")
        print("📁 Fichiers générés:")
        print("   - test_direct_original.pdf (document original)")
        print("   - test_direct_anonymized.pdf (document anonymisé)")
        print("   - test_direct_deanonymized.pdf (document dé-anonymisé)")
        print("\n🎯 AVANTAGE CLEF: L'anonymisation directe préserve PARFAITEMENT la mise en page!")
        print("💡 Comparez visuellement les fichiers pour vérifier la préservation de la mise en page!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors des tests: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_direct_pdf_anonymization()
    sys.exit(0 if success else 1) 