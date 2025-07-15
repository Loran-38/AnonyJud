#!/usr/bin/env python3
"""
Test pour vérifier si l'anonymisation PDF fonctionne réellement.
Ce test va créer un PDF avec le nom "HUISSOUD" et vérifier s'il est bien remplacé par "NOM1".
"""

import fitz  # PyMuPDF
import io
from app.anonymizer import anonymize_pdf_direct, deanonymize_pdf_direct
from app.anonymizer import anonymize_text
import logging

# Configurer les logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_test_pdf_with_huissoud():
    """Crée un PDF de test avec le nom HUISSOUD"""
    print("📄 Création d'un PDF de test avec 'HUISSOUD'...")
    
    # Créer un document PDF
    doc = fitz.open()
    page = doc.new_page()
    
    # Ajouter du texte avec "HUISSOUD"
    text_content = """
    CONTRAT DE TRAVAIL
    
    Entre les soussignés :
    
    La société ABC, représentée par Monsieur HUISSOUD
    Adresse : 123 rue de la Paix, 75001 Paris
    Téléphone : 01 23 45 67 89
    Email : contact@abc.com
    
    Et Monsieur HUISSOUD Jean
    Né le 15 mars 1980
    Adresse : 456 avenue des Champs, 75008 Paris
    Téléphone : 06 12 34 56 78
    Email : jean.huissoud@email.com
    
    Il est convenu ce qui suit :
    
    Monsieur HUISSOUD sera employé en qualité de développeur
    à compter du 1er janvier 2024.
    
    Fait à Paris, le 15 décembre 2023
    
    Signatures :
    _________________                    _________________
    La société ABC                      Monsieur HUISSOUD
    """
    
    # Insérer le texte dans le PDF
    page.insert_text((50, 50), text_content, fontsize=12)
    
    # Sauvegarder le PDF
    pdf_bytes = doc.tobytes()
    doc.close()
    
    print(f"✅ PDF de test créé avec succès - Taille: {len(pdf_bytes)} bytes")
    return pdf_bytes

def test_anonymisation_reelle():
    """Test l'anonymisation réelle du PDF"""
    print("\n🔍 TEST D'ANONYMIZATION RÉELLE")
    print("=" * 50)
    
    # 1. Créer le PDF de test
    pdf_content = create_test_pdf_with_huissoud()
    
    # 2. Définir les tiers pour l'anonymisation
    tiers = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Jean",
            "adresse_numero": "456",
            "adresse_voie": "avenue des Champs",
            "adresse_code_postal": "75008",
            "adresse_ville": "Paris",
            "telephone": "06 12 34 56 78",
            "email": "jean.huissoud@email.com"
        }
    ]
    
    print(f"\n👥 Tiers défini: {tiers}")
    
    # 3. Anonymiser le PDF
    print("\n🔒 ANONYMIZATION DU PDF...")
    try:
        anonymized_pdf, mapping = anonymize_pdf_direct(pdf_content, tiers)
        print(f"✅ Anonymisation réussie!")
        print(f"📊 Mapping généré: {mapping}")
        print(f"📁 Taille PDF anonymisé: {len(anonymized_pdf)} bytes")
        
        # 4. Vérifier le contenu du PDF anonymisé
        print("\n🔍 VÉRIFICATION DU CONTENU ANONYMIZÉ...")
        doc = fitz.open(stream=anonymized_pdf, filetype="pdf")
        anonymized_text = ""
        for page in doc:
            anonymized_text += page.get_text()
        doc.close()
        
        print(f"📝 Texte extrait du PDF anonymisé:")
        print("-" * 40)
        print(anonymized_text[:500] + "..." if len(anonymized_text) > 500 else anonymized_text)
        print("-" * 40)
        
        # 5. Vérifier si "HUISSOUD" a été remplacé par "NOM1"
        if "HUISSOUD" in anonymized_text:
            print("❌ PROBLÈME: 'HUISSOUD' est encore présent dans le PDF anonymisé!")
            print("🔍 Recherche des occurrences...")
            count = anonymized_text.count("HUISSOUD")
            print(f"📊 Nombre d'occurrences de 'HUISSOUD': {count}")
        else:
            print("✅ SUCCÈS: 'HUISSOUD' a été correctement remplacé!")
        
        # 6. Vérifier si "NOM1" est présent
        if "NOM1" in anonymized_text:
            print("✅ SUCCÈS: 'NOM1' est présent dans le PDF anonymisé!")
            count = anonymized_text.count("NOM1")
            print(f"📊 Nombre d'occurrences de 'NOM1': {count}")
        else:
            print("❌ PROBLÈME: 'NOM1' n'est pas présent dans le PDF anonymisé!")
        
        # 7. Test de dé-anonymisation
        print("\n🔓 TEST DE DÉ-ANONYMIZATION...")
        try:
            deanonymized_pdf = deanonymize_pdf_direct(anonymized_pdf, mapping)
            print("✅ Dé-anonymisation réussie!")
            
            # Vérifier le contenu dé-anonymisé
            doc = fitz.open(stream=deanonymized_pdf, filetype="pdf")
            deanonymized_text = ""
            for page in doc:
                deanonymized_text += page.get_text()
            doc.close()
            
            if "HUISSOUD" in deanonymized_text:
                print("✅ SUCCÈS: 'HUISSOUD' restauré dans le PDF dé-anonymisé!")
            else:
                print("❌ PROBLÈME: 'HUISSOUD' n'a pas été restauré!")
                
        except Exception as e:
            print(f"❌ Erreur lors de la dé-anonymisation: {str(e)}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'anonymisation: {str(e)}")
        import traceback
        traceback.print_exc()

