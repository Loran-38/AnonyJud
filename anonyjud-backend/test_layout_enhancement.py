#!/usr/bin/env python3
"""
Script de test pour la fonctionnalité d'amélioration de mise en page PDF
Test avec le fichier PDF réel fourni par l'utilisateur
"""

import sys
import os
import requests
import json
from pathlib import Path

# Ajouter le chemin de l'application
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Chemin vers le fichier PDF de test
TEST_PDF_PATH = "../anonyjud-app/Docs/fichiers tests/p25-originale.pdf"

def load_test_pdf():
    """
    Charge le fichier PDF de test fourni par l'utilisateur
    """
    pdf_path = Path(__file__).parent / TEST_PDF_PATH
    
    if not pdf_path.exists():
        print(f"❌ Fichier PDF de test non trouvé: {pdf_path}")
        print("Assurez-vous que le fichier p25-originale.pdf est présent dans anonyjud-app/Docs/fichiers tests/")
        return None
    
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read()
        
        print(f"✅ Fichier PDF de test chargé: {pdf_path}")
        print(f"📊 Taille du fichier: {len(content)} bytes")
        return content, pdf_path.name
        
    except Exception as e:
        print(f"❌ Erreur lors du chargement du PDF: {str(e)}")
        return None

def analyze_pdf_content(pdf_content):
    """
    Analyse le contenu du PDF pour identifier les éléments visuels
    """
    try:
        import fitz  # PyMuPDF
        
        print("🔍 ANALYSE_PDF_CONTENT - Analyse du contenu du PDF")
        
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        analysis = {
            "pages": doc.page_count,
            "images": 0,
            "tables": 0,
            "text_blocks": 0,
            "has_graphics": False
        }
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Compter les images
            images = page.get_images()
            analysis["images"] += len(images)
            
            # Compter les tableaux
            try:
                tables = page.find_tables()
                analysis["tables"] += len(tables)
            except:
                pass  # Méthode peut ne pas être disponible sur toutes les versions
            
            # Compter les blocs de texte
            text_dict = page.get_text("dict")
            analysis["text_blocks"] += len(text_dict.get("blocks", []))
            
            # Vérifier les graphiques vectoriels
            try:
                drawings = page.get_drawings()
                if drawings:
                    analysis["has_graphics"] = True
            except:
                pass
        
        doc.close()
        
        print(f"📊 Analyse terminée:")
        print(f"   - Pages: {analysis['pages']}")
        print(f"   - Images: {analysis['images']}")
        print(f"   - Tableaux: {analysis['tables']}")
        print(f"   - Blocs de texte: {analysis['text_blocks']}")
        print(f"   - Graphiques vectoriels: {'Oui' if analysis['has_graphics'] else 'Non'}")
        
        return analysis
        
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")
        return None

def test_image_extraction_api_with_real_pdf():
    """
    Test de l'endpoint /test/extract-images avec le fichier PDF réel
    """
    print("🧪 TEST_IMAGE_EXTRACTION_API_REAL_PDF - Test avec PDF réel")
    
    # Charger le PDF de test
    pdf_data = load_test_pdf()
    if not pdf_data:
        return False
    
    pdf_content, filename = pdf_data
    
    # Analyser le contenu avant traitement
    analysis = analyze_pdf_content(pdf_content)
    if not analysis:
        print("⚠️ Impossible d'analyser le PDF, mais on continue le test")
    
    # URL de l'API
    api_url = "http://localhost:8000/test/extract-images"
    
    # Préparer la requête
    files = {
        'file': (filename, pdf_content, 'application/pdf')
    }
    
    try:
        print(f"📡 Envoi de la requête à {api_url}")
        response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            print("✅ Test réussi - PDF avec images extraites généré")
            
            # Sauvegarder le résultat
            base_name = os.path.splitext(filename)[0]
            output_path = f"{base_name}_TEST_IMAGES.pdf"
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"📄 Fichier sauvegardé: {output_path}")
            print(f"📊 Taille du fichier de sortie: {len(response.content)} bytes")
            
            # Comparer les tailles
            if len(response.content) > 0:
                print(f"📈 Ratio de taille: {len(response.content)/len(pdf_content):.2f}")
            
            return True
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est démarré sur localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test API: {str(e)}")
        return False

