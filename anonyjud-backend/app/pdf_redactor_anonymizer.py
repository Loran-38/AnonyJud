#!/usr/bin/env python3
"""
Anonymisation PDF avancée avec pdf-redactor
Préserve la mise en page et les styles originaux en utilisant des substitutions de texte dans le flux PDF
"""

import logging
import re
import tempfile
import os
from typing import Dict, List, Tuple, Any
from io import BytesIO

# Imports pour pdf-redactor
try:
    import pdf_redactor
    from pdfrw import PdfReader, PdfWriter
    import fitz  # PyMuPDF pour l'extraction de texte et validation
    PDF_REDACTOR_SUPPORT = True
    print("✓ Support pdf-redactor activé")
except ImportError as e:
    PDF_REDACTOR_SUPPORT = False
    print(f"⚠ Support pdf-redactor non disponible: {e}")
    print("Pour activer le support pdf-redactor, installez: pip install pdf-redactor")

def create_redaction_functions(mapping: Dict[str, str]) -> List:
    """
    Crée les fonctions de redaction pour pdf-redactor basées sur le mapping.
    
    Args:
        mapping: Dictionnaire {tag: original_value} pour l'anonymisation
                ou {tag: original_value} pour la dé-anonymisation
        
    Returns:
        List: Liste des fonctions de redaction pour pdf-redactor
    """
    redaction_functions = []
    
    # Trier par longueur décroissante pour éviter les remplacements partiels
    sorted_items = sorted(mapping.items(), key=lambda x: len(x[1]), reverse=True)
    
    for tag, original_value in sorted_items:
        # Créer une fonction de substitution pour chaque valeur
        def make_substitution_func(old_text, new_text):
            def substitution_func(text_obj):
                # Remplacer le texte en préservant la casse si possible
                if old_text in text_obj:
                    return text_obj.replace(old_text, new_text)
                # Essayer avec différentes variantes de casse
                if old_text.lower() in text_obj.lower():
                    # Utiliser une expression régulière pour un remplacement insensible à la casse
                    pattern = re.compile(re.escape(old_text), re.IGNORECASE)
                    return pattern.sub(new_text, text_obj)
                return text_obj
            return substitution_func
        
        redaction_functions.append(make_substitution_func(original_value, tag))
    
    return redaction_functions

def anonymize_pdf_with_redactor(pdf_content: bytes, tiers: List[Dict[str, Any]] = []) -> Tuple[bytes, Dict[str, str]]:
    """
    Anonymise un PDF en préservant la mise en page avec pdf-redactor.
    
    Args:
        pdf_content: Le contenu du fichier PDF original
        tiers: Liste des tiers avec leurs informations personnelles
        
    Returns:
        Tuple contenant (contenu_pdf_anonymisé, mapping_des_remplacements)
    """
    if not PDF_REDACTOR_SUPPORT:
        raise ImportError("Support pdf-redactor non disponible")
    
    logging.info("Début anonymisation PDF avec pdf-redactor")
    
    try:
        # Générer le mapping d'anonymisation
        from .anonymizer import anonymize_text
        
        # Extraire le texte pour générer le mapping
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        full_text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            full_text += page.get_text() + "\n"
        doc.close()
        
        # Générer le mapping avec la fonction existante
        _, mapping = anonymize_text(full_text, tiers)
        
        logging.info(f"Mapping généré: {mapping}")
        
        # Créer un fichier temporaire pour le PDF d'entrée
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
            temp_input.write(pdf_content)
            temp_input_path = temp_input.name
        
        # Créer un fichier temporaire pour le PDF de sortie
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Créer les fonctions de redaction
            redaction_functions = create_redaction_functions(mapping)
            
            logging.info(f"Créé {len(redaction_functions)} fonctions de redaction")
            
            # Appliquer l'anonymisation avec pdf-redactor
            if redaction_functions:
                # Utiliser pdf-redactor pour anonymiser
                options = {
                    'content_filters': redaction_functions,
                    'metadata_filters': {},  # Pas de filtrage de métadonnées pour l'instant
                    'xmp_filters': []  # Pas de filtrage XMP pour l'instant
                }
                
                # Lire le PDF d'entrée
                with open(temp_input_path, 'rb') as input_file:
                    input_pdf = input_file.read()
                
                # Appliquer les redactions
                output_pdf = pdf_redactor.redact_pdf(
                    input_pdf,
                    content_filters=redaction_functions
                )
                
                # Sauvegarder le PDF redacté
                with open(temp_output_path, 'wb') as output_file:
                    output_file.write(output_pdf)
                
                # Lire le résultat
                with open(temp_output_path, 'rb') as output_file:
                    anonymized_content = output_file.read()
                
                logging.info("Anonymisation avec pdf-redactor terminée avec succès")
                
            else:
                # Aucune redaction à appliquer, retourner le PDF original
                anonymized_content = pdf_content
                logging.info("Aucune redaction à appliquer")
            
            return anonymized_content, mapping
            
        finally:
            # Nettoyer les fichiers temporaires
            try:
                os.unlink(temp_input_path)
                os.unlink(temp_output_path)
            except:
                pass
                
    except Exception as e:
        logging.error(f"Erreur lors de l'anonymisation avec pdf-redactor: {str(e)}")
        # Fallback vers l'ancienne méthode
        logging.info("Fallback vers l'ancienne méthode d'anonymisation")
        from .anonymizer import anonymize_pdf_file
        return anonymize_pdf_file(pdf_content, tiers)

