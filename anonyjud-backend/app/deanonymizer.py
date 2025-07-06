from typing import Dict
import re

def deanonymize_text(anonymized_text: str, mapping: Dict[str, str]) -> str:
    """
    Dé-anonymise le texte en remplaçant les balises par les valeurs originales.
    
    Args:
        anonymized_text: Le texte anonymisé contenant des balises
        mapping: Dictionnaire de correspondance entre balises et valeurs originales
        
    Returns:
        Le texte dé-anonymisé
    """
    deanonymized = anonymized_text
    
    # Trier les balises par longueur décroissante pour éviter les remplacements partiels
    sorted_tags = sorted(mapping.keys(), key=len, reverse=True)
    
    # Remplacer chaque balise par sa valeur originale
    for tag in sorted_tags:
        original = mapping[tag]
        # Utiliser une expression régulière pour remplacer la balise exacte (pas de remplacement partiel)
        pattern = re.compile(r'\b' + re.escape(tag) + r'\b')
        deanonymized = pattern.sub(original, deanonymized)
    
    return deanonymized 