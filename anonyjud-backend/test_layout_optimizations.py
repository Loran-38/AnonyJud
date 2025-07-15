#!/usr/bin/env python3
"""
Test des optimisations de mise en page pour le pipeline PDF → Word → PDF
Vérifie que les améliorations de conservation de mise en page fonctionnent correctement.
"""

import sys
import os
import logging
import tempfile
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.layout_optimizer import LayoutOptimizer, LayoutMetrics
from app.anonymizer import convert_pdf_to_word_enhanced, convert_word_to_pdf_enhanced

# Configuration des logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_test_pdf():
    """Crée un PDF de test avec une mise en page complexe"""
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER, TA_RIGHT
        from reportlab.lib import colors
        from reportlab.lib.units import inch
        from io import BytesIO
        
        # Créer un buffer pour le PDF
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4, 
                              rightMargin=72, leftMargin=72,
                              topMargin=72, bottomMargin=72)
        
        # Styles
        styles = getSampleStyleSheet()
        
        # Style titre
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )
        
        # Style sous-titre
        subtitle_style = ParagraphStyle(
            'CustomSubtitle',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=8,
            alignment=TA_LEFT,
            fontName='Helvetica-Bold'
        )
        
        # Style normal avec différentes polices
        normal_style = ParagraphStyle(
            'CustomNormal',
            parent=styles['Normal'],
            fontSize=11,
            leading=14,
            alignment=TA_JUSTIFY,
            fontName='Times-Roman'
        )
        
        # Style pour les adresses
        address_style = ParagraphStyle(
            'CustomAddress',
            parent=styles['Normal'],
            fontSize=10,
            leading=12,
            alignment=TA_LEFT,
            fontName='Courier'
        )
        
        story = []
        
        # Titre principal
        story.append(Paragraph("CONTRAT DE TRAVAIL", title_style))
        story.append(Spacer(1, 20))
        
        # Informations des parties
        story.append(Paragraph("ENTRE LES SOUSSIGNÉS :", subtitle_style))
        story.append(Spacer(1, 10))
        
        # Employeur
        story.append(Paragraph("L'employeur :", subtitle_style))
        story.append(Paragraph("SARL TECHNOLOGIES AVANCÉES<br/>"
                             "123 Avenue de l'Innovation<br/>"
                             "75001 Paris<br/>"
                             "Téléphone : 01 23 45 67 89<br/>"
                             "Email : contact@tech-avancees.fr", address_style))
        story.append(Spacer(1, 15))
        
        # Employé
        story.append(Paragraph("L'employé :", subtitle_style))
        story.append(Paragraph("Jean-Pierre MARTIN<br/>"
                             "Né le 15 mars 1985 à Lyon<br/>"
                             "Demeurant au 456 Rue de la Paix<br/>"
                             "69002 Lyon<br/>"
                             "Numéro de sécurité sociale : 1 85 03 15 123 456 78<br/>"
                             "Téléphone : 06 12 34 56 78<br/>"
                             "Email : jean-pierre.martin@email.com", address_style))
        story.append(Spacer(1, 20))
        
        # Tableau des conditions
        story.append(Paragraph("CONDITIONS D'EMPLOI :", subtitle_style))
        story.append(Spacer(1, 10))
        
        table_data = [
            ['Élément', 'Détail'],
            ['Poste', 'Développeur Full-Stack'],
            ['Date de début', '1er septembre 2024'],
            ['Lieu de travail', 'Paris (75)'],
            ['Salaire brut mensuel', '4 500 €'],
            ['Horaires', '35h/semaine'],
            ['Congés payés', '25 jours/an']
        ]
        
        table = Table(table_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
            ('FONTSIZE', (0, 1), (-1, -1), 10)
        ]))
        story.append(table)
        story.append(Spacer(1, 20))
        
        # Clause de confidentialité
        story.append(Paragraph("CLAUSE DE CONFIDENTIALITÉ :", subtitle_style))
        story.append(Paragraph("L'employé s'engage à respecter la confidentialité des informations "
                             "auxquelles il aura accès dans le cadre de ses fonctions. "
                             "Cette obligation de confidentialité s'applique pendant la durée "
                             "du contrat et après sa cessation.", normal_style))
        story.append(Spacer(1, 15))
        
        # Signature
        story.append(Paragraph("Fait à Paris, le 15 août 2024", normal_style))
        story.append(Spacer(1, 30))
        
        # Espaces pour signatures
        signature_table = Table([
            ['Signature employeur', 'Signature employé'],
            ['', ''],
            ['', '']
        ])
        signature_table.setStyle(TableStyle([
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('LINEBELOW', (0, 1), (-1, 1), 1, colors.black),
            ('LINEBELOW', (0, 2), (-1, 2), 1, colors.black)
        ]))
        story.append(signature_table)
        
        # Construire le PDF
        doc.build(story)
        
        # Récupérer le contenu
        pdf_content = buffer.getvalue()
        buffer.close()
        
        logger.info(f"✅ PDF de test créé avec succès. Taille: {len(pdf_content)} bytes")
        return pdf_content
        
    except Exception as e:
        logger.error(f"❌ Erreur lors de la création du PDF de test: {str(e)}")
        raise

