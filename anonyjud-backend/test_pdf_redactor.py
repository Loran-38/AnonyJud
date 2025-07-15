#!/usr/bin/env python3
"""
Test de la nouvelle fonction d'anonymisation PDF avec pdf-redactor.
Ce script compare les performances et la qualité de pdf-redactor 
avec les méthodes existantes.
"""

import sys
import os

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.anonymizer import anonymize_pdf_with_redactor, anonymize_pdf_enhanced_pipeline
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def test_pdf_redactor():
    """
    Test de la fonction d'anonymisation avec pdf-redactor.
    """
    print("🧪 Test de l'anonymisation PDF avec pdf-redactor")
    print("=" * 60)
    
    # Données de test avec des tiers
    tiers_test = [
        {
            "numero": 1,
            "nom": "HUISSOUD", 
            "prenom": "Louis",
            "adresse": "123 Rue de la Paix",
            "ville": "Paris",
            "code_postal": "75001",
            "telephone": "01 23 45 67 89",
            "email": "louis.huissoud@example.fr"
        },
        {
            "numero": 2,
            "nom": "MARTIN",
            "prenom": "Sophie", 
            "adresse": "456 Avenue des Champs",
            "ville": "Lyon",
            "code_postal": "69001",
            "telephone": "04 56 78 90 12",
            "email": "sophie.martin@test.com"
        },
        {
            "numero": 3,
            "nom": "BERNARD",
            "prenom": "Pierre",
            "adresse": "789 Boulevard Victor Hugo", 
            "ville": "Marseille",
            "code_postal": "13001",
            "telephone": "04 91 23 45 67",
            "email": "pierre.bernard@exemple.org"
        }
    ]
    
    # Créer un PDF de test simple
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from io import BytesIO
        
        # Créer un PDF de test avec les données des tiers
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Ajouter du contenu avec les informations des tiers
        y_position = 750
        c.setFont("Helvetica", 12)
        
        c.drawString(100, y_position, "DOCUMENT DE TEST - ANONYMISATION")
        y_position -= 40
        
        for i, tier in enumerate(tiers_test):
            c.drawString(100, y_position, f"Tiers {i+1}:")
            y_position -= 20
            c.drawString(120, y_position, f"Nom: {tier['nom']}")
            y_position -= 15
            c.drawString(120, y_position, f"Prénom: {tier['prenom']}")
            y_position -= 15
            c.drawString(120, y_position, f"Adresse: {tier['adresse']}")
            y_position -= 15
            c.drawString(120, y_position, f"Ville: {tier['ville']} {tier['code_postal']}")
            y_position -= 15
            c.drawString(120, y_position, f"Téléphone: {tier['telephone']}")
            y_position -= 15
            c.drawString(120, y_position, f"Email: {tier['email']}")
            y_position -= 30
        
        # Ajouter des données sensibles supplémentaires  
        c.drawString(100, y_position, "Données sensibles:")
        y_position -= 20
        c.drawString(120, y_position, "Date: 15/03/2024")
        y_position -= 15
        c.drawString(120, y_position, "NIR: 123456789012345")
        y_position -= 15
        c.drawString(120, y_position, "Carte: 1234 5678 9012 3456")
        y_position -= 15
        c.drawString(120, y_position, "Référence: AF-2024-001234")
        
        c.save()
        pdf_test_content = buffer.getvalue()
        buffer.close()
        
        print(f"📄 PDF de test créé: {len(pdf_test_content)} bytes")
        
        # Test 1: Anonymisation avec pdf-redactor
        print("\n🔍 Test 1: Anonymisation avec pdf-redactor")
        print("-" * 40)
        
        try:
            anonymized_pdf, mapping = anonymize_pdf_with_redactor(pdf_test_content, tiers_test)
            
            print(f"✅ Anonymisation pdf-redactor réussie!")
            print(f"📊 Taille original: {len(pdf_test_content)} bytes")
            print(f"📊 Taille anonymisé: {len(anonymized_pdf)} bytes")
            print(f"📊 Mapping généré: {len(mapping)} remplacements")
            print(f"📋 Clés du mapping: {list(mapping.keys())}")
            
            # Sauvegarder le résultat pour inspection
            with open("test_pdf_redactor_output.pdf", "wb") as f:
                f.write(anonymized_pdf)
            print("💾 Résultat sauvegardé: test_pdf_redactor_output.pdf")
            
        except Exception as e:
            print(f"❌ Erreur avec pdf-redactor: {str(e)}")
            import traceback
            traceback.print_exc()
        
        # Test 2: Comparaison avec la méthode pipeline existante
        print("\n🔍 Test 2: Comparaison avec pipeline existant")
        print("-" * 40)
        
        try:
            pipeline_pdf, pipeline_mapping = anonymize_pdf_enhanced_pipeline(pdf_test_content, tiers_test)
            
            print(f"✅ Anonymisation pipeline réussie!")
            print(f"📊 Taille pipeline: {len(pipeline_pdf)} bytes")
            print(f"📊 Mapping pipeline: {len(pipeline_mapping)} remplacements")
            
            # Sauvegarder pour comparaison
            with open("test_pipeline_output.pdf", "wb") as f:
                f.write(pipeline_pdf)
            print("💾 Pipeline sauvegardé: test_pipeline_output.pdf")
            
            # Comparaison des résultats
            print("\n📊 Comparaison des méthodes:")
            print(f"pdf-redactor: {len(anonymized_pdf)} bytes")
            print(f"Pipeline:     {len(pipeline_pdf)} bytes")
            
            diff_percent = ((len(anonymized_pdf) - len(pipeline_pdf)) / len(pipeline_pdf) * 100)
            print(f"Différence:   {diff_percent:+.1f}%")
            
        except Exception as e:
            print(f"⚠️ Erreur avec pipeline: {str(e)}")
        
        # Test 3: Vérification du contenu anonymisé
        print("\n🔍 Test 3: Vérification du contenu")
        print("-" * 40)
        
        try:
            import fitz  # PyMuPDF
            
            # Analyser le PDF anonymisé avec pdf-redactor
            doc = fitz.open(stream=anonymized_pdf, filetype="pdf")
            anonymized_text = ""
            for page in doc:
                anonymized_text += page.get_text()
            doc.close()
            
            print("📝 Contenu anonymisé (extrait):")
            print(anonymized_text[:500] + "..." if len(anonymized_text) > 500 else anonymized_text)
            
            # Vérifier que les données originales ont été remplacées
            originals_found = []
            anonymized_tags_found = []
            
            for tier in tiers_test:
                numero = tier.get('numero', 1)
                if tier.get('nom') and tier['nom'] in anonymized_text:
                    originals_found.append(tier['nom'])
                if f"NOM{numero}" in anonymized_text:
                    anonymized_tags_found.append(f"NOM{numero}")
                    
                if tier.get('prenom') and tier['prenom'] in anonymized_text:
                    originals_found.append(tier['prenom'])
                if f"PRENOM{numero}" in anonymized_text:
                    anonymized_tags_found.append(f"PRENOM{numero}")
            
            print(f"\n🔍 Résultats de l'anonymisation:")
            print(f"❌ Données originales encore visibles: {originals_found}")
            print(f"✅ Tags d'anonymisation trouvés: {anonymized_tags_found}")
            
            if not originals_found:
                print("🎉 SUCCÈS: Aucune donnée originale détectée!")
            else:
                print("⚠️ ATTENTION: Des données originales sont encore visibles!")
                
        except Exception as e:
            print(f"❌ Erreur lors de la vérification: {str(e)}")
        
    except ImportError as e:
        print(f"❌ Impossible de créer le PDF de test: {e}")
        return False
    
    except Exception as e:
        print(f"❌ Erreur générale: {str(e)}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✅ Test terminé!")
    return True

if __name__ == "__main__":
    test_pdf_redactor() 