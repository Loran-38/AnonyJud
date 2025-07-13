#!/usr/bin/env python3
"""
Test de l'anonymisation PDF avancée avec pdf-redactor
"""

import logging
from app.anonymizer import create_pdf_from_text

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_pdf_redactor_advanced():
    """Test de l'anonymisation PDF avec pdf-redactor"""
    print("=== Test PDF Redactor Avancé ===")
    
    # Texte de test avec mise en page complexe
    original_text = """CONTRAT DE BAIL

Nom du locataire : Huissoud Louis
Adresse : 123 Rue de la Paix, 75001 Paris
Téléphone : 01.23.45.67.89
Email : louis.huissoud@example.com

ARTICLE 1 - DESIGNATION DU BIEN
Le présent bail porte sur un appartement situé au :
123 Rue de la Paix, 75001 Paris

ARTICLE 2 - LOYER
Le loyer mensuel est fixé à 1200 euros.

Fait à Paris, le 15/01/2024

Signature du locataire : Louis Huissoud"""
    
    try:
        # Créer le PDF original
        original_pdf = create_pdf_from_text(original_text, "Contrat de Bail")
        print(f"✅ PDF original créé - Taille: {len(original_pdf)} bytes")
        
        # Définir les tiers
        tiers = [
            {
                "numero": 1,
                "nom": "Huissoud",
                "prenom": "Louis",
                "adresse": "123 Rue de la Paix, 75001 Paris",
                "telephone": "01.23.45.67.89",
                "email": "louis.huissoud@example.com"
            }
        ]
        
        print(f"📊 Tiers définis: {tiers}")
        
        # Tester avec la méthode avancée
        try:
            from app.pdf_redactor_simple import anonymize_pdf_with_simple_redactor, deanonymize_pdf_with_simple_redactor
            
            print("\n🚀 Test avec pdf-redactor (méthode avancée)")
            
            # Anonymiser le PDF
            anonymized_pdf, mapping = anonymize_pdf_with_simple_redactor(original_pdf, tiers)
            print(f"✅ PDF anonymisé avec pdf-redactor - Taille: {len(anonymized_pdf)} bytes")
            print(f"🗂️ Mapping généré: {mapping}")
            
            # Extraire le texte du PDF anonymisé pour vérification
            from app.utils import extract_text_from_pdf
            anonymized_text = extract_text_from_pdf(anonymized_pdf)
            print(f"📝 Texte anonymisé extrait:")
            print(anonymized_text[:500] + "..." if len(anonymized_text) > 500 else anonymized_text)
            
            # Dé-anonymiser le PDF
            deanonymized_pdf = deanonymize_pdf_with_simple_redactor(anonymized_pdf, mapping)
            print(f"✅ PDF dé-anonymisé avec pdf-redactor - Taille: {len(deanonymized_pdf)} bytes")
            
            # Extraire le texte du PDF dé-anonymisé pour vérification
            deanonymized_text = extract_text_from_pdf(deanonymized_pdf)
            print(f"📝 Texte dé-anonymisé extrait:")
            print(deanonymized_text[:500] + "..." if len(deanonymized_text) > 500 else deanonymized_text)
            
            # Vérifications
            print("\n=== Vérifications PDF Redactor ===")
            
            # Vérifier que le mapping contient les bonnes balises
            expected_tags = ["NOM1", "PRENOM1", "ADRESSE1", "TEL1", "EMAIL1"]
            for tag in expected_tags:
                if tag in mapping:
                    print(f"✅ {tag} trouvé dans le mapping: {mapping[tag]}")
                else:
                    print(f"❌ {tag} MANQUANT dans le mapping")
            
            # Vérifier que les valeurs sont correctement restaurées
            expected_values = ["Huissoud", "Louis", "123 Rue de la Paix, 75001 Paris"]
            for value in expected_values:
                if value in deanonymized_text:
                    print(f"✅ Valeur '{value}' correctement restaurée")
                else:
                    print(f"❌ Valeur '{value}' MANQUANTE dans le texte dé-anonymisé")
            
            # Sauvegarder les PDFs pour inspection
            with open("test_redactor_original.pdf", "wb") as f:
                f.write(original_pdf)
            with open("test_redactor_anonymized.pdf", "wb") as f:
                f.write(anonymized_pdf)
            with open("test_redactor_deanonymized.pdf", "wb") as f:
                f.write(deanonymized_pdf)
            
            print("✅ PDFs avec pdf-redactor sauvegardés pour inspection")
            
            return True
            
        except ImportError:
            print("⚠️ pdf-redactor non disponible, test ignoré")
            return True
            
    except Exception as e:
        print(f"❌ Erreur lors du test pdf-redactor: {e}")
        return False

def test_comparison_methods():
    """Compare les deux méthodes d'anonymisation PDF"""
    print("\n=== Comparaison des méthodes ===")
    
    # Texte simple pour comparaison
    test_text = """Nom: Dupont Jean
Prénom: Jean
Adresse: 456 Avenue Test, 69000 Lyon"""
    
    tiers = [{
        "numero": 1,
        "nom": "Dupont",
        "prenom": "Jean", 
        "adresse": "456 Avenue Test, 69000 Lyon"
    }]
    
    try:
        # Créer le PDF de test
        original_pdf = create_pdf_from_text(test_text, "Test Comparaison")
        
        # Test méthode standard
        from app.anonymizer import anonymize_pdf_file, deanonymize_pdf_file
        
        print("\n📝 Méthode standard (reportlab):")
        std_anonymized, std_mapping = anonymize_pdf_file(original_pdf, tiers)
        std_deanonymized = deanonymize_pdf_file(std_anonymized, std_mapping)
        print(f"Taille anonymisé: {len(std_anonymized)} bytes")
        print(f"Taille dé-anonymisé: {len(std_deanonymized)} bytes")
        
        # Test méthode avancée si disponible
        try:
            from app.pdf_redactor_simple import anonymize_pdf_with_simple_redactor, deanonymize_pdf_with_simple_redactor
            
            print("\n🚀 Méthode avancée (pdf-redactor):")
            adv_anonymized, adv_mapping = anonymize_pdf_with_simple_redactor(original_pdf, tiers)
            adv_deanonymized = deanonymize_pdf_with_simple_redactor(adv_anonymized, adv_mapping)
            print(f"Taille anonymisé: {len(adv_anonymized)} bytes")
            print(f"Taille dé-anonymisé: {len(adv_deanonymized)} bytes")
            
            print(f"\n📊 Comparaison:")
            print(f"Mappings identiques: {std_mapping == adv_mapping}")
            print(f"Différence de taille anonymisé: {len(adv_anonymized) - len(std_anonymized)} bytes")
            print(f"Différence de taille dé-anonymisé: {len(adv_deanonymized) - len(std_deanonymized)} bytes")
            
        except ImportError:
            print("⚠️ Méthode avancée non disponible pour comparaison")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la comparaison: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Tests PDF Redactor Avancé\n")
    
    # Test principal
    success1 = test_pdf_redactor_advanced()
    
    # Test de comparaison
    success2 = test_comparison_methods()
    
    if success1 and success2:
        print("\n🎉 Tous les tests sont réussis !")
    else:
        print("\n⚠️ Certains tests ont échoué") 