def test_anonymisation_text_only():
    """Test l'anonymisation du texte seulement"""
    print("\n🔍 TEST D'ANONYMIZATION TEXTE SEULEMENT")
    print("=" * 50)
    
    # Texte de test
    test_text = """
    CONTRAT DE TRAVAIL
    
    Entre les soussignés :
    
    La société ABC, représentée par Monsieur HUISSOUD
    Adresse : 123 rue de la Paix, 75001 Paris
    Téléphone : 01 23 45 67 89
    Email : contact@abc.com
    
    Et Monsieur HUISSOUD Jean
    Né le 15 mars 1980
    Adresse : 456 avenue des Champs, 75008 Paris
    Téléphone : 06 12 34 56 78
    Email : jean.huissoud@email.com
    """
    
    tiers = [
        {
            "numero": 1,
            "nom": "HUISSOUD",
            "prenom": "Jean",
            "adresse_numero": "456",
            "adresse_voie": "avenue des Champs",
            "adresse_code_postal": "75008",
            "adresse_ville": "Paris",
            "telephone": "06 12 34 56 78",
            "email": "jean.huissoud@email.com"
        }
    ]
    
    print("🔒 Anonymisation du texte...")
    anonymized_text, mapping = anonymize_text(test_text, tiers)
    
    print(f"📊 Mapping: {mapping}")
    print(f"📝 Texte anonymisé:")
    print("-" * 40)
    print(anonymized_text)
    print("-" * 40)
    
    if "HUISSOUD" in anonymized_text:
        print("❌ PROBLÈME: 'HUISSOUD' est encore présent dans le texte anonymisé!")
    else:
        print("✅ SUCCÈS: 'HUISSOUD' a été correctement remplacé dans le texte!")
    
    if "NOM1" in anonymized_text:
        print("✅ SUCCÈS: 'NOM1' est présent dans le texte anonymisé!")
    else:
        print("❌ PROBLÈME: 'NOM1' n'est pas présent dans le texte anonymisé!")

if __name__ == "__main__":
    print("🚀 DÉBUT DES TESTS D'ANONYMIZATION")
    print("=" * 60)
    
    # Test 1: Anonymisation du texte seulement
    test_anonymisation_text_only()
    
    # Test 2: Anonymisation réelle du PDF
    test_anonymisation_reelle()
    
    print("\n🏁 FIN DES TESTS") 