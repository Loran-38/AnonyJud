#!/usr/bin/env python3
"""
Anonymisation PDF simplifiée avec pdf-redactor
Utilise les substitutions de texte dans le flux PDF pour préserver la mise en page
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

def anonymize_pdf_with_simple_redactor(pdf_content: bytes, tiers: List[Dict[str, Any]] = []) -> Tuple[bytes, Dict[str, str]]:
    """
    Anonymise un PDF en utilisant pdf-redactor avec une approche simplifiée.
    
    Args:
        pdf_content: Le contenu du fichier PDF original
        tiers: Liste des tiers avec leurs informations personnelles
        
    Returns:
        Tuple contenant (contenu_pdf_anonymisé, mapping_des_remplacements)
    """
    if not PDF_REDACTOR_SUPPORT:
        raise ImportError("Support pdf-redactor non disponible")
    
    logging.info("Début anonymisation PDF avec pdf-redactor simple")
    
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
            # Fonction de filtrage du contenu pour pdf-redactor
            def content_filter(text_content):
                """Filtre le contenu textuel du PDF"""
                filtered_text = text_content
                
                # Trier par longueur décroissante pour éviter les remplacements partiels
                sorted_items = sorted(mapping.items(), key=lambda x: len(x[1]), reverse=True)
                
                for tag, original_value in sorted_items:
                    if original_value in filtered_text:
                        filtered_text = filtered_text.replace(original_value, tag)
                        logging.debug(f"Remplacé '{original_value}' par '{tag}'")
                
                return filtered_text
            
            # Lire le PDF avec pdfrw
            pdf_reader = PdfReader(temp_input_path)
            
            # Appliquer les filtres de contenu
            if mapping:
                logging.info(f"Application du filtrage sur {len(mapping)} éléments")
                
                # Utiliser les fonctions de pdf_redactor pour traiter le PDF
                # Mettre à jour la couche de texte
                pdf_redactor.update_text_layer(pdf_reader, content_filter)
                
                # Écrire le PDF modifié
                pdf_writer = PdfWriter()
                for page in pdf_reader.pages:
                    pdf_writer.addPage(page)
                
                with open(temp_output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                # Lire le résultat
                with open(temp_output_path, 'rb') as output_file:
                    anonymized_content = output_file.read()
                
                logging.info("Anonymisation avec pdf-redactor simple terminée avec succès")
                
            else:
                # Aucune anonymisation à appliquer, retourner le PDF original
                anonymized_content = pdf_content
                logging.info("Aucune anonymisation à appliquer")
            
            return anonymized_content, mapping
            
        finally:
            # Nettoyer les fichiers temporaires
            try:
                os.unlink(temp_input_path)
                os.unlink(temp_output_path)
            except:
                pass
                
    except Exception as e:
        logging.error(f"Erreur lors de l'anonymisation avec pdf-redactor simple: {str(e)}")
        # Fallback vers l'ancienne méthode
        logging.info("Fallback vers l'ancienne méthode d'anonymisation")
        from .anonymizer import anonymize_pdf_file
        return anonymize_pdf_file(pdf_content, tiers)

def deanonymize_pdf_with_simple_redactor(pdf_content: bytes, mapping: Dict[str, str]) -> bytes:
    """
    Dé-anonymise un PDF en utilisant pdf-redactor avec une approche simplifiée.
    
    Args:
        pdf_content: Le contenu du fichier PDF anonymisé
        mapping: Dictionnaire de mapping des balises vers les valeurs originales
        
    Returns:
        bytes: Le contenu du fichier PDF dé-anonymisé
    """
    if not PDF_REDACTOR_SUPPORT:
        raise ImportError("Support pdf-redactor non disponible")
    
    logging.info("Début dé-anonymisation PDF avec pdf-redactor simple")
    
    try:
        # Créer un fichier temporaire pour le PDF d'entrée
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_input:
            temp_input.write(pdf_content)
            temp_input_path = temp_input.name
        
        # Créer un fichier temporaire pour le PDF de sortie
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_output:
            temp_output_path = temp_output.name
        
        try:
            # Fonction de filtrage du contenu pour la dé-anonymisation
            def content_filter(text_content):
                """Filtre le contenu textuel du PDF pour la dé-anonymisation"""
                filtered_text = text_content
                
                # Trier par longueur décroissante pour éviter les remplacements partiels
                sorted_tags = sorted(mapping.keys(), key=len, reverse=True)
                
                for tag in sorted_tags:
                    original_value = mapping[tag]
                    if tag in filtered_text:
                        filtered_text = filtered_text.replace(tag, original_value)
                        logging.debug(f"Remplacé '{tag}' par '{original_value}'")
                
                return filtered_text
            
            # Lire le PDF avec pdfrw
            pdf_reader = PdfReader(temp_input_path)
            
            # Appliquer les filtres de contenu
            if mapping:
                logging.info(f"Application du filtrage de dé-anonymisation sur {len(mapping)} éléments")
                
                # Utiliser les fonctions de pdf_redactor pour traiter le PDF
                # Mettre à jour la couche de texte
                pdf_redactor.update_text_layer(pdf_reader, content_filter)
                
                # Écrire le PDF modifié
                pdf_writer = PdfWriter()
                for page in pdf_reader.pages:
                    pdf_writer.addPage(page)
                
                with open(temp_output_path, 'wb') as output_file:
                    pdf_writer.write(output_file)
                
                # Lire le résultat
                with open(temp_output_path, 'rb') as output_file:
                    deanonymized_content = output_file.read()
                
                logging.info("Dé-anonymisation avec pdf-redactor simple terminée avec succès")
                
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
        logging.error(f"Erreur lors de la dé-anonymisation avec pdf-redactor simple: {str(e)}")
        # Fallback vers l'ancienne méthode
        logging.info("Fallback vers l'ancienne méthode de dé-anonymisation")
        from .anonymizer import deanonymize_pdf_file
        return deanonymize_pdf_file(pdf_content, mapping) 