#!/usr/bin/env python3
"""
Test direct de l'anonymisation avec amélioration de mise en page
Sans dépendance à requests - utilise directement les modules internes
"""

import sys
import os
from pathlib import Path
import json
import tempfile

# Ajouter le chemin de l'application
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_enhanced_anonymization_direct():
    """Test direct de l'anonymisation améliorée avec le fichier PDF réel"""
    
    print("=" * 70)
    print("🎨 TEST DIRECT - ANONYMISATION AVEC AMÉLIORATION DE MISE EN PAGE")
    print("=" * 70)
    
    # Localiser le fichier PDF
    pdf_path = Path(__file__).parent / "../anonyjud-app/Docs/fichiers tests/p25-originale.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Fichier non trouvé: {pdf_path}")
        return False
    
    print(f"✅ Fichier trouvé: {pdf_path}")
    
    try:
        # Charger le fichier
        with open(pdf_path, 'rb') as f:
            original_content = f.read()
        
        print(f"✅ Fichier chargé: {len(original_content)} bytes")
        
        # Données des tiers pour anonymisation
        tiers_data = [
            {
                "numero": 1,
                "nom": "HUISSOUD",
                "prenom": "Laurent",
                "adresse": "304 Chemin de la Poyat 38260 ORNACIEUX-BALBINS",
                "email": "laurent.douget@architecte-expert.com"
            },
            {
                "numero": 2,
                "nom": "IMBERT-FOURNIER-GAUTHIER",
                "prenom": "",
                "societe": "Pyramide avocats"
            },
            {
                "numero": 3,
                "nom": "RIBEIRO",
                "prenom": "",
                "societe": "MAÇONNERIE RIBEIRO"
            }
        ]
        
        print(f"👥 Tiers à anonymiser: {len(tiers_data)}")
        for i, tier in enumerate(tiers_data, 1):
            nom = tier.get('nom', 'N/A')
            prenom = tier.get('prenom', '')
            societe = tier.get('societe', '')
            print(f"   {i}. {nom} {prenom} {societe}")
        
        # ÉTAPE 1: Anonymisation classique
        print(f"\n🔒 ÉTAPE 1: Anonymisation du texte")
        try:
            from app.main import anonymize_pdf_secure_with_graphics
            
            anonymized_content, mapping = anonymize_pdf_secure_with_graphics(original_content, tiers_data)
            
            print(f"✅ Anonymisation réussie:")
            print(f"   - Taille fichier anonymisé: {len(anonymized_content)} bytes")
            print(f"   - Substitutions effectuées: {len(mapping)}")
            
            for tag, original in mapping.items():
                print(f"     {tag} ← {original}")
            
            # Sauvegarder le fichier anonymisé classique
            base_name = os.path.splitext(pdf_path.name)[0]
            anonymized_path = f"{base_name}_ANONYMISE_CLASSIQUE.pdf"
            
            with open(anonymized_path, 'wb') as f:
                f.write(anonymized_content)
            
            print(f"📄 Fichier anonymisé sauvegardé: {anonymized_path}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'anonymisation: {str(e)}")
            return False
        
        # ÉTAPE 2: Amélioration de la mise en page
        print(f"\n🎨 ÉTAPE 2: Amélioration de la mise en page")
        try:
            from app.pdf_layout_enhancer import enhance_pdf_layout_after_anonymization
            
            enhanced_content = enhance_pdf_layout_after_anonymization(original_content, anonymized_content)
            
            print(f"✅ Amélioration réussie:")
            print(f"   - Taille fichier amélioré: {len(enhanced_content)} bytes")
            print(f"   - Ratio de taille: {len(enhanced_content)/len(original_content):.2f}")
            
            # Sauvegarder le fichier amélioré
            enhanced_path = f"{base_name}_ANONYMISE_AMELIORE.pdf"
            
            with open(enhanced_path, 'wb') as f:
                f.write(enhanced_content)
            
            print(f"📄 Fichier amélioré sauvegardé: {enhanced_path}")
            
        except Exception as e:
            print(f"❌ Erreur lors de l'amélioration: {str(e)}")
            print(f"⚠️ Le fichier anonymisé classique reste disponible")
            return False
        
        # ÉTAPE 3: Analyse comparative
        print(f"\n📊 ÉTAPE 3: Analyse comparative")
        analyze_results(original_content, anonymized_content, enhanced_content, pdf_path.name)
        
        print(f"\n🎉 TEST COMPLET RÉUSSI !")
        print(f"📁 Fichiers générés:")
        print(f"   - {anonymized_path}")
        print(f"   - {enhanced_path}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        return False

def analyze_results(original_content, anonymized_content, enhanced_content, filename):
    """Analyse comparative des résultats"""
    try:
        import fitz
        
        print("🔍 Analyse comparative des PDFs:")
        
        # Analyser le PDF original
        original_doc = fitz.open(stream=original_content, filetype="pdf")
        original_images = 0
        original_text_blocks = 0
        
        for page_num in range(original_doc.page_count):
            page = original_doc[page_num]
            original_images += len(page.get_images())
            text_dict = page.get_text("dict")
            original_text_blocks += len(text_dict.get("blocks", []))
        
        original_doc.close()
        
        # Analyser le PDF anonymisé
        anon_doc = fitz.open(stream=anonymized_content, filetype="pdf")
        anon_images = 0
        anon_text_blocks = 0
        
        for page_num in range(anon_doc.page_count):
            page = anon_doc[page_num]
            anon_images += len(page.get_images())
            text_dict = page.get_text("dict")
            anon_text_blocks += len(text_dict.get("blocks", []))
        
        anon_doc.close()
        
        # Analyser le PDF amélioré
        enhanced_doc = fitz.open(stream=enhanced_content, filetype="pdf")
        enhanced_images = 0
        enhanced_text_blocks = 0
        
        for page_num in range(enhanced_doc.page_count):
            page = enhanced_doc[page_num]
            enhanced_images += len(page.get_images())
            text_dict = page.get_text("dict")
            enhanced_text_blocks += len(text_dict.get("blocks", []))
        
        enhanced_doc.close()
        
        print(f"📊 Comparaison des éléments:")
        print(f"   Format           | Images | Blocs Texte | Taille")
        print(f"   Original         |   {original_images:2d}   |     {original_text_blocks:2d}      | {len(original_content):6d}")
        print(f"   Anonymisé        |   {anon_images:2d}   |     {anon_text_blocks:2d}      | {len(anonymized_content):6d}")
        print(f"   Amélioré         |   {enhanced_images:2d}   |     {enhanced_text_blocks:2d}      | {len(enhanced_content):6d}")
        
        # Calcul des améliorations
        image_preservation = enhanced_images / original_images * 100 if original_images > 0 else 100
        text_preservation = enhanced_text_blocks / original_text_blocks * 100 if original_text_blocks > 0 else 100
        
        print(f"\n✅ Taux de préservation:")
        print(f"   - Images: {image_preservation:.1f}%")
        print(f"   - Structure texte: {text_preservation:.1f}%")
        
        if image_preservation >= 90 and text_preservation >= 90:
            print(f"🎉 Excellente préservation des éléments visuels!")
        elif image_preservation >= 70 and text_preservation >= 70:
            print(f"✅ Bonne préservation des éléments visuels")
        else:
            print(f"⚠️ Préservation partielle - amélioration possible")
        
    except Exception as e:
        print(f"⚠️ Erreur lors de l'analyse comparative: {str(e)}")

def test_module_components():
    """Test des composants individuels du module"""
    
    print("\n" + "-" * 50)
    print("🧪 TEST DES COMPOSANTS INDIVIDUELS")
    print("-" * 50)
    
    try:
        # Test 1: PDFLayoutEnhancer
        print("1. Test PDFLayoutEnhancer...")
        from app.pdf_layout_enhancer import PDFLayoutEnhancer
        enhancer = PDFLayoutEnhancer()
        print("   ✅ PDFLayoutEnhancer importé et initialisé")
        
        # Test 2: Fonctions d'anonymisation
        print("2. Test fonctions d'anonymisation...")
        from app.main import anonymize_pdf_secure_with_graphics
        print("   ✅ Fonctions d'anonymisation importées")
        
        # Test 3: Fonction utilitaire
        print("3. Test fonction utilitaire...")
        from app.pdf_layout_enhancer import enhance_pdf_layout_after_anonymization
        print("   ✅ Fonction utilitaire importée")
        
        # Test 4: Preuve de concept
        print("4. Test preuve de concept...")
        from app.pdf_layout_enhancer import proof_of_concept_extract_reinject_images
        print("   ✅ Preuve de concept importée")
        
        print("\n✅ Tous les composants sont disponibles!")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

def main():
    """Fonction principale"""
    
    print("🚀 DÉMARRAGE DES TESTS DIRECTS")
    print("=" * 70)
    
    # Test 1: Composants
    success1 = test_module_components()
    
    # Test 2: Anonymisation complète
    if success1:
        success2 = test_enhanced_anonymization_direct()
    else:
        success2 = False
        print("⚠️ Tests d'anonymisation ignorés car les composants ne sont pas disponibles")
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    print(f"Test des composants: {'✅ RÉUSSI' if success1 else '❌ ÉCHEC'}")
    print(f"Test anonymisation: {'✅ RÉUSSI' if success2 else '❌ ÉCHEC'}")
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS SONT PASSÉS !")
        print("La fonctionnalité d'amélioration de mise en page est opérationnelle.")
        print("\n📋 Prochaines étapes:")
        print("   1. Tester avec l'interface web")
        print("   2. Intégrer dans le frontend")
        print("   3. Optimiser les performances")
    else:
        print("\n⚠️ Certains tests ont échoué")
        print("Vérifiez les dépendances et la configuration")
    
    return success1 and success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 