def test_enhanced_anonymization_api_with_real_pdf():
    """
    Test de l'endpoint /anonymize/pdf/enhanced avec le fichier PDF réel
    """
    print("🎨 TEST_ENHANCED_ANONYMIZATION_API_REAL_PDF - Test avec PDF réel")
    
    # Charger le PDF de test
    pdf_data = load_test_pdf()
    if not pdf_data:
        return False
    
    pdf_content, filename = pdf_data
    
    # Analyser le contenu avant traitement
    print("📋 Analyse du PDF avant anonymisation:")
    analysis = analyze_pdf_content(pdf_content)
    
    # URL de l'API
    api_url = "http://localhost:8000/anonymize/pdf/enhanced"
    
    # Données des tiers pour anonymisation basées sur le contenu probable du PDF
    # Ces données seront adaptées selon le contenu réel du PDF
    tiers_data = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Laurent",
            "adresse": "304 Chemin de la Poyat 38260 ORNACIEUX-BALBINS"
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
    
    # Préparer la requête
    files = {
        'file': (filename, pdf_content, 'application/pdf')
    }
    data = {
        'tiers_json': json.dumps(tiers_data)
    }
    
    try:
        print(f"📡 Envoi de la requête à {api_url}")
        print(f"👥 Tiers à anonymiser: {len(tiers_data)}")
        for i, tier in enumerate(tiers_data, 1):
            print(f"   {i}. {tier.get('nom', 'N/A')} {tier.get('prenom', '')}")
        
        response = requests.post(api_url, files=files, data=data)
        
        if response.status_code == 200:
            print("✅ Test réussi - PDF anonymisé avec mise en page améliorée")
            
            # Récupérer le mapping depuis les headers
            mapping_header = response.headers.get('X-Mapping')
            if mapping_header:
                mapping = json.loads(mapping_header)
                print(f"🗂️ Mapping généré ({len(mapping)} substitutions):")
                for tag, original in mapping.items():
                    print(f"   {tag} ← {original}")
            
            # Sauvegarder le résultat
            base_name = os.path.splitext(filename)[0]
            output_path = f"{base_name}_ANONYM_ENHANCED.pdf"
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"📄 Fichier sauvegardé: {output_path}")
            print(f"📊 Taille du fichier de sortie: {len(response.content)} bytes")
            
            # Analyser le résultat
            print("📋 Analyse du PDF après anonymisation:")
            result_analysis = analyze_pdf_content(response.content)
            
            if analysis and result_analysis:
                print("📊 Comparaison avant/après:")
                print(f"   Images: {analysis['images']} → {result_analysis['images']}")
                print(f"   Tableaux: {analysis['tables']} → {result_analysis['tables']}")
                print(f"   Blocs texte: {analysis['text_blocks']} → {result_analysis['text_blocks']}")
            
            return True
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est démarré sur localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test API: {str(e)}")
        return False

