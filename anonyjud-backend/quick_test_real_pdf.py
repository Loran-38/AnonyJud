#!/usr/bin/env python3
"""
Test rapide avec le fichier PDF réel p25-originale.pdf
Analyse le contenu et teste l'extraction d'éléments visuels
"""

import sys
import os
from pathlib import Path

# Ajouter le chemin de l'application
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def main():
    """Test rapide avec le fichier PDF réel"""
    
    print("=" * 60)
    print("🧪 TEST RAPIDE - FICHIER PDF RÉEL")
    print("=" * 60)
    
    # Localiser le fichier PDF
    pdf_path = Path(__file__).parent / "../anonyjud-app/Docs/fichiers tests/p25-originale.pdf"
    
    if not pdf_path.exists():
        print(f"❌ Fichier non trouvé: {pdf_path}")
        print("Veuillez vérifier le chemin du fichier p25-originale.pdf")
        return False
    
    print(f"✅ Fichier trouvé: {pdf_path}")
    print(f"📊 Taille: {pdf_path.stat().st_size} bytes")
    
    try:
        # Charger le fichier
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        print(f"✅ Fichier chargé en mémoire: {len(pdf_content)} bytes")
        
        # Analyser avec PyMuPDF
        print("\n🔍 ANALYSE AVEC PYMUPDF:")
        analyze_with_pymupdf(pdf_content)
        
        # Test du module PDFLayoutEnhancer
        print("\n🎨 TEST DU MODULE PDFLAYOUTENHANCER:")
        test_layout_enhancer(pdf_content, pdf_path.name)
        
        print("\n✅ Test rapide terminé avec succès!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")
        return False

def analyze_with_pymupdf(pdf_content):
    """Analyse le PDF avec PyMuPDF pour identifier son contenu"""
    try:
        import fitz
        
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        print(f"📄 Document PDF analysé:")
        print(f"   - Pages: {doc.page_count}")
        print(f"   - Titre: {doc.metadata.get('title', 'N/A')}")
        print(f"   - Auteur: {doc.metadata.get('author', 'N/A')}")
        print(f"   - Créateur: {doc.metadata.get('creator', 'N/A')}")
        
        total_images = 0
        total_text_blocks = 0
        has_tables = False
        has_graphics = False
        sample_text = ""
        
        for page_num in range(doc.page_count):
            page = doc[page_num]
            
            # Images
            images = page.get_images()
            total_images += len(images)
            
            # Texte
            text = page.get_text()
            if not sample_text and text.strip():
                sample_text = text[:200] + "..." if len(text) > 200 else text
            
            # Blocs de texte structurés
            text_dict = page.get_text("dict")
            total_text_blocks += len(text_dict.get("blocks", []))
            
            # Tableaux (si disponible)
            try:
                tables = page.find_tables()
                if tables:
                    has_tables = True
                    print(f"   - Page {page_num + 1}: {len(tables)} tableau(x) détecté(s)")
            except:
                pass
            
            # Graphiques vectoriels
            try:
                drawings = page.get_drawings()
                if drawings:
                    has_graphics = True
                    print(f"   - Page {page_num + 1}: {len(drawings)} élément(s) graphique(s)")
            except:
                pass
            
            if images:
                print(f"   - Page {page_num + 1}: {len(images)} image(s)")
        
        print(f"\n📊 Résumé du contenu:")
        print(f"   - Images totales: {total_images}")
        print(f"   - Blocs de texte: {total_text_blocks}")
        print(f"   - Tableaux détectés: {'Oui' if has_tables else 'Non'}")
        print(f"   - Graphiques vectoriels: {'Oui' if has_graphics else 'Non'}")
        
        if sample_text:
            print(f"\n📝 Échantillon de texte:")
            print(f"   {sample_text}")
        
        # Identifier les noms potentiels à anonymiser
        potential_names = []
        text_full = ""
        for page_num in range(doc.page_count):
            text_full += doc[page_num].get_text() + " "
        
        # Recherche de patterns typiques
        import re
        
        # Rechercher "HUISSOUD", "RIBEIRO", etc.
        name_patterns = [
            r'\bHUISSOU[D]?\b',
            r'\bRIBEIRO\b',
            r'\bIMBERT[-\s]*FOURNIER[-\s]*GAUTHIER\b',
            r'\bPyramide\s+avocats\b',
            r'304\s*Chemin\s*de\s*la\s*Poyat'
        ]
        
        for pattern in name_patterns:
            matches = re.findall(pattern, text_full, re.IGNORECASE)
            if matches:
                potential_names.extend(matches)
        
        if potential_names:
            print(f"\n🎯 Éléments potentiels à anonymiser détectés:")
            for name in set(potential_names):
                print(f"   - {name}")
        
        doc.close()
        
    except ImportError:
        print("❌ PyMuPDF (fitz) non disponible")
    except Exception as e:
        print(f"❌ Erreur lors de l'analyse: {str(e)}")