def deanonymize_pdf_with_redactor(pdf_content: bytes, mapping: Dict[str, str]) -> bytes:
    """
    Dé-anonymise un PDF en préservant la mise en page avec pdf-redactor.
    
    Args:
        pdf_content: Le contenu du fichier PDF anonymisé
        mapping: Dictionnaire de mapping des balises vers les valeurs originales
        
    Returns:
        bytes: Le contenu du fichier PDF dé-anonymisé
    """
    if not PDF_REDACTOR_SUPPORT:
        raise ImportError("Support pdf-redactor non disponible")
    
    logging.info("Début dé-anonymisation PDF avec pdf-redactor")
    
    try:
        # Créer un fichier temporaire pour le PDF d'entrée
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
            temp_input.write(pdf_content)
            temp_input_path = temp_input.name
        
        # Créer un fichier temporaire pour le PDF de sortie
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Créer les fonctions de dé-anonymisation (mapping inversé)
            # Pour la dé-anonymisation, on remplace les balises par les valeurs originales
            deanon_mapping = {v: k for k, v in mapping.items()}  # Inverser le mapping
            redaction_functions = create_redaction_functions(deanon_mapping)
            
            logging.info(f"Créé {len(redaction_functions)} fonctions de dé-anonymisation")
            
            # Appliquer la dé-anonymisation avec pdf-redactor
            if redaction_functions:
                # Lire le PDF d'entrée
                with open(temp_input_path, 'rb') as input_file:
                    input_pdf = input_file.read()
                
                # Appliquer les redactions
                output_pdf = pdf_redactor.redact_pdf(
                    input_pdf,
                    content_filters=redaction_functions
                )
                
                # Sauvegarder le PDF redacté
                with open(temp_output_path, 'wb') as output_file:
                    output_file.write(output_pdf)
                
                # Lire le résultat
                with open(temp_output_path, 'rb') as output_file:
                    deanonymized_content = output_file.read()
                
                logging.info("Dé-anonymisation avec pdf-redactor terminée avec succès")
                
            else:
                # Aucune dé-anonymisation à appliquer, retourner le PDF original
                deanonymized_content = pdf_content
                logging.info("Aucune dé-anonymisation à appliquer")
            
            return deanonymized_content
            
        finally:
            # Nettoyer les fichiers temporaires
            try:
                os.unlink(temp_input_path)
                os.unlink(temp_output_path)
            except:
                pass
                
    except Exception as e:
        logging.error(f"Erreur lors de la dé-anonymisation avec pdf-redactor: {str(e)}")
        # Fallback vers l'ancienne méthode
        logging.info("Fallback vers l'ancienne méthode de dé-anonymisation")
        from .anonymizer import deanonymize_pdf_file
        return deanonymize_pdf_file(pdf_content, mapping) 