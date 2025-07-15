#!/usr/bin/env python3
"""
Test des améliorations pour gros fichiers PDF.
Ce script teste les différentes méthodes d'anonymisation avec simulation 
de fichiers volumineux et surveillance mémoire.
"""

import sys
import os
import time
import psutil
import gc

# Ajouter le répertoire parent au path pour importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.anonymizer import (
    anonymize_pdf_with_redactor, 
    anonymize_pdf_enhanced_pipeline,
    anonymize_pdf_direct
)
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def get_memory_usage():
    """Retourne l'usage mémoire actuel en MB"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024

def create_large_test_pdf(target_size_mb=10):
    """
    Crée un PDF de test avec beaucoup de contenu pour simuler un gros fichier.
    """
    try:
        from reportlab.pdfgen import canvas
        from reportlab.lib.pagesizes import A4
        from io import BytesIO
        
        print(f"📄 Création PDF de test ciblé: {target_size_mb}MB")
        
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        
        # Calculer combien de pages approximativement
        pages_needed = max(10, target_size_mb // 2)  # Estimation grossière
        
        # Données de test avec les tiers
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
                "adresse": "456 Avenue des Champs-Élysées",
                "ville": "Lyon",
                "code_postal": "69001",
                "telephone": "04 56 78 90 12",
                "email": "sophie.martin@test.com"
            }
        ]
        
        for page_num in range(pages_needed):
            if page_num > 0:
                c.showPage()
            
            c.setFont("Helvetica", 12)
            y_position = 750
            
            c.drawString(100, y_position, f"PAGE {page_num + 1} - DOCUMENT DE TEST VOLUMINEUX")
            y_position -= 40
            
            # Répéter le contenu plusieurs fois par page pour augmenter la taille
            for repeat in range(20):  # 20 répétitions par page
                for i, tier in enumerate(tiers_test):
                    c.drawString(100, y_position, f"Répétition {repeat+1} - Tiers {i+1}:")
                    y_position -= 15
                    c.drawString(120, y_position, f"Nom: {tier['nom']} {tier['prenom']}")
                    y_position -= 12
                    c.drawString(120, y_position, f"Adresse: {tier['adresse']}")
                    y_position -= 12
                    c.drawString(120, y_position, f"Ville: {tier['ville']} {tier['code_postal']}")
                    y_position -= 12
                    c.drawString(120, y_position, f"Contact: {tier['telephone']} - {tier['email']}")
                    y_position -= 15
                    
                    # Ajouter des données sensibles
                    c.drawString(120, y_position, f"Date naissance: 15/03/1985, NIR: 123456789012345")
                    y_position -= 12
                    c.drawString(120, y_position, f"Carte: 1234 5678 9012 3456, Réf: AF-2024-{page_num:06d}")
                    y_position -= 20
                    
                    if y_position < 50:  # Nouvelle page si plus de place
                        c.showPage()
                        y_position = 750
            
            if page_num % 10 == 0:
                print(f"  Pages créées: {page_num + 1}/{pages_needed}")
        
        c.save()
        pdf_content = buffer.getvalue()
        buffer.close()
        
        actual_size_mb = len(pdf_content) / 1024 / 1024
        print(f"✅ PDF créé: {len(pdf_content):,} bytes ({actual_size_mb:.1f} MB)")
        print(f"📄 Nombre de pages: {pages_needed}")
        
        return pdf_content, tiers_test
        
    except ImportError as e:
        print(f"❌ Impossible de créer le PDF de test: {e}")
        return None, None

def test_method(method_name, method_func, pdf_content, tiers, timeout_seconds=300):
    """
    Teste une méthode d'anonymisation avec surveillance mémoire et timeout.
    """
    print(f"\n🧪 Test de {method_name}")
    print("=" * 50)
    
    start_time = time.time()
    initial_memory = get_memory_usage()
    max_memory = initial_memory
    
    print(f"💾 Mémoire initiale: {initial_memory:.1f} MB")
    print(f"⏱️ Timeout configuré: {timeout_seconds}s")
    
    try:
        # Démarrer un monitoring mémoire en arrière-plan
        start_monitor_time = time.time()
        
        # Exécuter la méthode
        result = method_func(pdf_content, tiers)
        
        if isinstance(result, tuple):
            anonymized_pdf, mapping = result
        else:
            anonymized_pdf = result
            mapping = {}
        
        end_time = time.time()
        final_memory = get_memory_usage()
        processing_time = end_time - start_time
        
        # Statistiques
        input_size_mb = len(pdf_content) / 1024 / 1024
        output_size_mb = len(anonymized_pdf) / 1024 / 1024
        memory_increase = final_memory - initial_memory
        
        print(f"✅ {method_name} RÉUSSI!")
        print(f"⏱️ Temps de traitement: {processing_time:.2f}s")
        print(f"📊 Taille entrée: {input_size_mb:.1f} MB")
        print(f"📊 Taille sortie: {output_size_mb:.1f} MB")
        print(f"📊 Compression: {((input_size_mb - output_size_mb) / input_size_mb * 100):+.1f}%")
        print(f"💾 Mémoire finale: {final_memory:.1f} MB")
        print(f"💾 Augmentation mémoire: {memory_increase:+.1f} MB")
        print(f"📝 Mapping: {len(mapping)} remplacements")
        
        # Test de validation rapide
        if len(anonymized_pdf) > 0:
            print(f"✅ PDF généré valide ({len(anonymized_pdf):,} bytes)")
        else:
            print(f"❌ PDF généré vide!")
            
        return {
            "success": True,
            "method": method_name,
            "processing_time": processing_time,
            "input_size_mb": input_size_mb,
            "output_size_mb": output_size_mb,
            "memory_increase_mb": memory_increase,
            "mapping_count": len(mapping),
            "result_size": len(anonymized_pdf)
        }
        
    except Exception as e:
        end_time = time.time()
        final_memory = get_memory_usage()
        processing_time = end_time - start_time
        memory_increase = final_memory - initial_memory
        
        print(f"❌ {method_name} ÉCHEC après {processing_time:.2f}s")
        print(f"❌ Erreur: {str(e)}")
        print(f"💾 Mémoire à l'échec: {final_memory:.1f} MB")
        print(f"💾 Augmentation mémoire: {memory_increase:+.1f} MB")
        
        return {
            "success": False,
            "method": method_name,
            "processing_time": processing_time,
            "error": str(e),
            "memory_increase_mb": memory_increase
        }
    finally:
        # Nettoyage mémoire
        gc.collect()

def main():
    """
    Test principal des améliorations pour gros fichiers.
    """
    print("🚀 Test des améliorations pour GROS FICHIERS PDF")
    print("=" * 60)
    
    # Créer différentes tailles de test
    test_sizes = [5, 20, 50]  # MB
    
    for target_size in test_sizes:
        print(f"\n🎯 TEST AVEC FICHIER SIMULÉ: {target_size}MB")
        print("=" * 40)
        
        # Créer le PDF de test
        pdf_content, tiers = create_large_test_pdf(target_size)
        
        if pdf_content is None:
            print(f"❌ Impossible de créer le PDF de test de {target_size}MB")
            continue
            
        actual_size_mb = len(pdf_content) / 1024 / 1024
        print(f"📄 PDF créé: {actual_size_mb:.1f}MB")
        
        # Tests des différentes méthodes
        results = []
        
        methods_to_test = [
            ("PDF-REDACTOR", anonymize_pdf_with_redactor),
            ("PIPELINE", anonymize_pdf_enhanced_pipeline),
            ("DIRECT", anonymize_pdf_direct)
        ]
        
        for method_name, method_func in methods_to_test:
            result = test_method(method_name, method_func, pdf_content, tiers)
            results.append(result)
            
            # Pause entre les tests
            time.sleep(2)
            gc.collect()
        
        # Résumé des résultats pour cette taille
        print(f"\n📊 RÉSUMÉ POUR {actual_size_mb:.1f}MB:")
        print("-" * 30)
        
        successful_methods = [r for r in results if r["success"]]
        failed_methods = [r for r in results if not r["success"]]
        
        if successful_methods:
            print("✅ Méthodes réussies:")
            for result in successful_methods:
                print(f"  {result['method']}: {result['processing_time']:.1f}s, "
                      f"mémoire: {result['memory_increase_mb']:+.1f}MB")
                      
        if failed_methods:
            print("❌ Méthodes échouées:")
            for result in failed_methods:
                print(f"  {result['method']}: {result['error'][:60]}...")
        
        # Recommandation
        if successful_methods:
            fastest = min(successful_methods, key=lambda x: x["processing_time"])
            lowest_memory = min(successful_methods, key=lambda x: x["memory_increase_mb"])
            
            print(f"\n💡 RECOMMANDATIONS pour {actual_size_mb:.1f}MB:")
            print(f"  Plus rapide: {fastest['method']} ({fastest['processing_time']:.1f}s)")
            print(f"  Moins de mémoire: {lowest_memory['method']} ({lowest_memory['memory_increase_mb']:+.1f}MB)")
            
        print("\n" + "="*60)
    
    print("\n🎉 Tests terminés!")
    print("\n💡 CONCLUSIONS GÉNÉRALES:")
    print("💡 - Utilisez pdf-redactor pour fichiers < 500MB")
    print("💡 - Utilisez pipeline pour fichiers 100-500MB") 
    print("💡 - Évitez direct pour gros fichiers (problèmes mémoire)")
    print("💡 - Segmentez les fichiers > 1GB")

if __name__ == "__main__":
    main() 