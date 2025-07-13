#!/usr/bin/env python3
"""
Test pour vérifier que le problème du champ PRENOM est résolu.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.anonymizer import anonymize_text
from app.deanonymizer import deanonymize_text

def test_prenom_problem():
    """
    Test spécifique pour le problème rapporté :
    - Nom : Huissoud
    - Prénom : Louis
    - Le résultat ne doit pas être "PREHUISSOUD" mais "Louis"
    """
    print("=" * 60)
    print("🧪 TEST DU PROBLÈME PRENOM")
    print("=" * 60)
    
    # Données de test
    texte_original = "Monsieur Louis Huissoud habite à Paris."
    
    tiers = [{
        "numero": 1,
        "nom": "Huissoud",
        "prenom": "Louis"
    }]
    
    print(f"📝 Texte original: {texte_original}")
    print(f"👤 Tiers: {tiers}")
    
    # Étape 1: Anonymisation
    print("\n🔒 ÉTAPE 1: ANONYMISATION")
    print("-" * 40)
    
    texte_anonymise, mapping = anonymize_text(texte_original, tiers)
    
    print(f"📝 Texte anonymisé: {texte_anonymise}")
    print(f"🗂️ Mapping généré: {mapping}")
    
    # Vérifications de l'anonymisation
    assert "Louis" not in texte_anonymise, "❌ Le prénom 'Louis' n'a pas été anonymisé"
    assert "Huissoud" not in texte_anonymise, "❌ Le nom 'Huissoud' n'a pas été anonymisé"
    assert "PRENOM1" in texte_anonymise, "❌ La balise 'PRENOM1' n'est pas présente"
    assert "NOM1" in texte_anonymise, "❌ La balise 'NOM1' n'est pas présente"
    
    print("✅ Anonymisation réussie")
    
    # Étape 2: Dé-anonymisation
    print("\n🔓 ÉTAPE 2: DÉ-ANONYMISATION")
    print("-" * 40)
    
    texte_deanonymise = deanonymize_text(texte_anonymise, mapping)
    
    print(f"📝 Texte dé-anonymisé: {texte_deanonymise}")
    
    # Vérifications de la dé-anonymisation
    assert "Louis" in texte_deanonymise, "❌ Le prénom 'Louis' n'a pas été restauré"
    assert "Huissoud" in texte_deanonymise, "❌ Le nom 'Huissoud' n'a pas été restauré"
    assert "PRENOM1" not in texte_deanonymise, "❌ La balise 'PRENOM1' n'a pas été remplacée"
    assert "NOM1" not in texte_deanonymise, "❌ La balise 'NOM1' n'a pas été remplacée"
    
    # Vérification spécifique du problème rapporté
    assert "PREHUISSOUD" not in texte_deanonymise, "❌ PROBLÈME: 'PREHUISSOUD' détecté (concaténation incorrecte)"
    assert texte_deanonymise == texte_original, f"❌ Le texte dé-anonymisé ne correspond pas à l'original\nAttendu: {texte_original}\nObtenu: {texte_deanonymise}"
    
    print("✅ Dé-anonymisation réussie")
    print("✅ Problème PRENOM résolu !")
    
    return True

def test_multiple_tiers():
    """
    Test avec plusieurs tiers pour vérifier que la numérotation fonctionne correctement
    """
    print("\n" + "=" * 60)
    print("🧪 TEST AVEC PLUSIEURS TIERS")
    print("=" * 60)
    
    texte_original = "Jean Dupont et Marie Martin sont présents."
    
    tiers = [
        {
            "numero": 1,
            "nom": "Dupont",
            "prenom": "Jean"
        },
        {
            "numero": 2,
            "nom": "Martin",
            "prenom": "Marie"
        }
    ]
    
    print(f"📝 Texte original: {texte_original}")
    print(f"👥 Tiers: {tiers}")
    
    # Anonymisation
    texte_anonymise, mapping = anonymize_text(texte_original, tiers)
    print(f"📝 Texte anonymisé: {texte_anonymise}")
    print(f"🗂️ Mapping: {mapping}")
    
    # Dé-anonymisation
    texte_deanonymise = deanonymize_text(texte_anonymise, mapping)
    print(f"📝 Texte dé-anonymisé: {texte_deanonymise}")
    
    # Vérifications
    assert texte_deanonymise == texte_original, f"❌ Échec du test multi-tiers\nAttendu: {texte_original}\nObtenu: {texte_deanonymise}"
    
    print("✅ Test multi-tiers réussi")
    
    return True

if __name__ == "__main__":
    try:
        test_prenom_problem()
        test_multiple_tiers()
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS !")
        print("✅ Le problème du champ PRENOM est résolu")
    except Exception as e:
        print(f"\n❌ ÉCHEC DU TEST: {str(e)}")
        sys.exit(1) 