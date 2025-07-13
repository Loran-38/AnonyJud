#!/usr/bin/env python3
"""
Test des fonctions PDF d'anonymisation et de dé-anonymisation
"""

import logging
from app.anonymizer import create_pdf_from_text, anonymize_pdf_file, deanonymize_pdf_file

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_create_pdf():
    """Test de création d'un PDF simple"""
    print("=== Test création PDF ===")
    
    text = """Ceci est un test de création de PDF.

    Ce document contient plusieurs paragraphes pour tester la fonctionnalité de création de PDF avec reportlab.
    
    Nous testons les caractères spéciaux : & < > et les accents : éàèùç"""
    
    try:
        pdf_content = create_pdf_from_text(text, "Test PDF")
        print(f"✅ PDF créé avec succès - Taille: {len(pdf_content)} bytes")
        
        # Sauvegarder le PDF pour vérification
        with open("test_created.pdf", "wb") as f:
            f.write(pdf_content)
        print("✅ PDF sauvegardé dans test_created.pdf")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création PDF: {e}")
        return False

def test_anonymize_pdf():
    """Test d'anonymisation d'un PDF"""
    print("\n=== Test anonymisation PDF ===")
    
    # Créer un PDF de test avec des données personnelles
    original_text = """Document de test

    Nom: Dupont Jean
    Prénom: Jean
    Adresse: 123 Rue de la Paix, 75001 Paris
    Téléphone: 01.23.45.67.89
    Email: jean.dupont@example.com
    
    Ce document contient des informations personnelles qui doivent être anonymisées."""
    
    try:
        # Créer le PDF original
        original_pdf = create_pdf_from_text(original_text, "Document Original")
        print(f"✅ PDF original créé - Taille: {len(original_pdf)} bytes")
        
        # Définir les tiers
        tiers = [
            {
                "numero": 1,
                "nom": "Dupont",
                "prenom": "Jean",
                "adresse": "123 Rue de la Paix, 75001 Paris",
                "telephone": "01.23.45.67.89",
                "email": "jean.dupont@example.com"
            }
        ]
        
        # Anonymiser le PDF
        anonymized_pdf, mapping = anonymize_pdf_file(original_pdf, tiers)
        print(f"✅ PDF anonymisé - Taille: {len(anonymized_pdf)} bytes")
        print(f"✅ Mapping généré: {mapping}")
        
        # Sauvegarder le PDF anonymisé
        with open("test_anonymized.pdf", "wb") as f:
            f.write(anonymized_pdf)
        print("✅ PDF anonymisé sauvegardé dans test_anonymized.pdf")
        
        return anonymized_pdf, mapping
        
    except Exception as e:
        print(f"❌ Erreur lors de l'anonymisation PDF: {e}")
        return None, None

def test_deanonymize_pdf():
    """Test de dé-anonymisation d'un PDF"""
    print("\n=== Test dé-anonymisation PDF ===")
    
    # D'abord anonymiser un PDF
    anonymized_pdf, mapping = test_anonymize_pdf()
    
    if anonymized_pdf is None:
        print("❌ Impossible de tester la dé-anonymisation sans PDF anonymisé")
        return False
    
    try:
        # Dé-anonymiser le PDF
        deanonymized_pdf = deanonymize_pdf_file(anonymized_pdf, mapping)
        print(f"✅ PDF dé-anonymisé - Taille: {len(deanonymized_pdf)} bytes")
        
        # Sauvegarder le PDF dé-anonymisé
        with open("test_deanonymized.pdf", "wb") as f:
            f.write(deanonymized_pdf)
        print("✅ PDF dé-anonymisé sauvegardé dans test_deanonymized.pdf")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la dé-anonymisation PDF: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Tests des fonctions PDF\n")
    
    # Test 1: Création PDF
    success1 = test_create_pdf()
    
    # Test 2: Anonymisation PDF
    success2 = test_anonymize_pdf() != (None, None)
    
    # Test 3: Dé-anonymisation PDF
    success3 = test_deanonymize_pdf()
    
    print(f"\n=== Résultats des tests ===")
    print(f"Création PDF: {'✅' if success1 else '❌'}")
    print(f"Anonymisation PDF: {'✅' if success2 else '❌'}")
    print(f"Dé-anonymisation PDF: {'✅' if success3 else '❌'}")
    
    if success1 and success2 and success3:
        print("\n🎉 Tous les tests PDF sont réussis !")
    else:
        print("\n⚠️ Certains tests ont échoué") 