def test_direct_module_with_real_pdf():
    """
    Test direct du module PDFLayoutEnhancer avec le fichier PDF réel
    """
    print("🔧 TEST_DIRECT_MODULE_REAL_PDF - Test du module avec PDF réel")
    
    # Charger le PDF de test
    pdf_data = load_test_pdf()
    if not pdf_data:
        return False
    
    pdf_content, filename = pdf_data
    
    try:
        from app.pdf_layout_enhancer import PDFLayoutEnhancer
        
        print("📄 Test d'extraction des éléments visuels")
        
        # Tester l'extraction d'éléments
        enhancer = PDFLayoutEnhancer()
        visual_elements = enhancer.extract_visual_elements(pdf_content)
        
        print(f"🎨 Éléments visuels extraits du fichier réel:")
        print(f"   - Document: {filename}")
        print(f"   - Pages: {len(visual_elements['pages'])}")
        
        total_images = 0
        total_tables = 0
        total_graphics = 0
        
        for i, page in enumerate(visual_elements['pages']):
            images = len(page['images'])
            tables = len(page['tables'])
            graphics = len(page['vector_graphics'])
            
            total_images += images
            total_tables += tables
            total_graphics += graphics
            
            print(f"   - Page {i+1}: {images} images, {tables} tableaux, {graphics} graphiques, {len(page['text_layout'])} blocs texte")
        
        print(f"📊 Total:")
        print(f"   - Images: {total_images}")
        print(f"   - Tableaux: {total_tables}")
        print(f"   - Graphiques vectoriels: {total_graphics}")
        
        # Tester la preuve de concept si des images sont présentes
        if total_images > 0:
            print("🧪 Test de la preuve de concept d'extraction/réinjection")
            try:
                from app.pdf_layout_enhancer import proof_of_concept_extract_reinject_images
                result_pdf = proof_of_concept_extract_reinject_images(pdf_content)
                
                # Sauvegarder le résultat
                base_name = os.path.splitext(filename)[0]
                output_path = f"{base_name}_PROOF_OF_CONCEPT.pdf"
                
                with open(output_path, 'wb') as f:
                    f.write(result_pdf)
                
                print(f"✅ Preuve de concept sauvegardée: {output_path}")
                
            except Exception as e:
                print(f"⚠️ Erreur dans la preuve de concept: {str(e)}")
        
        # Nettoyer
        enhancer.cleanup_temp_files()
        
        print("✅ Test direct du module réussi avec fichier réel")
        return True
        
    except ImportError as e:
        print(f"❌ Erreur d'import: {str(e)}")
        print("Le module pdf_layout_enhancer n'est pas accessible")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test direct: {str(e)}")
        return False

def test_image_extraction_api():
    """
    Test de l'endpoint /test/extract-images via API REST avec PDF généré
    """
    print("🧪 TEST_IMAGE_EXTRACTION_API - Test avec PDF généré")
    
    # Créer un PDF de test simple avec du texte
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    import io
    
    # Créer un PDF de test
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    # Ajouter du texte
    c.setFont("Helvetica", 14)
    c.drawString(100, 750, "Document de test pour extraction d'images")
    c.drawString(100, 700, "Nom: Jean Dupont")
    c.drawString(100, 650, "Adresse: 123 Rue de la Paix, Paris")
    
    # Ajouter un rectangle comme élément graphique
    c.rect(100, 500, 200, 100, stroke=1, fill=0)
    c.drawString(120, 540, "Tableau de test")
    
    # Ajouter une ligne
    c.line(100, 450, 300, 450)
    
    c.save()
    test_pdf_content = buffer.getvalue()
    buffer.close()
    
    # URL de l'API (ajustez selon votre configuration)
    api_url = "http://localhost:8000/test/extract-images"
    
    # Préparer la requête
    files = {
        'file': ('test_document.pdf', test_pdf_content, 'application/pdf')
    }
    
    try:
        print(f"📡 Envoi de la requête à {api_url}")
        response = requests.post(api_url, files=files)
        
        if response.status_code == 200:
            print("✅ Test réussi - PDF généré")
            
            # Sauvegarder le résultat
            output_path = "test_result_images_generated.pdf"
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            print(f"📄 Fichier sauvegardé: {output_path}")
            print(f"📊 Taille du fichier: {len(response.content)} bytes")
            
            return True
            
        else:
            print(f"❌ Erreur API: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("Assurez-vous que le serveur FastAPI est démarré sur localhost:8000")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test API: {str(e)}")
        return False

