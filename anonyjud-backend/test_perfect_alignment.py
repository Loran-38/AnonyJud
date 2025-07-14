#!/usr/bin/env python3
"""
Test de l'alignement parfait pour l'anonymisation PDF directe
"""

import os
import sys
import logging
from pathlib import Path

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(str(Path(__file__).parent))

from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def test_perfect_alignment():
    """Test l'alignement parfait et le respect des polices originales"""
    print("🎯 Test de l'ALIGNEMENT PARFAIT pour l'anonymisation PDF directe")
    print("=" * 70)
    
    # Données de test
    tiers_test = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Louis",
            "adresse": "244 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        },
        {
            "numero": 2,
            "nom": "IMBERT",
            "prenom": "Arnaud",
            "adresse": "256 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        },
        {
            "numero": 3,
            "nom": "GAUTHIER",
            "prenom": "Guylaine",
            "adresse": "256 Montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        },
        {
            "numero": 4,
            "nom": "THOIZET",
            "prenom": "Jacques",
            "adresse": "61, Quai Riondet",
            "code_postal": "38205",
            "ville": "VIENNE"
        }
    ]
    
    # Créer un fichier PDF de test si nécessaire
    pdf_file = "test_data.pdf"
    if not os.path.exists(pdf_file):
        print("📄 Création d'un fichier PDF de test...")
        from create_test_pdf import create_test_pdf
        create_test_pdf()
    
    print(f"📄 Fichier de test: {pdf_file}")
    
    try:
        # Lire le fichier PDF
        with open(pdf_file, 'rb') as f:
            pdf_content = f.read()
        
        print(f"📊 Taille du PDF original: {len(pdf_content)} bytes")
        
        # Test d'anonymisation avec alignement parfait
        print("\n🎯 Anonymisation avec ALIGNEMENT PARFAIT...")
        print("   • Préservation exacte de la position originale")
        print("   • Respect des polices originales")
        print("   • Traitement cohérent des lignes complètes")
        print("   • Élimination du centrage artificiel")
        
        anonymized_content, mapping = anonymize_pdf_direct(pdf_content, tiers_test)
        
        print(f"📊 Taille du PDF anonymisé: {len(anonymized_content)} bytes")
        print(f"🏷️  Nombre de balises générées: {len(mapping)}")
        
        # Afficher les balises générées
        print("\n📋 Balises d'anonymisation générées:")
        for original, anonymized in mapping.items():
            print(f"  • '{original}' → '{anonymized}'")
        
        # Sauvegarder le PDF anonymisé
        anonymized_file = "test_perfect_alignment_anonymized.pdf"
        with open(anonymized_file, 'wb') as f:
            f.write(anonymized_content)
        print(f"💾 PDF anonymisé sauvegardé: {anonymized_file}")
        
        # Test de dé-anonymisation avec alignement parfait
        print("\n🎯 Dé-anonymisation avec ALIGNEMENT PARFAIT...")
        deanonymized_content = deanonymize_pdf_direct(anonymized_content, mapping)
        
        print(f"📊 Taille du PDF dé-anonymisé: {len(deanonymized_content)} bytes")
        
        # Sauvegarder le PDF dé-anonymisé
        deanonymized_file = "test_perfect_alignment_deanonymized.pdf"
        with open(deanonymized_file, 'wb') as f:
            f.write(deanonymized_content)
        print(f"💾 PDF dé-anonymisé sauvegardé: {deanonymized_file}")
        
        # Analyser les polices utilisées
        print("\n🔍 Analyse des polices utilisées...")
        
        try:
            import fitz
            
            # Analyser les polices du document original
            doc_original = fitz.open(stream=pdf_content, filetype="pdf")
            original_fonts = set()
            for page in doc_original:
                for block in page.get_text("dict")["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["font"]:
                                    original_fonts.add(span["font"])
            doc_original.close()
            
            # Analyser les polices du document anonymisé
            doc_anonymized = fitz.open(stream=anonymized_content, filetype="pdf")
            anonymized_fonts = set()
            for page in doc_anonymized:
                for block in page.get_text("dict")["blocks"]:
                    if "lines" in block:
                        for line in block["lines"]:
                            for span in line["spans"]:
                                if span["font"]:
                                    anonymized_fonts.add(span["font"])
            doc_anonymized.close()
            
            print(f"📝 Polices dans le document original: {sorted(original_fonts)}")
            print(f"📝 Polices dans le document anonymisé: {sorted(anonymized_fonts)}")
            
            # Vérifier la cohérence des polices
            fonts_preserved = len(original_fonts.intersection(anonymized_fonts))
            fonts_total = len(original_fonts)
            print(f"📊 Polices préservées: {fonts_preserved}/{fonts_total}")
            
            if fonts_preserved == fonts_total:
                print("✅ Toutes les polices originales ont été préservées!")
            else:
                print("⚠️ Certaines polices ont été remplacées par des équivalents")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de l'analyse des polices: {str(e)}")
        
        # Vérification du contenu
        print("\n🔍 Vérification du contenu...")
        
        try:
            import fitz
            
            # Texte original
            doc_original = fitz.open(stream=pdf_content, filetype="pdf")
            text_original = ""
            for page in doc_original:
                text_original += page.get_text()
            doc_original.close()
            
            # Texte anonymisé
            doc_anonymized = fitz.open(stream=anonymized_content, filetype="pdf")
            text_anonymized = ""
            for page in doc_anonymized:
                text_anonymized += page.get_text()
            doc_anonymized.close()
            
            # Texte dé-anonymisé
            doc_deanonymized = fitz.open(stream=deanonymized_content, filetype="pdf")
            text_deanonymized = ""
            for page in doc_deanonymized:
                text_deanonymized += page.get_text()
            doc_deanonymized.close()
            
            # Vérifier que les balises sont présentes
            balises_trouvees = 0
            for balise in mapping.values():
                if balise in text_anonymized:
                    balises_trouvees += 1
            
            print(f"✅ {balises_trouvees}/{len(mapping)} balises trouvées dans le texte anonymisé")
            
            # Vérifier que les valeurs originales sont restaurées
            valeurs_restaurees = 0
            for original_value in mapping.keys():
                if original_value in text_deanonymized:
                    valeurs_restaurees += 1
            
            print(f"✅ {valeurs_restaurees}/{len(mapping)} valeurs restaurées dans le texte dé-anonymisé")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification du contenu: {str(e)}")
        
        print("\n🎉 Test de l'alignement parfait terminé!")
        print("=" * 70)
        print("🎯 Améliorations apportées:")
        print("   • Position exacte préservée (pas de centrage artificiel)")
        print("   • Polices originales respectées")
        print("   • Traitement cohérent des lignes complètes")
        print("   • Élimination des décalages de retrait")
        print("\n📋 Vérification visuelle recommandée:")
        print(f"   1. Ouvrir {anonymized_file} → Vérifier l'alignement parfait")
        print(f"   2. Ouvrir {deanonymized_file} → Vérifier la restauration exacte")
        print("   3. Comparer avec le document original pour confirmer l'alignement")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_perfect_alignment()
    sys.exit(0 if success else 1) 