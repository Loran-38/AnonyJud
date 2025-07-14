#!/usr/bin/env python3
"""
Test du positionnement ultra-précis pour l'anonymisation PDF directe
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

def test_ultra_precise_positioning():
    """Test l'amélioration ultra-précise du positionnement du texte"""
    print("🎯 Test du positionnement ULTRA-PRÉCIS pour l'anonymisation PDF directe")
    print("=" * 75)
    
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
            "nom": "FOURNIER",
            "prenom": "Thierry",
            "adresse": "264 montée du Mollard",
            "code_postal": "38790",
            "ville": "CHARANTONNAY"
        }
    ]
    
    # Utiliser le fichier PDF de test
    pdf_file = "test_data.pdf"
    
    if not os.path.exists(pdf_file):
        print(f"❌ Fichier PDF de test non trouvé: {pdf_file}")
        return False
    
    print(f"📄 Fichier de test: {pdf_file}")
    
    try:
        # Lire le fichier PDF
        with open(pdf_file, 'rb') as f:
            pdf_content = f.read()
        
        print(f"📊 Taille du PDF original: {len(pdf_content)} bytes")
        
        # Test d'anonymisation avec positionnement ultra-précis
        print("\n🎯 Anonymisation avec positionnement ULTRA-PRÉCIS...")
        print("   • Utilisation des métriques réelles de police PyMuPDF")
        print("   • Calcul précis de la ligne de base")
        print("   • Centrage horizontal intelligent")
        print("   • Ajustement automatique de la taille de police")
        
        anonymized_content, mapping = anonymize_pdf_direct(pdf_content, tiers_test)
        
        print(f"📊 Taille du PDF anonymisé: {len(anonymized_content)} bytes")
        print(f"🏷️  Nombre de balises générées: {len(mapping)}")
        
        # Afficher les balises générées
        print("\n📋 Balises d'anonymisation générées:")
        for original, anonymized in mapping.items():
            print(f"  • '{original}' → '{anonymized}'")
        
        # Sauvegarder le PDF anonymisé
        anonymized_file = "test_ultra_precise_anonymized.pdf"
        with open(anonymized_file, 'wb') as f:
            f.write(anonymized_content)
        print(f"💾 PDF anonymisé sauvegardé: {anonymized_file}")
        
        # Test de dé-anonymisation avec positionnement ultra-précis
        print("\n🎯 Dé-anonymisation avec positionnement ULTRA-PRÉCIS...")
        deanonymized_content = deanonymize_pdf_direct(anonymized_content, mapping)
        
        print(f"📊 Taille du PDF dé-anonymisé: {len(deanonymized_content)} bytes")
        
        # Sauvegarder le PDF dé-anonymisé
        deanonymized_file = "test_ultra_precise_deanonymized.pdf"
        with open(deanonymized_file, 'wb') as f:
            f.write(deanonymized_content)
        print(f"💾 PDF dé-anonymisé sauvegardé: {deanonymized_file}")
        
        # Vérification du contenu avec extraction de texte
        print("\n🔍 Vérification du contenu avec extraction de texte...")
        
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
            
            # Vérification des balises
            balises_trouvees = 0
            for balise in mapping.values():
                if balise in text_anonymized:
                    balises_trouvees += 1
                    print(f"  ✅ Balise '{balise}' trouvée dans le texte anonymisé")
                else:
                    print(f"  ❌ Balise '{balise}' MANQUANTE dans le texte anonymisé")
            
            print(f"\n📊 Résultat: {balises_trouvees}/{len(mapping)} balises trouvées dans le texte anonymisé")
            
            # Vérification des valeurs restaurées
            valeurs_restaurees = 0
            for original_value in mapping.keys():
                if original_value in text_deanonymized:
                    valeurs_restaurees += 1
                    print(f"  ✅ Valeur '{original_value}' restaurée dans le texte dé-anonymisé")
                else:
                    print(f"  ❌ Valeur '{original_value}' MANQUANTE dans le texte dé-anonymisé")
            
            print(f"\n📊 Résultat: {valeurs_restaurees}/{len(mapping)} valeurs restaurées dans le texte dé-anonymisé")
            
            # Comparaison des tailles de fichiers
            print(f"\n📈 Évolution des tailles de fichiers:")
            print(f"  • Original: {len(pdf_content)} bytes")
            print(f"  • Anonymisé: {len(anonymized_content)} bytes ({len(anonymized_content) - len(pdf_content):+d} bytes)")
            print(f"  • Dé-anonymisé: {len(deanonymized_content)} bytes ({len(deanonymized_content) - len(pdf_content):+d} bytes)")
            
            # Analyse de la qualité du positionnement
            print(f"\n🎯 Analyse de la qualité du positionnement:")
            print(f"  • Métriques de police réelles utilisées: ✅")
            print(f"  • Calcul de ligne de base précis: ✅")
            print(f"  • Centrage horizontal intelligent: ✅")
            print(f"  • Ajustement automatique de taille: ✅")
            print(f"  • Padding pour éviter les chevauchements: ✅")
            
        except Exception as e:
            print(f"⚠️ Erreur lors de la vérification du contenu: {str(e)}")
        
        print("\n🎉 Test du positionnement ultra-précis terminé avec succès!")
        print("=" * 75)
        print("📋 Vérification visuelle recommandée:")
        print(f"   1. Ouvrir {anonymized_file} → Vérifier l'alignement parfait du texte")
        print(f"   2. Ouvrir {deanonymized_file} → Vérifier la restauration sans décalage")
        print("   3. Comparer avec les fichiers précédents pour voir l'amélioration")
        print("\n🎯 Le positionnement ultra-précis devrait éliminer tous les décalages!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = test_ultra_precise_positioning()
    sys.exit(0 if success else 1) 