def main():
    """
    Fonction principale de test
    """
    print("=" * 70)
    print("🧪 TESTS DE LA FONCTIONNALITÉ D'AMÉLIORATION DE MISE EN PAGE")
    print("📁 Utilisation du fichier PDF réel fourni par l'utilisateur")
    print("=" * 70)
    
    tests_results = []
    
    # Vérifier la présence du fichier PDF de test
    print(f"🔍 Vérification du fichier de test...")
    pdf_path = Path(__file__).parent / TEST_PDF_PATH
    print(f"📍 Chemin recherché: {pdf_path}")
    
    if pdf_path.exists():
        print(f"✅ Fichier PDF trouvé: {pdf_path.name}")
        use_real_pdf = True
    else:
        print(f"⚠️ Fichier PDF non trouvé, utilisation de PDFs générés pour les tests")
        use_real_pdf = False
    
    # Test 1: Module direct
    print("\n" + "-" * 50)
    print("TEST 1: Module direct")
    print("-" * 50)
    if use_real_pdf:
        result1 = test_direct_module_with_real_pdf()
    else:
        # Fallback vers le test original si pas de fichier réel
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        import io
        
        try:
            from app.pdf_layout_enhancer import PDFLayoutEnhancer
            
            buffer = io.BytesIO()
            c = canvas.Canvas(buffer, pagesize=A4)
            c.setFont("Helvetica", 14)
            c.drawString(100, 750, "Test direct du module")
            c.rect(100, 600, 200, 50, stroke=1, fill=0)
            c.save()
            test_content = buffer.getvalue()
            buffer.close()
            
            enhancer = PDFLayoutEnhancer()
            visual_elements = enhancer.extract_visual_elements(test_content)
            enhancer.cleanup_temp_files()
            result1 = True
            print("✅ Test direct du module réussi (PDF généré)")
        except Exception as e:
            print(f"❌ Erreur: {str(e)}")
            result1 = False
    
    tests_results.append(("Module direct", result1))
    
    # Test 2: API extraction d'images
    print("\n" + "-" * 50)
    print("TEST 2: API extraction d'images")
    print("-" * 50)
    if use_real_pdf:
        result2 = test_image_extraction_api_with_real_pdf()
    else:
        result2 = test_image_extraction_api()
    tests_results.append(("API extraction images", result2))
    
    # Test 3: API anonymisation améliorée
    print("\n" + "-" * 50)
    print("TEST 3: API anonymisation améliorée")
    print("-" * 50)
    if use_real_pdf:
        result3 = test_enhanced_anonymization_api_with_real_pdf()
    else:
        # Utiliser le test de fallback si pas de fichier réel
        result3 = False
        print("⚠️ Test non exécuté car aucun fichier PDF réel disponible")
    tests_results.append(("API anonymisation améliorée", result3))
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 70)
    
    success_count = 0
    for test_name, result in tests_results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHEC"
        print(f"{test_name}: {status}")
        if result:
            success_count += 1
    
    print(f"\n📈 Score: {success_count}/{len(tests_results)} tests réussis")
    
    if success_count == len(tests_results):
        print("🎉 Tous les tests sont passés avec succès!")
        print("La fonctionnalité d'amélioration de mise en page est opérationnelle.")
    elif success_count > 0:
        print("⚠️ Certains tests ont échoué.")
        print("Vérifiez la configuration et les dépendances.")
    else:
        print("❌ Tous les tests ont échoué.")
        print("Vérifiez l'installation et la configuration du système.")
    
    print(f"\n📁 Fichiers de sortie générés dans le répertoire courant:")
    output_files = [
        "p25-originale_TEST_IMAGES.pdf",
        "p25-originale_ANONYM_ENHANCED.pdf", 
        "p25-originale_PROOF_OF_CONCEPT.pdf",
        "test_result_images_generated.pdf"
    ]
    
    for file in output_files:
        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"   📄 {file} ({size} bytes)")
    
    return success_count == len(tests_results)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 