def test_layout_enhancer(pdf_content, filename):
    """Test du module PDFLayoutEnhancer"""
    try:
        from app.pdf_layout_enhancer import PDFLayoutEnhancer
        
        print("🚀 Initialisation du PDFLayoutEnhancer...")
        enhancer = PDFLayoutEnhancer()
        
        print("🎨 Extraction des éléments visuels...")
        visual_elements = enhancer.extract_visual_elements(pdf_content)
        
        print(f"✅ Extraction terminée:")
        print(f"   - Pages traitées: {len(visual_elements['pages'])}")
        
        total_images = 0
        total_tables = 0
        total_graphics = 0
        total_text_layouts = 0
        
        for i, page in enumerate(visual_elements['pages']):
            images = len(page['images'])
            tables = len(page['tables'])
            graphics = len(page['vector_graphics'])
            text_layouts = len(page['text_layout'])
            
            total_images += images
            total_tables += tables
            total_graphics += graphics
            total_text_layouts += text_layouts
            
            if images > 0 or tables > 0 or graphics > 0:
                print(f"   - Page {i+1}: {images} img, {tables} tab, {graphics} graph, {text_layouts} txt")
        
        print(f"\n📊 Totaux extraits:")
        print(f"   - Images: {total_images}")
        print(f"   - Tableaux: {total_tables}")
        print(f"   - Graphiques vectoriels: {total_graphics}")
        print(f"   - Structures de texte: {total_text_layouts}")
        
        # Test de la preuve de concept si des images sont présentes
        if total_images > 0:
            print("\n🧪 Test de la preuve de concept (extraction/réinjection d'images)...")
            try:
                from app.pdf_layout_enhancer import proof_of_concept_extract_reinject_images
                result_pdf = proof_of_concept_extract_reinject_images(pdf_content)
                
                # Sauvegarder
                base_name = os.path.splitext(filename)[0]
                output_path = f"{base_name}_PROOF_OF_CONCEPT_QUICK.pdf"
                
                with open(output_path, 'wb') as f:
                    f.write(result_pdf)
                
                print(f"✅ Preuve de concept sauvegardée: {output_path}")
                print(f"📊 Taille fichier généré: {len(result_pdf)} bytes")
                
            except Exception as e:
                print(f"⚠️ Erreur preuve de concept: {str(e)}")
        else:
            print("\n⚠️ Aucune image détectée, preuve de concept non applicable")
        
        # Nettoyer
        enhancer.cleanup_temp_files()
        print("🧹 Nettoyage des fichiers temporaires terminé")
        
    except ImportError as e:
        print(f"❌ Module PDFLayoutEnhancer non disponible: {str(e)}")
    except Exception as e:
        print(f"❌ Erreur lors du test: {str(e)}")

if __name__ == "__main__":
    success = main()
    print(f"\n{'='*60}")
    if success:
        print("🎉 TEST RAPIDE RÉUSSI")
        print("Le fichier PDF a été analysé avec succès!")
        print("Vous pouvez maintenant lancer le test complet avec:")
        print("   python test_layout_enhancement.py")
    else:
        print("❌ TEST RAPIDE ÉCHOUÉ")
        print("Vérifiez le chemin du fichier et les dépendances")
    print(f"{'='*60}")
    
    sys.exit(0 if success else 1) 