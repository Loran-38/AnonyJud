import re
import json
from typing import Dict, List, Tuple, Any

def anonymize_text(text: str, tiers: List[Dict[str, Any]] = []) -> Tuple[str, Dict[str, str]]:
    """
    Anonymise le texte en détectant les entités personnelles et en les remplaçant par des balises.
    
    Args:
        text: Le texte à anonymiser
        tiers: Liste des tiers avec leurs informations personnelles (optionnel)
        
    Returns:
        Tuple contenant (texte_anonymisé, mapping_des_remplacements)
    """
    # Initialiser le mapping des remplacements
    mapping = {}
    anonymized = text
    
    # Si aucun tiers n'est fourni, on utilise une détection basique
    if not tiers or len(tiers) == 0:
        # Anonymisation basique (sans tiers)
        # Recherche des patterns qui ressemblent à des noms, adresses, etc.
        
        # Exemple : numéros de téléphone français
        phone_pattern = r'(?<!\d)((0|\+33|0033)[1-9](?:[ .-]?[0-9]{2}){4})(?!\d)'
        phone_matches = re.finditer(phone_pattern, anonymized)
        phone_count = 1
        
        for match in phone_matches:
            phone = match.group(0)
            if phone not in mapping.values():
                tag = f"TEL{phone_count}"
                mapping[tag] = phone
                anonymized = anonymized.replace(phone, tag)
                phone_count += 1
        
        # Exemple : adresses email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_matches = re.finditer(email_pattern, anonymized)
        email_count = 1
        
        for match in email_matches:
            email = match.group(0)
            if email not in mapping.values():
                tag = f"EMAIL{email_count}"
                mapping[tag] = email
                anonymized = anonymized.replace(email, tag)
                email_count += 1
    
    else:
        # Anonymisation avancée avec les tiers fournis
        # Parcourir chaque tier et anonymiser ses informations
        for tier_index, tier in enumerate(tiers):
            # Déterminer le numéro du tiers (utiliser l'index + 1 si pas de numéro explicite)
            tier_number = tier.get("numero", tier_index + 1)
            # Compteur local pour les champs personnalisés de ce tiers
            perso_count = 1
            # Traiter le nom
            if tier.get("nom"):
                nom = tier["nom"].strip()
                if nom and len(nom) > 1:  # Éviter les noms trop courts
                    tag = f"NOM{tier_number}"
                    mapping[tag] = nom
                    
                    # Remplacer toutes les occurrences (insensible à la casse)
                    pattern = re.compile(re.escape(nom), re.IGNORECASE)
                    anonymized = pattern.sub(tag, anonymized)
                    
                    # Variantes: nom en majuscules, minuscules
                    if nom.upper() != nom:
                        anonymized = anonymized.replace(nom.upper(), tag)
                    if nom.lower() != nom:
                        anonymized = anonymized.replace(nom.lower(), tag)
            
            # Traiter le prénom
            if tier.get("prenom"):
                prenom = tier["prenom"].strip()
                if prenom and len(prenom) > 1:
                    tag = f"PRENOM{tier_number}"
                    mapping[tag] = prenom
                    
                    pattern = re.compile(re.escape(prenom), re.IGNORECASE)
                    anonymized = pattern.sub(tag, anonymized)
                    
                    if prenom.upper() != prenom:
                        anonymized = anonymized.replace(prenom.upper(), tag)
                    if prenom.lower() != prenom:
                        anonymized = anonymized.replace(prenom.lower(), tag)
                        
            # Traiter les composants de l'adresse
            # Numéro de voie
            if tier.get("adresse_numero"):
                numero = tier["adresse_numero"].strip()
                if numero and len(numero) > 0:
                    tag = f"NUMERO{tier_number}"
                    mapping[tag] = numero
                    
                    # Remplacer toutes les occurrences
                    pattern = re.compile(re.escape(numero), re.IGNORECASE)
                    anonymized = pattern.sub(tag, anonymized)
            
            # Voie (rue, avenue, etc.)
            if tier.get("adresse_voie"):
                voie = tier["adresse_voie"].strip()
                if voie and len(voie) > 2:
                    tag = f"VOIE{tier_number}"
                    mapping[tag] = voie
                    
                    # Remplacer toutes les occurrences (insensible à la casse)
                    pattern = re.compile(re.escape(voie), re.IGNORECASE)
                    anonymized = pattern.sub(tag, anonymized)
                    
                    # Variantes: en majuscules, minuscules
                    if voie.upper() != voie:
                        anonymized = anonymized.replace(voie.upper(), tag)
                    if voie.lower() != voie:
                        anonymized = anonymized.replace(voie.lower(), tag)
            
            # Code postal
            if tier.get("adresse_code_postal"):
                code_postal = tier["adresse_code_postal"].strip()
                if code_postal and len(code_postal) > 0:
                    tag = f"CODEPOSTAL{tier_number}"
                    mapping[tag] = code_postal
                    
                    # Remplacer toutes les occurrences
                    anonymized = anonymized.replace(code_postal, tag)
            
            # Ville
            if tier.get("adresse_ville"):
                ville = tier["adresse_ville"].strip()
                if ville and len(ville) > 1:
                    tag = f"VILLE{tier_number}"
                    mapping[tag] = ville
                    
                    # Remplacer toutes les occurrences (insensible à la casse)
                    pattern = re.compile(re.escape(ville), re.IGNORECASE)
                    anonymized = pattern.sub(tag, anonymized)
                    
                    # Variantes: en majuscules, minuscules
                    if ville.upper() != ville:
                        anonymized = anonymized.replace(ville.upper(), tag)
                    if ville.lower() != ville:
                        anonymized = anonymized.replace(ville.lower(), tag)
            
            # Traiter l'adresse complète (pour compatibilité avec l'ancien format)
            if tier.get("adresse"):
                adresse = tier["adresse"].strip()
                if adresse and len(adresse) > 5:  # Éviter les adresses trop courtes
                    tag = f"ADRESSE{tier_number}"
                    mapping[tag] = adresse
                    
                    # Pour l'adresse, on fait un remplacement exact car elle peut contenir des caractères spéciaux
                    anonymized = anonymized.replace(adresse, tag)
            
            # Traiter le téléphone fixe
            if tier.get("telephone"):
                tel = tier["telephone"].strip()
                if tel and len(tel) > 5:
                    tag = f"TEL{tier_number}"
                    mapping[tag] = tel
                    
                    # Normaliser le format du téléphone pour la recherche
                    tel_clean = re.sub(r'[. -]', '', tel)
                    pattern = re.compile(r'[. -]'.join(re.escape(c) for c in tel_clean))
                    anonymized = pattern.sub(tag, anonymized)
                    
                    # Remplacer aussi le format sans espaces/points
                    anonymized = anonymized.replace(tel_clean, tag)
            
            # Traiter le portable
            if tier.get("portable"):
                portable = tier["portable"].strip()
                if portable and len(portable) > 5:
                    tag = f"PORTABLE{tier_number}"
                    mapping[tag] = portable
                    
                    # Même approche que pour le téléphone
                    portable_clean = re.sub(r'[. -]', '', portable)
                    pattern = re.compile(r'[. -]'.join(re.escape(c) for c in portable_clean))
                    anonymized = pattern.sub(tag, anonymized)
                    
                    anonymized = anonymized.replace(portable_clean, tag)
            
            # Traiter l'email
            if tier.get("email"):
                email = tier["email"].strip()
                if email and '@' in email:
                    tag = f"EMAIL{tier_number}"
                    mapping[tag] = email
                    
                    anonymized = anonymized.replace(email, tag)
            
            # Traiter la société
            if tier.get("societe"):
                societe = tier["societe"].strip()
                if societe and len(societe) > 1:
                    tag = f"SOCIETE{tier_number}"
                    mapping[tag] = societe
                    
                    pattern = re.compile(re.escape(societe), re.IGNORECASE)
                    anonymized = pattern.sub(tag, anonymized)
                    
                    if societe.upper() != societe:
                        anonymized = anonymized.replace(societe.upper(), tag)
                    if societe.lower() != societe:
                        anonymized = anonymized.replace(societe.lower(), tag)
                        
            # Traiter les champs personnalisés (nouveau format)
            if tier.get("customFields") and isinstance(tier["customFields"], list):
                for custom_field in tier["customFields"]:
                    if isinstance(custom_field, dict):
                        champ_value = custom_field.get("value")
                        champ_label = custom_field.get("label")
                        
                        if champ_value and isinstance(champ_value, str):
                            champ_value = champ_value.strip()
                            if champ_value and len(champ_value) > 1:
                                # Utiliser le label personnalisé s'il existe, sinon "PERSO"
                                label_base = "PERSO"
                                if champ_label and isinstance(champ_label, str):
                                    label_perso = champ_label.strip()
                                    # Nettoyer le label pour qu'il soit utilisable comme balise
                                    if label_perso:
                                        label_base = re.sub(r'[^A-Za-z]', '', label_perso.upper())
                                        if not label_base:  # Si le label ne contient pas de lettres
                                            label_base = "PERSO"
                                
                                tag = f"{label_base}{tier_number}"
                                mapping[tag] = champ_value
                                
                                # Remplacer toutes les occurrences (insensible à la casse)
                                pattern = re.compile(re.escape(champ_value), re.IGNORECASE)
                                anonymized = pattern.sub(tag, anonymized)
                                
                                # Variantes: en majuscules, minuscules
                                if champ_value.upper() != champ_value:
                                    anonymized = anonymized.replace(champ_value.upper(), tag)
                                if champ_value.lower() != champ_value:
                                    anonymized = anonymized.replace(champ_value.lower(), tag)
            
            # Traiter le champ personnalisé (ancien format pour compatibilité)
            if tier.get("champPerso"):
                champ_perso = tier["champPerso"]
                if champ_perso and isinstance(champ_perso, str):
                    champ_perso = champ_perso.strip()
                    if champ_perso and len(champ_perso) > 1:
                        # Utiliser le label personnalisé s'il existe, sinon "PERSO"
                        label_base = "PERSO"
                        if tier.get("labelChampPerso") and isinstance(tier["labelChampPerso"], str):
                            label_perso = tier["labelChampPerso"].strip()
                            # Nettoyer le label pour qu'il soit utilisable comme balise
                            if label_perso:
                                label_base = re.sub(r'[^A-Za-z]', '', label_perso.upper())
                                if not label_base:  # Si le label ne contient pas de lettres
                                    label_base = "PERSO"
                        
                        tag = f"{label_base}{tier_number}"
                        mapping[tag] = champ_perso
                        
                        # Remplacer toutes les occurrences (insensible à la casse)
                        pattern = re.compile(re.escape(champ_perso), re.IGNORECASE)
                        anonymized = pattern.sub(tag, anonymized)
                        
                        # Variantes: en majuscules, minuscules
                        if champ_perso.upper() != champ_perso:
                            anonymized = anonymized.replace(champ_perso.upper(), tag)
                        if champ_perso.lower() != champ_perso:
                            anonymized = anonymized.replace(champ_perso.lower(), tag)
    
    return anonymized, mapping 