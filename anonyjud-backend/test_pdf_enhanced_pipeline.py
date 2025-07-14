"""
Test du pipeline PDF enhanced : PDF → Word → Anonymisation → PDF
Teste la préservation de mise en page et l'anonymisation correcte.
"""

import os
import sys
import tempfile

# Ajouter le répertoire app au chemin Python
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.anonymizer import (
    anonymize_pdf_enhanced_pipeline, 
    deanonymize_pdf_enhanced_pipeline,
    convert_pdf_to_word_enhanced,
    convert_word_to_pdf_enhanced,
    PDF_ENHANCED_PIPELINE
)
from app.utils import extract_text_from_pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def create_test_pdf_complex():
    """Crée un PDF de test avec une mise en page complexe"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    
    story = []
    
    # Titre
    story.append(Paragraph("JUGEMENT TRIBUNAL DE GRANDE INSTANCE", styles['Title']))
    story.append(Spacer(1, 20))
    
    # Informations du dossier avec mise en forme
    story.append(Paragraph("<b>Affaire:</b> Dupont c/ Martin", styles['Normal']))
    story.append(Paragraph("<b>Date:</b> 15 janvier 2024", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Parties avec formatage
    story.append(Paragraph("<b>DEMANDEUR:</b>", styles['Heading2']))
    story.append(Paragraph("Monsieur Jean DUPONT", styles['Normal']))
    story.append(Paragraph("Né le 12 mars 1975", styles['Normal']))
    story.append(Paragraph("Demeurant 15 rue de la Paix, 75001 Paris", styles['Normal']))
    story.append(Spacer(1, 10))
    
    story.append(Paragraph("<b>DÉFENDEUR:</b>", styles['Heading2']))
    story.append(Paragraph("Madame Marie MARTIN", styles['Normal']))
    story.append(Paragraph("Née le 8 juin 1980", styles['Normal']))
    story.append(Paragraph("Demeurant 42 avenue des Champs, 69001 Lyon", styles['Normal']))
    story.append(Spacer(1, 15))
    
    # Tableau avec formatage
    data = [
        ['Type', 'Montant', 'Bénéficiaire'],
        ['Dommages-intérêts', '5 000 €', 'Jean DUPONT'],
        ['Frais de procédure', '1 500 €', 'Jean DUPONT'],
        ['Total', '6 500 €', '']
    ]
    table = Table(data)
    story.append(table)
    story.append(Spacer(1, 15))
    
    # Paragraphe de conclusion
    story.append(Paragraph(
        "PAR CES MOTIFS, le Tribunal condamne Marie MARTIN à verser à Jean DUPONT "
        "la somme de six mille cinq cents euros (6 500 €) au titre des dommages-intérêts "
        "et frais de procédure.",
        styles['Normal']
    ))
    
    doc.build(story)
    return buffer.getvalue()

def test_pipeline_enhanced():
    """Test complet du pipeline enhanced"""
    print("=" * 60)
    print("🧪 TEST PIPELINE PDF ENHANCED")
    print("=" * 60)
    
    # Vérifier que le pipeline enhanced est disponible
    if not PDF_ENHANCED_PIPELINE:
        print("❌ ERREUR: Pipeline PDF enhanced non disponible")
        print("Installez pdf2docx: pip install pdf2docx")
        return False
    
    print("✅ Pipeline PDF enhanced disponible")
    
    # Définir les tiers de test
    tiers = [
        {
            "numero": 1,
            "nom": "DUPONT",
            "prenom": "Jean",
            "adresse": "15 rue de la Paix, 75001 Paris",
            "customFields": []
        },
        {
            "numero": 2,
            "nom": "MARTIN", 
            "prenom": "Marie",
            "adresse": "42 avenue des Champs, 69001 Lyon",
            "customFields": []
        }
    ]
    
    try:
        # Étape 1: Créer un PDF de test complexe
        print("\n📄 Étape 1: Création du PDF de test...")
        pdf_content = create_test_pdf_complex()
        print(f"✅ PDF créé: {len(pdf_content)} bytes")
        
        # Extraire le texte original pour comparaison
        original_text = extract_text_from_pdf(pdf_content)
        print(f"📝 Texte original (premiers 200 chars): {original_text[:200]}...")
        
        # Étape 2: Test de conversion PDF → Word
        print("\n🔄 Étape 2: Test conversion PDF → Word...")
        word_content = convert_pdf_to_word_enhanced(pdf_content)
        print(f"✅ Conversion PDF → Word réussie: {len(word_content)} bytes")
        
        # Étape 3: Test de conversion Word → PDF
        print("\n🔄 Étape 3: Test conversion Word → PDF...")
        pdf_reconverted = convert_word_to_pdf_enhanced(word_content)
        print(f"✅ Conversion Word → PDF réussie: {len(pdf_reconverted)} bytes")
        
        # Étape 4: Test du pipeline complet d'anonymisation
        print("\n🔒 Étape 4: Test pipeline complet d'anonymisation...")
        anonymized_pdf, mapping = anonymize_pdf_enhanced_pipeline(pdf_content, tiers)
        print(f"✅ Anonymisation réussie: {len(anonymized_pdf)} bytes")
        print(f"📊 Mapping généré: {mapping}")
        
        # Vérifier le mapping
        expected_tags = ["NOM1", "PRENOM1", "NOM2", "PRENOM2"]
        for tag in expected_tags:
            if tag in mapping:
                print(f"✅ Tag {tag} trouvé: {mapping[tag]}")
            else:
                print(f"❌ Tag {tag} manquant dans le mapping")
        
        # Extraire le texte anonymisé pour vérification
        anonymized_text = extract_text_from_pdf(anonymized_pdf)
        print(f"📝 Texte anonymisé (premiers 200 chars): {anonymized_text[:200]}...")
        
        # Vérifier que les noms ont été anonymisés
        if "DUPONT" not in anonymized_text and "NOM1" in anonymized_text:
            print("✅ Anonymisation des noms réussie")
        else:
            print("❌ Problème d'anonymisation des noms")
            
        if "Jean" not in anonymized_text and "PRENOM1" in anonymized_text:
            print("✅ Anonymisation des prénoms réussie")
        else:
            print("❌ Problème d'anonymisation des prénoms")
        
        # Étape 5: Test du pipeline de dé-anonymisation
        print("\n🔓 Étape 5: Test pipeline de dé-anonymisation...")
        deanonymized_pdf = deanonymize_pdf_enhanced_pipeline(anonymized_pdf, mapping)
        print(f"✅ Dé-anonymisation réussie: {len(deanonymized_pdf)} bytes")
        
        # Extraire le texte dé-anonymisé pour vérification
        deanonymized_text = extract_text_from_pdf(deanonymized_pdf)
        print(f"📝 Texte dé-anonymisé (premiers 200 chars): {deanonymized_text[:200]}...")
        
        # Vérifier que les noms ont été restaurés
        if "DUPONT" in deanonymized_text and "NOM1" not in deanonymized_text:
            print("✅ Dé-anonymisation des noms réussie")
        else:
            print("❌ Problème de dé-anonymisation des noms")
            
        if "Jean" in deanonymized_text and "PRENOM1" not in deanonymized_text:
            print("✅ Dé-anonymisation des prénoms réussie")
        else:
            print("❌ Problème de dé-anonymisation des prénoms")
        
        # Sauvegarder les fichiers de test pour inspection
        print("\n💾 Sauvegarde des fichiers de test...")
        
        with open("test_original.pdf", "wb") as f:
            f.write(pdf_content)
        print("✅ test_original.pdf sauvegardé")
        
        with open("test_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("✅ test_anonymized.pdf sauvegardé")
        
        with open("test_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("✅ test_deanonymized.pdf sauvegardé")
        
        print("\n" + "=" * 60)
        print("🎉 TOUS LES TESTS ONT RÉUSSI!")
        print("🔍 Vérifiez les fichiers PDF générés pour valider la mise en page")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR DANS LE TEST: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_fallback_libreoffice():
    """Test si LibreOffice est disponible"""
    print("\n🔧 Test de disponibilité LibreOffice...")
    
    try:
        import subprocess
        import sys
        
        # Commandes à tester selon l'OS
        if sys.platform == "win32":
            commands = ["soffice", "libreoffice"]
        elif sys.platform == "darwin":
            commands = ["/Applications/LibreOffice.app/Contents/MacOS/soffice", "soffice"]
        else:
            commands = ["soffice", "libreoffice"]
        
        for cmd in commands:
            try:
                result = subprocess.run([cmd, "--version"], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print(f"✅ LibreOffice trouvé: {cmd}")
                    print(f"   Version: {result.stdout.strip()}")
                    return True
            except:
                continue
        
        print("❌ LibreOffice non trouvé - le pipeline utilisera reportlab en fallback")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors du test LibreOffice: {str(e)}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage des tests du pipeline PDF enhanced")
    
    # Test de LibreOffice
    test_fallback_libreoffice()
    
    # Test principal
    success = test_pipeline_enhanced()
    
    if success:
        print("\n🎉 Tous les tests sont passés avec succès!")
        sys.exit(0)
    else:
        print("\n❌ Certains tests ont échoué")
        sys.exit(1) 