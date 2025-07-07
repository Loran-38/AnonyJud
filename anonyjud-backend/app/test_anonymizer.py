import sys
import os

# Ajouter le répertoire parent au chemin pour pouvoir importer les modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.anonymizer import anonymize_text
from app.deanonymizer import deanonymize_text

def test_champ_personnalise():
    """
    Test pour vérifier si l'anonymiseur traite correctement les champs personnalisés.
    """
    # Cas de test avec un champ personnalisé (SIRET)
    texte = "Test avec un numéro SIRET 12345678901234 qui doit être anonymisé."
    tiers = [{
        "champPerso": "12345678901234",
        "labelChampPerso": "SIRET"
    }]
    
    # Anonymiser le texte
    texte_anonymise, mapping = anonymize_text(texte, tiers)
    
    print("Texte original:", texte)
    print("Texte anonymisé:", texte_anonymise)
    print("Mapping:", mapping)
    
    # Vérifier si le numéro SIRET a été remplacé
    assert "12345678901234" not in texte_anonymise, "Le numéro SIRET n'a pas été anonymisé"
    
    # Vérifier si une balise SIRET est présente dans le texte anonymisé
    siret_tag_present = any("SIRET" in tag for tag in mapping.keys())
    assert siret_tag_present, "Aucune balise SIRET n'a été créée"
    
    # Test de dé-anonymisation
    texte_deanonymise = deanonymize_text(texte_anonymise, mapping)
    print("Texte dé-anonymisé:", texte_deanonymise)
    
    # Vérifier si le texte dé-anonymisé correspond au texte original
    assert texte_deanonymise == texte, "La dé-anonymisation n'a pas restauré le texte original"
    
    print("Test réussi!")

def test_multiple_champs_personnalises():
    """
    Test pour vérifier si l'anonymiseur traite correctement plusieurs champs personnalisés.
    """
    # Cas de test avec plusieurs champs personnalisés
    texte = "Patient: Jean Dupont, Numéro SS: 1234567890123, Dossier médical: MED-2023-456"
    tiers = [
        {
            "nom": "Dupont",
            "prenom": "Jean",
            "champPerso": "1234567890123",
            "labelChampPerso": "NumSS"
        },
        {
            "champPerso": "MED-2023-456",
            "labelChampPerso": "Dossier"
        }
    ]
    
    # Anonymiser le texte
    texte_anonymise, mapping = anonymize_text(texte, tiers)
    
    print("\nTest multiple:")
    print("Texte original:", texte)
    print("Texte anonymisé:", texte_anonymise)
    print("Mapping:", mapping)
    
    # Vérifier si les informations ont été remplacées
    assert "1234567890123" not in texte_anonymise, "Le numéro SS n'a pas été anonymisé"
    assert "MED-2023-456" not in texte_anonymise, "Le numéro de dossier n'a pas été anonymisé"
    
    # Vérifier si les balises personnalisées sont présentes
    numss_tag_present = any("NUMSS" in tag for tag in mapping.keys())
    dossier_tag_present = any("DOSSIER" in tag for tag in mapping.keys())
    
    assert numss_tag_present, "Aucune balise NumSS n'a été créée"
    assert dossier_tag_present, "Aucune balise Dossier n'a été créée"
    
    # Test de dé-anonymisation
    texte_deanonymise = deanonymize_text(texte_anonymise, mapping)
    print("Texte dé-anonymisé:", texte_deanonymise)
    
    # Vérifier si le texte dé-anonymisé correspond au texte original
    assert texte_deanonymise == texte, "La dé-anonymisation n'a pas restauré le texte original"
    
    print("Test multiple réussi!")

def test_nouveau_format_custom_fields():
    """
    Test pour vérifier si l'anonymiseur traite correctement le nouveau format customFields.
    """
    # Cas de test avec le nouveau format customFields
    texte = "Entreprise ACME SARL (SIRET: 12345678901234) gérée par Jean Dupont (Réf: REF-2023-789)"
    tiers = [
        {
            "nom": "Dupont",
            "prenom": "Jean",
            "societe": "ACME SARL",
            "customFields": [
                {
                    "id": 1,
                    "label": "SIRET",
                    "value": "12345678901234"
                },
                {
                    "id": 2,
                    "label": "Reference",
                    "value": "REF-2023-789"
                }
            ]
        }
    ]
    
    # Anonymiser le texte
    texte_anonymise, mapping = anonymize_text(texte, tiers)
    
    print("\nTest nouveau format customFields:")
    print("Texte original:", texte)
    print("Texte anonymisé:", texte_anonymise)
    print("Mapping:", mapping)
    
    # Vérifier si les informations ont été remplacées
    assert "12345678901234" not in texte_anonymise, "Le numéro SIRET n'a pas été anonymisé"
    assert "REF-2023-789" not in texte_anonymise, "La référence n'a pas été anonymisée"
    assert "ACME SARL" not in texte_anonymise, "La société n'a pas été anonymisée"
    assert "Jean" not in texte_anonymise, "Le prénom n'a pas été anonymisé"
    assert "Dupont" not in texte_anonymise, "Le nom n'a pas été anonymisé"
    
    # Vérifier si les balises personnalisées sont présentes
    siret_tag_present = any("SIRET" in tag for tag in mapping.keys())
    reference_tag_present = any("REFERENCE" in tag for tag in mapping.keys())
    societe_tag_present = any("SOCIETE" in tag for tag in mapping.keys())
    nom_tag_present = any("NOM" in tag for tag in mapping.keys())
    prenom_tag_present = any("PRENOM" in tag for tag in mapping.keys())
    
    assert siret_tag_present, "Aucune balise SIRET n'a été créée"
    assert reference_tag_present, "Aucune balise REFERENCE n'a été créée"
    assert societe_tag_present, "Aucune balise SOCIETE n'a été créée"
    assert nom_tag_present, "Aucune balise NOM n'a été créée"
    assert prenom_tag_present, "Aucune balise PRENOM n'a été créée"
    
    # Test de dé-anonymisation
    texte_deanonymise = deanonymize_text(texte_anonymise, mapping)
    print("Texte dé-anonymisé:", texte_deanonymise)
    
    # Vérifier si le texte dé-anonymisé correspond au texte original
    assert texte_deanonymise == texte, "La dé-anonymisation n'a pas restauré le texte original"
    
    print("Test nouveau format customFields réussi!")

if __name__ == "__main__":
    test_champ_personnalise()
    test_multiple_champs_personnalises()
    test_nouveau_format_custom_fields()
    print("\nTous les tests sont réussis! ✅") 