def test_layout_optimizations():
    """Test complet des optimisations de mise en page"""
    logger.info("🚀 Début des tests d'optimisation de mise en page")
    
    try:
        # Créer un PDF de test
        logger.info("📄 Création du PDF de test...")
        test_pdf_content = create_test_pdf()
        
        # Créer l'optimiseur
        optimizer = LayoutOptimizer()
        
        # Test 1: Optimisation PDF → Word
        logger.info("🔄 Test 1: Optimisation PDF → Word")
        try:
            optimized_docx = optimizer.optimize_pdf_to_word_conversion(test_pdf_content)
            logger.info(f"✅ Test 1 réussi. Taille DOCX optimisé: {len(optimized_docx)} bytes")
        except Exception as e:
            logger.error(f"❌ Test 1 échoué: {str(e)}")
            return False
        
        # Test 2: Optimisation Word → PDF
        logger.info("🔄 Test 2: Optimisation Word → PDF")
        try:
            optimized_pdf = optimizer.optimize_word_to_pdf_conversion(optimized_docx)
            logger.info(f"✅ Test 2 réussi. Taille PDF optimisé: {len(optimized_pdf)} bytes")
        except Exception as e:
            logger.error(f"❌ Test 2 échoué: {str(e)}")
            return False
        
        # Test 3: Comparaison des mises en page
        logger.info("🔄 Test 3: Comparaison des mises en page")
        try:
            comparison = optimizer.compare_layouts(test_pdf_content, optimized_pdf)
            
            if "differences" in comparison:
                diff = comparison["differences"]
                preservation_score = diff.get("preservation_score", 0)
                
                logger.info(f"📊 Résultats de la comparaison:")
                logger.info(f"   - Score de préservation: {preservation_score:.2f}%")
                logger.info(f"   - Différence pages: {diff.get('page_count_diff', 0)}")
                logger.info(f"   - Différence blocs texte: {diff.get('text_blocks_diff', 0)}")
                logger.info(f"   - Différence taille police: {diff.get('font_size_diff', 0):.2f}")
                
                # Vérifier que le score de préservation est acceptable (> 70%)
                if preservation_score >= 70:
                    logger.info(f"✅ Test 3 réussi. Score de préservation excellent: {preservation_score:.2f}%")
                else:
                    logger.warning(f"⚠️ Test 3: Score de préservation faible: {preservation_score:.2f}%")
                    
            else:
                logger.error(f"❌ Test 3 échoué: Impossible de comparer les mises en page")
                return False
                
        except Exception as e:
            logger.error(f"❌ Test 3 échoué: {str(e)}")
            return False
        
        # Test 4: Test des fonctions intégrées
        logger.info("🔄 Test 4: Test des fonctions intégrées")
        try:
            # Test convert_pdf_to_word_enhanced
            docx_content = convert_pdf_to_word_enhanced(test_pdf_content)
            logger.info(f"✅ convert_pdf_to_word_enhanced réussi. Taille: {len(docx_content)} bytes")
            
            # Test convert_word_to_pdf_enhanced
            pdf_content = convert_word_to_pdf_enhanced(docx_content)
            logger.info(f"✅ convert_word_to_pdf_enhanced réussi. Taille: {len(pdf_content)} bytes")
            
        except Exception as e:
            logger.error(f"❌ Test 4 échoué: {str(e)}")
            return False
        
        logger.info("🎉 Tous les tests d'optimisation de mise en page ont réussi!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur générale lors des tests: {str(e)}")
        return False

def test_specific_optimizations():
    """Test des optimisations spécifiques"""
    logger.info("🔄 Test des optimisations spécifiques")
    
    try:
        # Créer un PDF de test
        test_pdf_content = create_test_pdf()
        optimizer = LayoutOptimizer()
        
        # Test du pré-traitement PDF
        logger.info("📄 Test du pré-traitement PDF...")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(test_pdf_content)
            temp_pdf_path = temp_pdf.name
        
        try:
            cleaned_pdf_path = optimizer._preprocess_pdf(temp_pdf_path)
            logger.info(f"✅ Pré-traitement PDF réussi: {cleaned_pdf_path}")
        finally:
            for path in [temp_pdf_path, cleaned_pdf_path]:
                if os.path.exists(path):
                    os.unlink(path)
        
        # Test de l'analyse de mise en page
        logger.info("📊 Test de l'analyse de mise en page...")
        metrics = optimizer._analyze_pdf_layout(test_pdf_content)
        logger.info(f"✅ Analyse mise en page réussie:")
        logger.info(f"   - Nombre de pages: {metrics.page_count}")
        logger.info(f"   - Nombre de blocs texte: {metrics.total_text_blocks}")
        logger.info(f"   - Taille moyenne police: {metrics.average_font_size:.2f}")
        logger.info(f"   - Nombre de polices différentes: {len(metrics.font_distribution)}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Erreur lors des tests spécifiques: {str(e)}")
        return False

if __name__ == "__main__":
    logger.info("🚀 Démarrage des tests d'optimisation de mise en page")
    
    # Test principal
    success_main = test_layout_optimizations()
    
    # Test des optimisations spécifiques
    success_specific = test_specific_optimizations()
    
    if success_main and success_specific:
        logger.info("🎉 Tous les tests ont réussi!")
        sys.exit(0)
    else:
        logger.error("❌ Certains tests ont échoué")
        sys.exit(1) 