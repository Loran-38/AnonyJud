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
    print(f"🔍 DEANONYMIZE_TEXT - Début du processus")
    print(f"📝 Texte d'entrée (premiers 300 chars): {anonymized_text[:300]}...")
    print(f"🗂️ Mapping reçu: {mapping}")
    print(f"📊 Nombre de balises dans le mapping: {len(mapping)}")
    
    deanonymized = anonymized_text
    
    # Trier les balises par longueur décroissante pour éviter les remplacements partiels
    sorted_tags = sorted(mapping.keys(), key=len, reverse=True)
    print(f"🔢 Balises triées par longueur: {sorted_tags}")
    
    # Analyser quelles balises sont présentes dans le texte
    found_tags = []
    for tag in sorted_tags:
        if tag in anonymized_text:
            found_tags.append(tag)
            print(f"✅ Balise '{tag}' trouvée dans le texte")
        else:
            print(f"❌ Balise '{tag}' NON trouvée dans le texte")
    
    print(f"📋 Résumé: {len(found_tags)}/{len(sorted_tags)} balises trouvées: {found_tags}")
    
    # Remplacer chaque balise par sa valeur originale
    replacements_made = 0
    for tag in sorted_tags:
        if tag in deanonymized:
        original = mapping[tag]
            print(f"🔄 Tentative de remplacement: '{tag}' -> '{original}'")
            
            # Compter les occurrences avant remplacement
            count_before = deanonymized.count(tag)
            
        # Utiliser une expression régulière pour remplacer la balise exacte (pas de remplacement partiel)
        pattern = re.compile(r'\b' + re.escape(tag) + r'\b')
            deanonymized_new = pattern.sub(original, deanonymized)
            
            # Compter les occurrences après remplacement
            count_after = deanonymized_new.count(tag)
            actual_replacements = count_before - count_after
            
            if actual_replacements > 0:
                print(f"✅ Remplacement réussi: {actual_replacements} occurrence(s) de '{tag}' remplacée(s) par '{original}'")
                replacements_made += actual_replacements
                deanonymized = deanonymized_new
            else:
                print(f"⚠️ Aucun remplacement effectué pour '{tag}' (peut-être pas de correspondance de mots entiers)")
                # Essayer un remplacement simple comme fallback
                if tag in deanonymized:
                    deanonymized = deanonymized.replace(tag, original)
                    print(f"🔄 Remplacement simple effectué pour '{tag}'")
                    replacements_made += 1
    
    print(f"📈 Total des remplacements effectués: {replacements_made}")
    print(f"📝 Texte de sortie (premiers 300 chars): {deanonymized[:300]}...")
    print(f"🏁 DEANONYMIZE_TEXT - Fin du processus")
    
    return deanonymized 