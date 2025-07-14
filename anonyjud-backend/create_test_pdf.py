#!/usr/bin/env python3
"""
Création d'un fichier PDF de test pour tester l'amélioration du positionnement
"""

from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def create_test_pdf():
    """Crée un PDF de test avec du contenu similaire aux images fournies"""
    
    filename = "test_data.pdf"
    doc = SimpleDocTemplate(filename, pagesize=A4, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=14,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=12,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold'
    )
    
    normal_style = ParagraphStyle(
        'CustomNormal',
        parent=styles['Normal'],
        fontSize=10,
        spaceAfter=6,
        fontName='Helvetica'
    )
    
    # Contenu du document
    story = []
    
    # Titre principal
    story.append(Paragraph("Références des Parties", title_style))
    story.append(Spacer(1, 12))
    
    # Partie Demanderesse
    story.append(Paragraph("Partie Demanderesse", heading_style))
    
    story.append(Paragraph("Demandeur 1", normal_style))
    story.append(Paragraph("Monsieur HUISSOUD Louis", normal_style))
    story.append(Paragraph("244 Montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Avocat du demandeur", normal_style))
    story.append(Paragraph("SCP THOIZET & Associés", normal_style))
    story.append(Paragraph("Me Jacques THOIZET", normal_style))
    story.append(Paragraph("61, Quai Riondet", normal_style))
    story.append(Paragraph("BP 374", normal_style))
    story.append(Paragraph("38205 VIENNE cedex", normal_style))
    story.append(Paragraph("Tel : 04.74.53.70.00", normal_style))
    story.append(Paragraph("Courriel : avocat.thoizet@gmail.com / avocat.thoizet@gmail.com", normal_style))
    story.append(Paragraph("Référence du dossier : 22.0003-HUISSOUD/IMBERT-GAUTHIER-MAAF-MATMUT", normal_style))
    story.append(Spacer(1, 20))
    
    # Partie Défenderesse
    story.append(Paragraph("Partie Défenderesse", heading_style))
    
    story.append(Paragraph("Défendeur 01", normal_style))
    story.append(Paragraph("Monsieur IMBERT Arnaud", normal_style))
    story.append(Paragraph("256 Montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Défendeur 02", normal_style))
    story.append(Paragraph("Madame GAUTHIER Guylaine", normal_style))
    story.append(Paragraph("256 Montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Avocat des défendeurs 1 et 2", normal_style))
    story.append(Paragraph("SCP PYRAMIDE AVOCATS", normal_style))
    story.append(Paragraph("Maître ROMULUS Philippe", normal_style))
    story.append(Paragraph("59 Cours Romestang", normal_style))
    story.append(Paragraph("CS 80437", normal_style))
    story.append(Paragraph("38217 VIENNE Cedex", normal_style))
    story.append(Paragraph("Tel : 04.74.85.01.55", normal_style))
    story.append(Paragraph("Courriel : contact@pyramide-avocats.com", normal_style))
    story.append(Paragraph("Référence du dossier : 22.00090/PR - IMBERT - GAUTHIER / HUISSOUD", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Expert technique", normal_style))
    story.append(Paragraph("ELEX-LYON", normal_style))
    story.append(Paragraph("Monsieur RIVOIRE Pierre", normal_style))
    story.append(Paragraph("129 RUE SERVIENT", normal_style))
    story.append(Paragraph("69326 LYON CEDEX 03", normal_style))
    story.append(Paragraph("Courriel : pierre.rivoire@elex.fr", normal_style))
    story.append(Paragraph("Référence du dossier : 21ERW8948", normal_style))
    story.append(Spacer(1, 12))
    
    story.append(Paragraph("Défendeur 03", normal_style))
    story.append(Paragraph("Monsieur FOURNIER Thierry, Marc", normal_style))
    story.append(Paragraph("264 montée du Mollard", normal_style))
    story.append(Paragraph("38790 CHARANTONNAY", normal_style))
    
    # Construire le PDF
    doc.build(story)
    print(f"✅ PDF de test créé: {filename}")
    return filename

if __name__ == "__main__":
    create_test_pdf() 