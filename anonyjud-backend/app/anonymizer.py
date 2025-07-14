import re
import json
from typing import Dict, List, Tuple, Any

# Imports pour le support PDF
try:
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
    from reportlab.lib.units import inch
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    from io import BytesIO
    import logging
    PDF_SUPPORT = True
    print("✓ Support PDF activé avec reportlab")
except ImportError as e:
    PDF_SUPPORT = False
    print(f"⚠ Support PDF non disponible: {e}")
    print("Pour activer le support PDF, installez: pip install reportlab")

# Imports pour le pipeline PDF → Word → PDF avec préservation de mise en page
try:
    from pdf2docx import Converter
    import tempfile
    import os
    import subprocess
    import sys
    PDF_ENHANCED_PIPELINE = True
    print("✓ Pipeline PDF enhanced activé avec pdf2docx")
except ImportError as e:
    PDF_ENHANCED_PIPELINE = False
    print(f"⚠ Pipeline PDF enhanced non disponible: {e}")
    print("Pour activer le pipeline enhanced, installez: pip install pdf2docx")

# Import docx2pdf comme alternative à LibreOffice
try:
    from docx2pdf import convert as docx2pdf_convert
    DOCX2PDF_AVAILABLE = True
    print("✓ docx2pdf disponible pour conversion Word→PDF")
except ImportError as e:
    DOCX2PDF_AVAILABLE = False
    print(f"⚠ docx2pdf non disponible: {e}")
    print("Pour installer docx2pdf: pip install docx2pdf")


def anonymize_text(text: str, tiers: List[Dict[str, Any]] = []) -> Tuple[str, Dict[str, str]]:
    """
    Anonymise le texte en détectant les entités personnelles et en les remplaçant par des balises.
    Étendu : anonymise aussi les dates, numéros de sécurité sociale, numéros de carte, références, etc.
    
    Args:
        text: Le texte à anonymiser
        tiers: Liste des tiers avec leurs informations personnelles (optionnel)
        
    Returns:
        Tuple contenant (texte_anonymisé, mapping_des_remplacements)
    """
    # Initialiser le mapping des remplacements
    mapping = {}
    anonymized = text
    
    # --- ANONYMISATION DES DATES ---
    # Formats français courants : 15/12/2023, 15-12-2023, 15 décembre 2023, 2023-12-15, etc.
    date_patterns = [
        r'\b(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})\b',  # 15/12/2023 ou 15-12-2023
        r'\b(\d{4}[/-]\d{1,2}[/-]\d{1,2})\b',    # 2023-12-15
        r'\b(\d{1,2} [a-zA-Zéûî]+ \d{4})\b',      # 15 décembre 2023
    ]
    date_count = 1
    for pattern in date_patterns:
        for match in re.finditer(pattern, anonymized):
            date = match.group(0)
            if date not in mapping.values():
                tag = f"DATE{date_count}"
                mapping[tag] = date
                anonymized = anonymized.replace(date, tag)
                date_count += 1

    # --- ANONYMISATION NUMÉROS DE SÉCURITÉ SOCIALE (NIR) ---
    nir_pattern = r'\b(\d{2} ?\d{2} ?\d{2} ?\d{3} ?\d{3} ?\d{2})\b'
    nir_count = 1
    for match in re.finditer(nir_pattern, anonymized):
        nir = match.group(0)
        if nir not in mapping.values():
            tag = f"NIR{nir_count}"
            mapping[tag] = nir
            anonymized = anonymized.replace(nir, tag)
            nir_count += 1

    # --- ANONYMISATION NUMÉROS DE CARTE BANCAIRE ---
    cb_pattern = r'\b(\d{4} ?\d{4} ?\d{4} ?\d{4})\b'
    cb_count = 1
    for match in re.finditer(cb_pattern, anonymized):
        cb = match.group(0)
        if cb not in mapping.values():
            tag = f"CB{cb_count}"
            mapping[tag] = cb
            anonymized = anonymized.replace(cb, tag)
            cb_count += 1

    # --- ANONYMISATION NUMÉROS DE DOSSIER/RÉFÉRENCE ---
    ref_pattern = r'\b([A-Z]{2,5}\d{3,10})\b'
    ref_count = 1
    for match in re.finditer(ref_pattern, anonymized):
        ref = match.group(0)
        if ref not in mapping.values():
            tag = f"REF{ref_count}"
            mapping[tag] = ref
            anonymized = anonymized.replace(ref, tag)
            ref_count += 1

    # --- ANONYMISATION NUMÉROS SIMPLES (hors téléphone déjà géré) ---
    simple_num_pattern = r'\b(\d{6,})\b'
    num_count = 1
    for match in re.finditer(simple_num_pattern, anonymized):
        num = match.group(0)
        if num not in mapping.values():
            tag = f"NUM{num_count}"
            mapping[tag] = num
            anonymized = anonymized.replace(num, tag)
            num_count += 1

    # --- ANONYMISATION CLASSIQUE (tiers, emails, etc.) ---
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
            # Utiliser le numéro fixe du tiers ou fallback sur l'index + 1
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

def create_pdf_from_text(text: str, title: str = "Document anonymisé") -> bytes:
    """
    Crée un fichier PDF à partir d'un texte donné.
    
    Args:
        text: Le texte à convertir en PDF
        title: Le titre du document PDF
        
    Returns:
        bytes: Le contenu du fichier PDF
    """
    if not PDF_SUPPORT:
        raise ImportError("Support PDF non disponible. Installez reportlab: pip install reportlab")
    
    logging.info(f"Création PDF - Titre: {title}, Taille texte: {len(text)} caractères")
    
    # Créer un buffer en mémoire pour le PDF
    buffer = BytesIO()
    
    # Créer le document PDF
    doc = SimpleDocTemplate(buffer, pagesize=A4, 
                          rightMargin=72, leftMargin=72,
                          topMargin=72, bottomMargin=18)
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    normal_style.alignment = TA_JUSTIFY
    
    # Contenu du PDF
    story = []
    
    # Titre
    if title:
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
    
    # Diviser le texte en paragraphes
    paragraphs = text.split('\n\n')
    
    for paragraph in paragraphs:
        if paragraph.strip():
            # Nettoyer le paragraphe
            clean_paragraph = paragraph.strip().replace('\n', ' ')
            # Échapper les caractères spéciaux pour reportlab
            clean_paragraph = clean_paragraph.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(clean_paragraph, normal_style))
            story.append(Spacer(1, 12))
    
    # Construire le PDF
    doc.build(story)
    
    # Récupérer le contenu du buffer
    pdf_content = buffer.getvalue()
    buffer.close()
    
    logging.info(f"PDF créé avec succès - Taille: {len(pdf_content)} bytes")
    return pdf_content

def anonymize_pdf_file(file_content: bytes, tiers: List[Dict[str, Any]] = []) -> Tuple[bytes, Dict[str, str]]:
    """
    Anonymise un fichier PDF en extrayant le texte, l'anonymisant et créant un nouveau PDF.
    
    Args:
        file_content: Le contenu du fichier PDF original
        tiers: Liste des tiers avec leurs informations personnelles
        
    Returns:
        Tuple contenant (contenu_pdf_anonymisé, mapping_des_remplacements)
    """
    if not PDF_SUPPORT:
        raise ImportError("Support PDF non disponible. Installez reportlab: pip install reportlab")
    
    logging.info("Début anonymisation PDF")
    
    try:
        # Importer la fonction d'extraction de texte PDF
        from .utils import extract_text_from_pdf
        
        # Extraire le texte du PDF original
        extracted_text = extract_text_from_pdf(file_content)
        
        logging.info(f"Texte extrait du PDF - Taille: {len(extracted_text)} caractères")
        
        # Anonymiser le texte
        anonymized_text, mapping = anonymize_text(extracted_text, tiers)
        
        logging.info(f"Texte anonymisé - Nouvelles balises: {len(mapping)}")
        
        # Créer un nouveau PDF avec le texte anonymisé
        pdf_content = create_pdf_from_text(anonymized_text, "Document PDF Anonymisé")
        
        logging.info("Anonymisation PDF terminée avec succès")
        return pdf_content, mapping
        
    except Exception as e:
        logging.error(f"Erreur lors de l'anonymisation PDF: {str(e)}")
        raise

def deanonymize_pdf_file(file_content: bytes, mapping: Dict[str, str]) -> bytes:
    """
    Dé-anonymise un fichier PDF en remplaçant les balises par les valeurs originales.
    
    Args:
        file_content: Le contenu du fichier PDF anonymisé
        mapping: Dictionnaire de mapping des balises vers les valeurs originales
        
    Returns:
        bytes: Le contenu du fichier PDF dé-anonymisé
    """
    if not PDF_SUPPORT:
        raise ImportError("Support PDF non disponible. Installez reportlab: pip install reportlab")
    
    logging.info("Début dé-anonymisation PDF")
    
    try:
        # Importer la fonction d'extraction de texte PDF
        from .utils import extract_text_from_pdf
        
        # Extraire le texte du PDF anonymisé
        extracted_text = extract_text_from_pdf(file_content)
        
        logging.info(f"Texte extrait du PDF anonymisé - Taille: {len(extracted_text)} caractères")
        
        # Dé-anonymiser le texte
        deanonymized_text = extracted_text
        
        if mapping:
            logging.info(f"Application du mapping - {len(mapping)} remplacements")
            
            for tag, original_value in mapping.items():
                if tag in deanonymized_text:
                    deanonymized_text = deanonymized_text.replace(tag, original_value)
                    logging.debug(f"Remplacé {tag} par {original_value}")
        
        logging.info("Dé-anonymisation du texte terminée")
        
        # Créer un nouveau PDF avec le texte dé-anonymisé
        pdf_content = create_pdf_from_text(deanonymized_text, "Document PDF Dé-anonymisé")
        
        logging.info("Dé-anonymisation PDF terminée avec succès")
        return pdf_content
        
    except Exception as e:
        logging.error(f"Erreur lors de la dé-anonymisation PDF: {str(e)}")
        raise 


# ===== NOUVEAU PIPELINE PDF → WORD → PDF =====

def convert_pdf_to_word_enhanced(pdf_content: bytes) -> bytes:
    """
    Convertit un PDF en Word en préservant strictement la mise en page avec pdf2docx.
    
    Args:
        pdf_content: Le contenu du fichier PDF
        
    Returns:
        bytes: Le contenu du fichier Word (.docx) généré
    """
    if not PDF_ENHANCED_PIPELINE:
        raise ImportError("Pipeline PDF enhanced non disponible. Installez pdf2docx: pip install pdf2docx")
    
    logging.info("🔄 Début conversion PDF → Word avec préservation de mise en page")
    
    try:
        # Créer des fichiers temporaires pour la conversion
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(pdf_content)
            temp_pdf_path = temp_pdf.name
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
            temp_docx_path = temp_docx.name
        
        try:
            # Conversion PDF → DOCX avec pdf2docx
            logging.info(f"📄 Conversion de {temp_pdf_path} vers {temp_docx_path}")
            
            # Utiliser pdf2docx pour convertir avec préservation maximale
            # Paramètres optimisés pour préserver la mise en page
            cv = Converter(temp_pdf_path)
            cv.convert(temp_docx_path, 
                      start=0, 
                      # Paramètres pour préserver au maximum la mise en page
                      multi_processing=False)  # Éviter les problèmes de concurrence
            cv.close()
            
            logging.info(f"✅ Conversion pdf2docx terminée")
            
            # Lire le fichier Word généré
            with open(temp_docx_path, 'rb') as f:
                docx_content = f.read()
            
            logging.info(f"✅ Conversion PDF → Word réussie. Taille DOCX: {len(docx_content)} bytes")
            return docx_content
            
        finally:
            # Nettoyer les fichiers temporaires
            if os.path.exists(temp_pdf_path):
                os.unlink(temp_pdf_path)
            if os.path.exists(temp_docx_path):
                os.unlink(temp_docx_path)
    
    except Exception as e:
        logging.error(f"❌ Erreur lors de la conversion PDF → Word: {str(e)}")
        raise Exception(f"Erreur conversion PDF → Word: {str(e)}")


def convert_word_to_pdf_enhanced(docx_content: bytes) -> bytes:
    """
    Convertit un fichier Word en PDF en préservant la mise en page.
    Utilise plusieurs méthodes par ordre de préférence pour la préservation.
    
    Args:
        docx_content: Le contenu du fichier Word (.docx)
        
    Returns:
        bytes: Le contenu du fichier PDF généré
    """
    logging.info("🔄 Début conversion Word → PDF avec préservation de mise en page")
    
    # Méthode 1: docx2pdf (Windows, meilleure préservation)
    if DOCX2PDF_AVAILABLE:
        try:
            logging.info("🔄 Tentative conversion avec docx2pdf...")
            return _convert_word_to_pdf_docx2pdf(docx_content)
        except Exception as e:
            logging.warning(f"⚠️ docx2pdf échoué: {str(e)}")
    
    # Méthode 2: LibreOffice headless (cross-platform, bonne préservation)
    try:
        logging.info("🔄 Tentative conversion avec LibreOffice...")
        return _convert_word_to_pdf_libreoffice(docx_content)
    except Exception as e:
        logging.warning(f"⚠️ LibreOffice non disponible: {str(e)}")
        
    # Méthode 3: Fallback amélioré avec reportlab (préservation partielle)
    try:
        logging.info("🔄 Fallback: conversion améliorée avec reportlab...")
        return _convert_word_to_pdf_reportlab_enhanced(docx_content)
    except Exception as e2:
        logging.error(f"❌ Toutes les méthodes de conversion ont échoué: {str(e2)}")
        raise Exception(f"Impossible de convertir Word → PDF: {str(e2)}")


def _convert_word_to_pdf_docx2pdf(docx_content: bytes) -> bytes:
    """
    Convertit Word → PDF avec docx2pdf (Windows uniquement, excellente préservation).
    """
    if not DOCX2PDF_AVAILABLE:
        raise ImportError("docx2pdf non disponible")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        temp_docx.write(docx_content)
        temp_docx_path = temp_docx.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf_path = temp_pdf.name
    
    try:
        # Utiliser docx2pdf pour la conversion
        logging.info(f"📄 Conversion docx2pdf: {temp_docx_path} → {temp_pdf_path}")
        docx2pdf_convert(temp_docx_path, temp_pdf_path)
        
        # Vérifier que le fichier PDF a été créé
        if not os.path.exists(temp_pdf_path):
            raise Exception(f"Fichier PDF non généré par docx2pdf: {temp_pdf_path}")
        
        # Lire le PDF généré
        with open(temp_pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        logging.info(f"✅ Conversion docx2pdf réussie. Taille PDF: {len(pdf_content)} bytes")
        return pdf_content
        
    finally:
        # Nettoyer les fichiers temporaires
        if os.path.exists(temp_docx_path):
            os.unlink(temp_docx_path)
        if os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)


def _convert_word_to_pdf_libreoffice(docx_content: bytes) -> bytes:
    """
    Convertit Word → PDF avec LibreOffice en mode headless (préservation maximale).
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=".docx") as temp_docx:
        temp_docx.write(docx_content)
        temp_docx_path = temp_docx.name
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
        temp_pdf_path = temp_pdf.name
    
    try:
        # Déterminer la commande LibreOffice selon l'OS
        if sys.platform == "win32":
            # Windows
            libreoffice_commands = [
                "soffice",
                "libreoffice",
                r"C:\Program Files\LibreOffice\program\soffice.exe",
                r"C:\Program Files (x86)\LibreOffice\program\soffice.exe"
            ]
        elif sys.platform == "darwin":
            # macOS
            libreoffice_commands = [
                "/Applications/LibreOffice.app/Contents/MacOS/soffice",
                "soffice",
                "libreoffice"
            ]
        else:
            # Linux
            libreoffice_commands = [
                "soffice",
                "libreoffice",
                "/usr/bin/soffice",
                "/opt/libreoffice7.1/program/soffice"
            ]
        
        # Essayer chaque commande jusqu'à ce qu'une fonctionne
        success = False
        for cmd in libreoffice_commands:
            try:
                # Commande LibreOffice headless
                result = subprocess.run([
                    cmd,
                    "--headless",
                    "--convert-to", "pdf",
                    "--outdir", os.path.dirname(temp_pdf_path),
                    temp_docx_path
                ], capture_output=True, text=True, timeout=30)
                
                if result.returncode == 0:
                    success = True
                    logging.info(f"✅ LibreOffice conversion réussie avec: {cmd}")
                    break
                else:
                    logging.debug(f"❌ Commande {cmd} échouée: {result.stderr}")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                logging.debug(f"❌ Commande {cmd} non trouvée ou timeout: {str(e)}")
                continue
        
        if not success:
            raise Exception("LibreOffice non trouvé ou échec de conversion")
        
        # Le fichier PDF généré aura le même nom de base que le docx
        expected_pdf_path = temp_docx_path.replace('.docx', '.pdf')
        
        if not os.path.exists(expected_pdf_path):
            raise Exception(f"Fichier PDF non généré: {expected_pdf_path}")
        
        # Lire le PDF généré
        with open(expected_pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        logging.info(f"✅ Conversion Word → PDF réussie. Taille PDF: {len(pdf_content)} bytes")
        return pdf_content
        
    finally:
        # Nettoyer les fichiers temporaires
        if os.path.exists(temp_docx_path):
            os.unlink(temp_docx_path)
        if os.path.exists(temp_pdf_path):
            os.unlink(temp_pdf_path)
        
        # Nettoyer le PDF généré par LibreOffice
        expected_pdf_path = temp_docx_path.replace('.docx', '.pdf')
        if os.path.exists(expected_pdf_path):
            os.unlink(expected_pdf_path)


def _convert_word_to_pdf_reportlab(docx_content: bytes) -> bytes:
    """
    Méthode de fallback: extrait le texte du Word et génère un PDF avec reportlab.
    """
    if not PDF_SUPPORT:
        raise ImportError("Support PDF non disponible. Installez reportlab: pip install reportlab")
    
    from docx import Document
    
    # Extraire le texte du document Word
    doc = Document(BytesIO(docx_content))
    text = ""
    
    for para in doc.paragraphs:
        text += para.text + "\n"
    
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for para in cell.paragraphs:
                    text += para.text + "\n"
    
    # Générer un PDF avec le texte extrait
    return create_pdf_from_text(text, "Document converti depuis Word")


def _convert_word_to_pdf_reportlab_enhanced(docx_content: bytes) -> bytes:
    """
    Méthode de fallback améliorée: extrait le texte du Word avec préservation partielle de la structure.
    """
    if not PDF_SUPPORT:
        raise ImportError("Support PDF non disponible. Installez reportlab: pip install reportlab")
    
    from docx import Document
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.enums import TA_JUSTIFY, TA_LEFT, TA_CENTER
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    
    # Ouvrir le document Word
    doc = Document(BytesIO(docx_content))
    
    # Créer un buffer pour le PDF
    buffer = BytesIO()
    pdf_doc = SimpleDocTemplate(buffer, pagesize=A4, 
                               rightMargin=72, leftMargin=72,
                               topMargin=72, bottomMargin=72)
    
    # Styles
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']
    normal_style.alignment = TA_JUSTIFY
    normal_style.fontSize = 11
    normal_style.leading = 14
    
    # Titre style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=16,
        spaceAfter=12,
        alignment=TA_CENTER
    )
    
    # Sous-titre style
    subtitle_style = ParagraphStyle(
        'CustomSubtitle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=8,
        alignment=TA_LEFT
    )
    
    story = []
    
    # Traiter chaque paragraphe
    for para in doc.paragraphs:
        if para.text.strip():
            text = para.text.strip()
            
            # Échapper les caractères spéciaux
            text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            
            # Détecter les titres (heuristique simple)
            if len(text) < 100 and (text.isupper() or text.startswith('TITRE') or text.startswith('CHAPITRE')):
                story.append(Paragraph(text, title_style))
            elif len(text) < 80 and text.endswith(':'):
                story.append(Paragraph(text, subtitle_style))
            else:
                story.append(Paragraph(text, normal_style))
            
            story.append(Spacer(1, 6))
    
    # Traiter les tableaux
    for table in doc.tables:
        table_data = []
        for row in table.rows:
            row_data = []
            for cell in row.cells:
                cell_text = ""
                for para in cell.paragraphs:
                    if para.text.strip():
                        cell_text += para.text.strip() + " "
                row_data.append(cell_text.strip())
            if any(row_data):  # Seulement si la ligne n'est pas vide
                table_data.append(row_data)
        
        if table_data:
            # Créer le tableau PDF
            pdf_table = Table(table_data)
            pdf_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            story.append(pdf_table)
            story.append(Spacer(1, 12))
    
    # Construire le PDF
    pdf_doc.build(story)
    
    # Récupérer le contenu
    pdf_content = buffer.getvalue()
    buffer.close()
    
    logging.info(f"✅ Conversion reportlab enhanced réussie. Taille PDF: {len(pdf_content)} bytes")
    return pdf_content


def anonymize_pdf_enhanced_pipeline(pdf_content: bytes, tiers: List[Dict[str, Any]] = []) -> Tuple[bytes, Dict[str, str]]:
    """
    Pipeline complet : PDF → Word → Anonymisation → PDF
    Préserve la mise en page tout au long du processus.
    
    Args:
        pdf_content: Le contenu du fichier PDF original
        tiers: Liste des tiers avec leurs informations personnelles
        
    Returns:
        Tuple contenant (pdf_anonymisé, mapping_des_remplacements)
    """
    logging.info("🚀 Début du pipeline PDF enhanced: PDF → Word → Anonymisation → PDF")
    logging.info(f"📊 Taille PDF d'entrée: {len(pdf_content)} bytes")
    logging.info(f"👥 Nombre de tiers: {len(tiers)}")
    
    try:
        # Étape 1: PDF → Word avec préservation de mise en page
        logging.info("📄 Étape 1/3: Conversion PDF → Word")
        docx_content = convert_pdf_to_word_enhanced(pdf_content)
        logging.info(f"✅ PDF → Word réussi. Taille DOCX: {len(docx_content)} bytes")
        
        # Étape 2: Anonymisation du fichier Word (préserve le formatage)
        logging.info("🔒 Étape 2/3: Anonymisation du document Word")
        from .main import anonymize_docx_file  # Import dynamique pour éviter la circularité
        anonymized_docx_content, mapping = anonymize_docx_file(docx_content, tiers)
        logging.info(f"✅ Anonymisation Word réussie. Taille DOCX anonymisé: {len(anonymized_docx_content)} bytes")
        logging.info(f"📊 Mapping généré: {len(mapping)} remplacements - {list(mapping.keys())}")
        
        # Étape 3: Word anonymisé → PDF final
        logging.info("📄 Étape 3/3: Conversion Word anonymisé → PDF")
        final_pdf_content = convert_word_to_pdf_enhanced(anonymized_docx_content)
        logging.info(f"✅ Word → PDF réussi. Taille PDF final: {len(final_pdf_content)} bytes")
        
        logging.info(f"🎉 Pipeline PDF enhanced terminé avec succès")
        logging.info(f"📊 Résumé: PDF({len(pdf_content)}) → DOCX({len(docx_content)}) → DOCX_ANONYM({len(anonymized_docx_content)}) → PDF_FINAL({len(final_pdf_content)})")
        
        return final_pdf_content, mapping
        
    except Exception as e:
        logging.error(f"❌ Erreur dans le pipeline PDF enhanced: {str(e)}")
        raise Exception(f"Erreur pipeline PDF enhanced: {str(e)}")


def deanonymize_pdf_enhanced_pipeline(pdf_content: bytes, mapping: Dict[str, str]) -> bytes:
    """
    Pipeline de dé-anonymisation : PDF → Word → Dé-anonymisation → PDF
    Préserve la mise en page tout au long du processus.
    
    Args:
        pdf_content: Le contenu du fichier PDF anonymisé
        mapping: Dictionnaire de mapping des balises vers les valeurs originales
        
    Returns:
        bytes: Le contenu du fichier PDF dé-anonymisé
    """
    logging.info("🔓 Début du pipeline PDF dé-anonymisation enhanced")
    
    try:
        # Étape 1: PDF anonymisé → Word avec préservation de mise en page
        logging.info("📄 Étape 1/3: Conversion PDF anonymisé → Word")
        docx_content = convert_pdf_to_word_enhanced(pdf_content)
        
        # Étape 2: Dé-anonymisation du fichier Word (préserve le formatage)
        logging.info("🔓 Étape 2/3: Dé-anonymisation du document Word")
        from .main import deanonymize_docx_file  # Import dynamique pour éviter la circularité
        deanonymized_docx_content = deanonymize_docx_file(docx_content, mapping)
        
        # Étape 3: Word dé-anonymisé → PDF final
        logging.info("📄 Étape 3/3: Conversion Word dé-anonymisé → PDF")
        final_pdf_content = convert_word_to_pdf_enhanced(deanonymized_docx_content)
        
        logging.info(f"✅ Pipeline PDF dé-anonymisation enhanced terminé avec succès")
        
        return final_pdf_content
        
    except Exception as e:
        logging.error(f"❌ Erreur dans le pipeline PDF dé-anonymisation enhanced: {str(e)}")
        raise Exception(f"Erreur pipeline PDF dé-anonymisation enhanced: {str(e)}") 


# ===== ANONYMISATION DIRECTE PDF AVEC PYMUPDF =====

def anonymize_pdf_direct(pdf_content: bytes, tiers: List[Dict[str, Any]] = []) -> Tuple[bytes, Dict[str, str]]:
    """
    Anonymise directement un PDF en remplaçant le texte in-place avec PyMuPDF.
    Préserve parfaitement la mise en page, les polices, les couleurs et la structure.
    
    Args:
        pdf_content: Le contenu du fichier PDF original
        tiers: Liste des tiers avec leurs informations personnelles
        
    Returns:
        Tuple contenant (pdf_anonymisé, mapping_des_remplacements)
    """
    import fitz  # PyMuPDF
    
    logging.info("🚀 Début anonymisation PDF directe avec PyMuPDF")
    logging.info(f"📊 Taille PDF d'entrée: {len(pdf_content)} bytes")
    logging.info(f"👥 Nombre de tiers: {len(tiers)}")
    
    try:
        # Générer le mapping d'anonymisation
        full_text = ""
        
        # Ouvrir le PDF avec gestion d'erreur MuPDF améliorée
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
        except Exception as e:
            if "object out of range" in str(e):
                logging.warning(f"⚠️ Erreur MuPDF 'object out of range': {str(e)}")
                # Essayer de récupérer le PDF en mode tolérant
                try:
                    doc = fitz.open(stream=pdf_content, filetype="pdf")
                    # Réparer le PDF si possible
                    doc.save(doc.name, garbage=4, deflate=True)
                    doc.close()
                    doc = fitz.open(stream=pdf_content, filetype="pdf")
                except:
                    logging.error(f"❌ Impossible de réparer le PDF: {str(e)}")
                    raise Exception(f"PDF corrompu ou non supporté: {str(e)}")
            else:
                raise
        
        # Extraire tout le texte pour générer le mapping
        for page in doc:
            try:
                full_text += page.get_text() + "\n"
            except Exception as e:
                logging.warning(f"⚠️ Erreur extraction texte page: {str(e)}")
                continue
        
        doc.close()
        
        # Générer le mapping d'anonymisation
        anonymized_text, mapping = anonymize_text(full_text, tiers)
        logging.info(f"📊 Mapping généré: {len(mapping)} remplacements - {list(mapping.keys())}")
        
        # Inverser le mapping pour avoir {valeur_originale: balise_anonymisée}
        reverse_mapping = {v: k for k, v in mapping.items()}
        logging.info(f"📊 Mapping inversé: {reverse_mapping}")
        
        # Ouvrir le PDF pour modification avec gestion d'erreur améliorée
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
        except Exception as e:
            if "object out of range" in str(e):
                logging.warning(f"⚠️ Erreur MuPDF lors de l'ouverture pour modification: {str(e)}")
                # Continuer avec le document tel quel
                doc = fitz.open(stream=pdf_content, filetype="pdf")
            else:
                raise
        
        # Parcourir chaque page
        for page_num in range(len(doc)):
            page = doc[page_num]
            logging.info(f"📄 Traitement page {page_num + 1}/{len(doc)}")
            
            try:
                # Obtenir tous les blocs de texte de la page
                text_blocks = page.get_text("dict")
                
                # Parcourir chaque bloc de texte avec alignement parfait amélioré
                for block in text_blocks["blocks"]:
                    if "lines" in block:  # Bloc de texte
                        _anonymize_text_block_comprehensive(page, block, reverse_mapping)
                        
            except Exception as e:
                logging.warning(f"⚠️ Erreur traitement page {page_num + 1}: {str(e)}")
                continue
        
        # Sauvegarder le PDF modifié avec gestion d'erreur améliorée
        try:
            anonymized_pdf = doc.tobytes()
        except Exception as e:
            if "object out of range" in str(e):
                logging.warning(f"⚠️ Erreur MuPDF lors de la sauvegarde: {str(e)}")
                # Essayer de sauvegarder avec nettoyage
                try:
                    doc.save(doc.name, garbage=4, deflate=True)
                    anonymized_pdf = doc.tobytes()
                except:
                    logging.error(f"❌ Impossible de sauvegarder le PDF: {str(e)}")
                    raise Exception(f"Erreur sauvegarde PDF: {str(e)}")
            else:
                raise
        
        doc.close()
        
        logging.info(f"✅ Anonymisation PDF directe terminée avec succès")
        logging.info(f"📊 Taille PDF anonymisé: {len(anonymized_pdf)} bytes")
        
        return anonymized_pdf, mapping
        
    except Exception as e:
        logging.error(f"❌ Erreur lors de l'anonymisation PDF directe: {str(e)}")
        raise Exception(f"Erreur anonymisation PDF directe: {str(e)}")


def deanonymize_pdf_direct(pdf_content: bytes, mapping: Dict[str, str]) -> bytes:
    """
    Dé-anonymise directement un PDF en remplaçant les balises par les valeurs originales.
    Préserve parfaitement la mise en page, les polices, les couleurs et la structure.
    
    Args:
        pdf_content: Le contenu du fichier PDF anonymisé
        mapping: Dictionnaire de mapping des balises vers les valeurs originales
        
    Returns:
        bytes: Le contenu du fichier PDF dé-anonymisé
    """
    import fitz  # PyMuPDF
    
    logging.info("🚀 Début dé-anonymisation PDF directe avec PyMuPDF")
    logging.info(f"📊 Taille PDF d'entrée: {len(pdf_content)} bytes")
    logging.info(f"📊 Mapping: {len(mapping)} remplacements - {list(mapping.keys())}")
    
    try:
        # Ouvrir le PDF avec gestion d'erreur MuPDF améliorée
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
        except Exception as e:
            if "object out of range" in str(e):
                logging.warning(f"⚠️ Erreur MuPDF 'object out of range': {str(e)}")
                # Essayer de récupérer le PDF en mode tolérant
                try:
                    doc = fitz.open(stream=pdf_content, filetype="pdf")
                    # Réparer le PDF si possible
                    doc.save(doc.name, garbage=4, deflate=True)
                    doc.close()
                    doc = fitz.open(stream=pdf_content, filetype="pdf")
                except:
                    logging.error(f"❌ Impossible de réparer le PDF: {str(e)}")
                    raise Exception(f"PDF corrompu ou non supporté: {str(e)}")
            else:
                raise
        
        # Parcourir chaque page
        for page_num in range(len(doc)):
            page = doc[page_num]
            logging.info(f"📄 Traitement page {page_num + 1}/{len(doc)}")
            
            try:
                # Obtenir tous les blocs de texte de la page
                text_blocks = page.get_text("dict")
                
                # Parcourir chaque bloc de texte avec alignement parfait amélioré
                for block in text_blocks["blocks"]:
                    if "lines" in block:  # Bloc de texte
                        _deanonymize_text_block_comprehensive(page, block, mapping)
                        
            except Exception as e:
                logging.warning(f"⚠️ Erreur traitement page {page_num + 1}: {str(e)}")
                continue
        
        # Sauvegarder le PDF modifié avec gestion d'erreur améliorée
        try:
            deanonymized_pdf = doc.tobytes()
        except Exception as e:
            if "object out of range" in str(e):
                logging.warning(f"⚠️ Erreur MuPDF lors de la sauvegarde: {str(e)}")
                # Essayer de sauvegarder avec nettoyage
                try:
                    doc.save(doc.name, garbage=4, deflate=True)
                    deanonymized_pdf = doc.tobytes()
                except:
                    logging.error(f"❌ Impossible de sauvegarder le PDF: {str(e)}")
                    raise Exception(f"Erreur sauvegarde PDF: {str(e)}")
            else:
                raise
        
        doc.close()
        
        logging.info(f"✅ Dé-anonymisation PDF directe terminée avec succès")
        logging.info(f"📊 Taille PDF dé-anonymisé: {len(deanonymized_pdf)} bytes")
        
        return deanonymized_pdf
        
    except Exception as e:
        logging.error(f"❌ Erreur lors de la dé-anonymisation PDF directe: {str(e)}")
        raise Exception(f"Erreur dé-anonymisation PDF directe: {str(e)}")


def _calculate_text_baseline_position(bbox, font_size):
    """
    Calcule la position optimale pour insérer du texte en tenant compte de la ligne de base.
    
    Args:
        bbox: Rectangle englobant du texte original (fitz.Rect)
        font_size: Taille de la police
        
    Returns:
        tuple: (x, y) position pour insert_text
    """
    # Calculer la ligne de base approximative
    # La ligne de base est généralement située à environ 20-25% de la hauteur depuis le bas
    height = bbox.height
    baseline_offset = height * 0.2  # 20% depuis le bas
    
    # Position x: coin gauche de la boîte
    x = bbox.x0
    
    # Position y: bas de la boîte + offset de ligne de base
    y = bbox.y1 - baseline_offset
    
    return (x, y)


def _get_text_width_estimation(text, font_size):
    """
    Estime la largeur du texte pour vérifier s'il rentre dans la boîte englobante.
    
    Args:
        text: Texte à mesurer
        font_size: Taille de la police
        
    Returns:
        float: Largeur estimée du texte
    """
    # Estimation approximative: largeur moyenne d'un caractère = 0.6 * font_size
    avg_char_width = font_size * 0.6
    return len(text) * avg_char_width


def _adjust_font_size_to_fit(text, bbox, original_font_size):
    """
    Ajuste la taille de la police pour que le texte rentre dans la boîte englobante.
    
    Args:
        text: Texte à insérer
        bbox: Rectangle englobant disponible
        original_font_size: Taille de police originale
        
    Returns:
        float: Taille de police ajustée
    """
    available_width = bbox.width
    estimated_width = _get_text_width_estimation(text, original_font_size)
    
    if estimated_width <= available_width:
        return original_font_size
    
    # Calculer le facteur de réduction nécessaire
    scale_factor = available_width / estimated_width
    adjusted_size = original_font_size * scale_factor
    
    # Ne pas descendre en dessous de 6pt pour la lisibilité
    return max(adjusted_size, 6.0)


def _anonymize_text_block_direct(page, block, mapping: Dict[str, str]):
    """
    Anonymise un bloc de texte directement dans la page PDF avec positionnement précis.
    Le mapping contient: {valeur_originale: balise_anonymisée}
    """
    import fitz
    
    for line in block["lines"]:
        for span in line["spans"]:
            original_text = span["text"]
            
            if not original_text.strip():
                continue
                
            # Appliquer les remplacements du mapping
            anonymized_text = original_text
            text_changed = False
            
            # Le mapping contient {valeur_originale: balise_anonymisée}
            # Trier les clés par longueur décroissante pour éviter les remplacements partiels
            sorted_items = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
            
            for original_value, anonymized_tag in sorted_items:
                if original_value in anonymized_text:
                    anonymized_text = anonymized_text.replace(original_value, anonymized_tag)
                    text_changed = True
                    logging.debug(f"🔄 Remplacement: '{original_value}' → '{anonymized_tag}'")
            
            # Si le texte a changé, le remplacer dans le PDF
            if text_changed and anonymized_text != original_text:
                # Obtenir les propriétés du texte original
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                
                # Ajuster la taille de la police si nécessaire
                adjusted_font_size = _adjust_font_size_to_fit(anonymized_text, bbox, font_size)
                
                # Calculer la position optimale pour la ligne de base
                text_position = _calculate_text_baseline_position(bbox, adjusted_font_size)
                
                # Effacer l'ancien texte en le couvrant avec un rectangle blanc
                page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                
                # Insérer le nouveau texte anonymisé avec positionnement précis
                try:
                    page.insert_text(
                        text_position,  # Position calculée pour la ligne de base
                        anonymized_text,
                        fontname=font_name,
                        fontsize=adjusted_font_size,
                        color=text_color
                    )
                    logging.debug(f"✅ Texte remplacé avec positionnement précis: '{original_text}' → '{anonymized_text}' (taille: {adjusted_font_size})")
                except Exception as e:
                    logging.warning(f"⚠️ Erreur remplacement texte: {str(e)}")
                    # Fallback: utiliser une police par défaut avec positionnement précis
                    try:
                        page.insert_text(
                            text_position,
                            anonymized_text,
                            fontname="helv",  # Police par défaut
                            fontsize=adjusted_font_size,
                            color=text_color
                        )
                        logging.debug(f"✅ Texte remplacé avec police par défaut et positionnement précis")
                    except Exception as e2:
                        logging.error(f"❌ Impossible de remplacer le texte: {str(e2)}")


def _calculate_precise_text_position(bbox, text, fontname, fontsize, page):
    """
    Calcule la position ultra-précise pour insérer du texte en utilisant les métriques réelles.
    
    Args:
        bbox: Rectangle englobant du texte original (fitz.Rect)
        text: Texte à insérer
        fontname: Nom de la police
        fontsize: Taille de la police
        page: Page PyMuPDF pour les métriques
        
    Returns:
        tuple: (x, y) position optimale pour insert_text
    """
    # Obtenir les métriques précises
    metrics = _get_precise_text_metrics(page, text, fontname, fontsize)
    
    # Position x: centrée horizontalement dans la boîte si possible
    available_width = bbox.width
    text_width = metrics['width']
    
    if text_width <= available_width:
        # Centrer le texte horizontalement
        x = bbox.x0 + (available_width - text_width) / 2
    else:
        # Aligner à gauche si trop large
        x = bbox.x0
    
    # Position y: calculer la ligne de base précise
    # La ligne de base est à une distance de l'ascender depuis le haut
    bbox_height = bbox.height
    text_height = metrics['height']
    ascender = metrics['ascender']
    
    # Centrer verticalement puis ajuster pour la ligne de base
    y_center = bbox.y0 + bbox_height / 2
    y = y_center + ascender / 2
    
    # S'assurer que le texte reste dans les limites
    if y > bbox.y1:
        y = bbox.y1 - metrics['descender']
    elif y < bbox.y0 + ascender:
        y = bbox.y0 + ascender
    
    return (x, y)


def _adjust_font_size_precise(text, bbox, original_font_size, fontname, page):
    """
    Ajuste la taille de la police de manière précise en utilisant les métriques réelles.
    
    Args:
        text: Texte à insérer
        bbox: Rectangle englobant disponible
        original_font_size: Taille de police originale
        fontname: Nom de la police
        page: Page PyMuPDF pour les métriques
        
    Returns:
        float: Taille de police ajustée
    """
    # Obtenir les métriques avec la taille originale
    metrics = _get_precise_text_metrics(page, text, fontname, original_font_size)
    
    available_width = bbox.width
    available_height = bbox.height
    
    # Calculer les facteurs d'ajustement
    width_scale = 1.0
    height_scale = 1.0
    
    if metrics['width'] > available_width:
        width_scale = available_width / metrics['width']
    
    if metrics['height'] > available_height:
        height_scale = available_height / metrics['height']
    
    # Utiliser le facteur le plus restrictif
    scale_factor = min(width_scale, height_scale)
    
    if scale_factor < 1.0:
        adjusted_size = original_font_size * scale_factor
        # Ne pas descendre en dessous de 6pt
        return max(adjusted_size, 6.0)
    
    return original_font_size


def _anonymize_text_block_ultra_precise(page, block, mapping: Dict[str, str]):
    """
    Anonymise un bloc de texte avec un positionnement ultra-précis utilisant les métriques réelles.
    Le mapping contient: {valeur_originale: balise_anonymisée}
    """
    import fitz
    
    for line in block["lines"]:
        for span in line["spans"]:
            original_text = span["text"]
            
            if not original_text.strip():
                continue
                
            # Appliquer les remplacements du mapping
            anonymized_text = original_text
            text_changed = False
            
            # Le mapping contient {valeur_originale: balise_anonymisée}
            # Trier les clés par longueur décroissante pour éviter les remplacements partiels
            sorted_items = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
            
            for original_value, anonymized_tag in sorted_items:
                if original_value in anonymized_text:
                    anonymized_text = anonymized_text.replace(original_value, anonymized_tag)
                    text_changed = True
                    logging.debug(f"🔄 Remplacement: '{original_value}' → '{anonymized_tag}'")
            
            # Si le texte a changé, le remplacer dans le PDF
            if text_changed and anonymized_text != original_text:
                # Obtenir les propriétés du texte original
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                
                # Ajuster la taille de la police avec précision
                adjusted_font_size = _adjust_font_size_precise(
                    anonymized_text, bbox, font_size, font_name, page
                )
                
                # Calculer la position ultra-précise
                text_position = _calculate_precise_text_position(
                    bbox, anonymized_text, font_name, adjusted_font_size, page
                )
                
                # Effacer l'ancien texte avec un rectangle légèrement plus grand
                padding = 1  # 1 point de padding
                expanded_bbox = fitz.Rect(
                    bbox.x0 - padding, bbox.y0 - padding,
                    bbox.x1 + padding, bbox.y1 + padding
                )
                page.draw_rect(expanded_bbox, color=None, fill=fitz.pdfcolor["white"])
                
                # Insérer le nouveau texte anonymisé avec positionnement ultra-précis
                try:
                    page.insert_text(
                        text_position,
                        anonymized_text,
                        fontname=font_name,
                        fontsize=adjusted_font_size,
                        color=text_color
                    )
                    logging.debug(f"✅ Texte remplacé avec positionnement ultra-précis: '{original_text}' → '{anonymized_text}' (taille: {adjusted_font_size:.1f})")
                except Exception as e:
                    logging.warning(f"⚠️ Erreur remplacement texte: {str(e)}")
                    # Fallback avec police par défaut
                    try:
                        fallback_position = _calculate_precise_text_position(
                            bbox, anonymized_text, "helv", adjusted_font_size, page
                        )
                        page.insert_text(
                            fallback_position,
                            anonymized_text,
                            fontname="helv",
                            fontsize=adjusted_font_size,
                            color=text_color
                        )
                        logging.debug(f"✅ Texte remplacé avec police par défaut et positionnement ultra-précis")
                    except Exception as e2:
                        logging.error(f"❌ Impossible de remplacer le texte: {str(e2)}")


def _deanonymize_text_block_ultra_precise(page, block, mapping: Dict[str, str]):
    """
    Dé-anonymise un bloc de texte avec un positionnement ultra-précis utilisant les métriques réelles.
    """
    import fitz
    
    for line in block["lines"]:
        for span in line["spans"]:
            original_text = span["text"]
            
            if not original_text.strip():
                continue
                
            # Appliquer les remplacements du mapping (balise → valeur originale)
            deanonymized_text = original_text
            text_changed = False
            
            # Trier les clés par longueur décroissante pour éviter les remplacements partiels
            sorted_keys = sorted(mapping.keys(), key=len, reverse=True)
            
            for anonymized_tag, original_value in mapping.items():
                if anonymized_tag in deanonymized_text:
                    deanonymized_text = deanonymized_text.replace(anonymized_tag, original_value)
                    text_changed = True
                    logging.debug(f"🔄 Dé-anonymisation: '{anonymized_tag}' → '{original_value}'")
            
            # Si le texte a changé, le remplacer dans le PDF
            if text_changed and deanonymized_text != original_text:
                # Obtenir les propriétés du texte original
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                
                # Ajuster la taille de la police avec précision
                adjusted_font_size = _adjust_font_size_precise(
                    deanonymized_text, bbox, font_size, font_name, page
                )
                
                # Calculer la position ultra-précise
                text_position = _calculate_precise_text_position(
                    bbox, deanonymized_text, font_name, adjusted_font_size, page
                )
                
                # Effacer l'ancien texte avec un rectangle légèrement plus grand
                padding = 1  # 1 point de padding
                expanded_bbox = fitz.Rect(
                    bbox.x0 - padding, bbox.y0 - padding,
                    bbox.x1 + padding, bbox.y1 + padding
                )
                page.draw_rect(expanded_bbox, color=None, fill=fitz.pdfcolor["white"])
                
                # Insérer le nouveau texte dé-anonymisé avec positionnement ultra-précis
                try:
                    page.insert_text(
                        text_position,
                        deanonymized_text,
                        fontname=font_name,
                        fontsize=adjusted_font_size,
                        color=text_color
                    )
                    logging.debug(f"✅ Texte dé-anonymisé avec positionnement ultra-précis: '{original_text}' → '{deanonymized_text}' (taille: {adjusted_font_size:.1f})")
                except Exception as e:
                    logging.warning(f"⚠️ Erreur dé-anonymisation texte: {str(e)}")
                    # Fallback avec police par défaut
                    try:
                        fallback_position = _calculate_precise_text_position(
                            bbox, deanonymized_text, "helv", adjusted_font_size, page
                        )
                        page.insert_text(
                            fallback_position,
                            deanonymized_text,
                            fontname="helv",
                            fontsize=adjusted_font_size,
                            color=text_color
                        )
                        logging.debug(f"✅ Texte dé-anonymisé avec police par défaut et positionnement ultra-précis")
                    except Exception as e2:
                        logging.error(f"❌ Impossible de dé-anonymiser le texte: {str(e2)}")


def _preserve_original_text_alignment(bbox, original_text, new_text, fontname, fontsize, page):
    """
    Calcule la position exacte pour préserver l'alignement original du texte.
    
    Args:
        bbox: Rectangle englobant du texte original
        original_text: Texte original
        new_text: Nouveau texte à insérer
        fontname: Nom de la police
        fontsize: Taille de la police
        page: Page PyMuPDF
        
    Returns:
        tuple: (x, y) position exacte pour préserver l'alignement
    """
    # Position x: utiliser exactement la position originale (pas de centrage)
    x = bbox.x0
    
    # Position y: calculer la ligne de base correctement pour éviter les coupures
    # La ligne de base doit être calculée en tenant compte des descenders
    # Utiliser une approche plus précise basée sur les métriques de la police
    
    # Estimation de la hauteur de la ligne de base (généralement 75-80% de la hauteur)
    baseline_ratio = 0.75
    y = bbox.y0 + (bbox.height * baseline_ratio)
    
    # Ajustement pour éviter les coupures de descenders (g, j, p, q, y)
    # Vérifier si le nouveau texte contient des descenders
    has_descenders = any(char in new_text for char in 'gjpqy')
    if has_descenders:
        # Ajuster légèrement vers le haut pour éviter les coupures
        y = y - (fontsize * 0.1)  # Ajustement de 10% de la taille de police
        logging.debug(f"🔧 Ajustement descenders pour '{new_text}': y = {y:.2f} (ajusté de -{fontsize * 0.1:.2f})")
    
    logging.debug(f"📍 Position calculée pour '{new_text}': x={x:.2f}, y={y:.2f} (bbox: {bbox}, ratio: {baseline_ratio})")
    
    return (x, y)


def _get_best_matching_font(original_fontname, page):
    """
    Trouve la meilleure police disponible qui correspond à la police originale.
    
    Args:
        original_fontname: Nom de la police originale
        page: Page PyMuPDF
        
    Returns:
        str: Nom de la police à utiliser
    """
    import fitz
    
    # Nettoyer le nom de la police original
    clean_fontname = original_fontname.lower().replace("-", "").replace(" ", "")
    
    # Mapping des polices communes
    font_mapping = {
        "helvetica": "helv",
        "arial": "helv", 
        "times": "times",
        "timesnewroman": "times",
        "courier": "cour",
        "couriernew": "cour",
        "calibri": "helv",
        "verdana": "helv",
        "georgia": "times",
        "trebuchet": "helv",
        "lucida": "helv",
        "palatino": "times",
        "garamond": "times",
        "bookman": "times",
        "avantgarde": "helv",
        "zapfdingbats": "zadb",
        "symbol": "symb"
    }
    
    # Chercher une correspondance directe
    for pattern, mapped_font in font_mapping.items():
        if pattern in clean_fontname:
            return mapped_font
    
    # Fallback intelligent basé sur les caractéristiques de la police
    if "bold" in clean_fontname or "black" in clean_fontname:
        return "helv"  # Helvetica pour le gras
    elif "italic" in clean_fontname or "oblique" in clean_fontname:
        return "helv"  # Helvetica pour l'italique
    elif "mono" in clean_fontname or "fixed" in clean_fontname:
        return "cour"  # Courier pour les polices monospace
    elif "serif" in clean_fontname or "roman" in clean_fontname:
        return "times"  # Times pour les polices serif
    else:
        return "helv"  # Helvetica par défaut


def _anonymize_text_block_perfect_alignment(page, block, mapping: Dict[str, str]):
    """
    Anonymise un bloc de texte en préservant parfaitement l'alignement et les polices originales.
    Le mapping contient: {valeur_originale: balise_anonymisée}
    """
    import fitz
    
    for line in block["lines"]:
        # Traiter tous les spans d'une ligne ensemble pour maintenir l'alignement
        line_spans = []
        
        for span in line["spans"]:
            original_text = span["text"]
            
            if not original_text.strip():
                continue
                
            # Appliquer les remplacements du mapping avec remplacement sécurisé
            anonymized_text, text_changed = _safe_replace_in_span_text(original_text, mapping)
            
            # Ajouter ce span à la liste des spans de la ligne
            line_spans.append({
                'span': span,
                'original_text': original_text,
                'anonymized_text': anonymized_text,
                'text_changed': text_changed
            })
        
        # Traiter tous les spans modifiés de la ligne
        for span_info in line_spans:
            if span_info['text_changed'] and span_info['anonymized_text'] != span_info['original_text']:
                span = span_info['span']
                original_text = span_info['original_text']
                anonymized_text = span_info['anonymized_text']
                
                # Obtenir les propriétés du texte original
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]  # Important pour le formatage
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                
                # Vérifier et ajuster les marges droites
                page_rect = page.rect
                if bbox.x1 > page_rect.x1 - 50:  # Marge droite de 50 points
                    logging.warning(f"⚠️ Texte trop proche du bord droit: {bbox.x1} > {page_rect.x1 - 50}")
                    # Ajuster la largeur disponible
                    available_width = page_rect.x1 - bbox.x0 - 50
                    if available_width < 100:  # Minimum 100 points
                        available_width = 100
                    bbox = fitz.Rect(bbox.x0, bbox.y0, bbox.x0 + available_width, bbox.y1)
                
                # Calculer la position exacte pour préserver l'alignement
                text_position = _preserve_original_text_alignment(
                    bbox, original_text, anonymized_text, font_name, font_size, page
                )
                
                # Effacer l'ancien texte avec un rectangle exact (sans padding excessif)
                try:
                    page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                except Exception as e:
                    logging.warning(f"⚠️ Erreur effacement rectangle: {str(e)}")
                
                # Insérer le nouveau texte anonymisé avec formatage préservé
                success = False
                
                # Tentative 1: Utiliser la police originale exacte
                try:
                    # Normaliser la couleur pour PyMuPDF
                    normalized_color = _normalize_color(text_color)
                    
                    page.insert_text(
                        text_position,
                        anonymized_text,
                        fontname=font_name,  # Police originale exacte
                        fontsize=font_size,
                        color=normalized_color
                    )
                    success = True
                    logging.debug(f"✅ Texte remplacé avec police originale: '{original_text}' → '{anonymized_text}' (police: {font_name})")
                except Exception as e:
                    logging.debug(f"⚠️ Police originale échouée: {str(e)}")
                
                # Tentative 2: Utiliser une police de base avec formatage
                if not success:
                    try:
                        # Trouver la meilleure police correspondante
                        best_font = _get_best_matching_font(font_name, page)
                        
                        # Appliquer le formatage si possible
                        formatted_font = _apply_font_formatting_safe(best_font, font_flags)
                        
                        normalized_color = _normalize_color(text_color)
                        
                        page.insert_text(
                            text_position,
                            anonymized_text,
                            fontname=formatted_font,
                            fontsize=font_size,
                            color=normalized_color
                        )
                        success = True
                        logging.debug(f"✅ Texte remplacé avec police formatée: '{original_text}' → '{anonymized_text}' (police: {formatted_font})")
                    except Exception as e:
                        logging.debug(f"⚠️ Police formatée échouée: {str(e)}")
                
                # Tentative 3: Fallback avec police de base
                if not success:
                    try:
                        best_font = _get_best_matching_font(font_name, page)
                        normalized_color = _normalize_color(text_color)
                        
                        page.insert_text(
                            text_position,
                            anonymized_text,
                            fontname=best_font,
                            fontsize=font_size,
                            color=normalized_color
                        )
                        success = True
                        logging.debug(f"✅ Texte remplacé avec police de base: '{original_text}' → '{anonymized_text}' (police: {best_font})")
                    except Exception as e:
                        logging.debug(f"⚠️ Police de base échouée: {str(e)}")
                
                # Tentative 4: Dernier fallback avec Helvetica
                if not success:
                    try:
                        normalized_color = _normalize_color(text_color)
                        
                        page.insert_text(
                            text_position,
                            anonymized_text,
                            fontname="helv",
                            fontsize=font_size,
                            color=normalized_color
                        )
                        success = True
                        logging.debug(f"✅ Texte remplacé avec Helvetica: '{original_text}' → '{anonymized_text}'")
                    except Exception as e:
                        logging.error(f"❌ Impossible de remplacer le texte: {str(e)}")


def _apply_font_formatting_safe(base_font: str, font_flags: int) -> str:
    """
    Applique le formatage (gras, italique) à une police de base de manière sécurisée.
    Retourne la police de base si le formatage n'est pas disponible.
    
    Args:
        base_font: Police de base (helv, times, cour)
        font_flags: Flags de formatage PyMuPDF
        
    Returns:
        str: Nom de police avec formatage appliqué ou police de base
    """
    import fitz
    
    # Constantes PyMuPDF pour les flags
    BOLD_FLAG = 2**4   # 16
    ITALIC_FLAG = 2**5  # 32
    
    # Détecter le formatage
    is_bold = bool(font_flags & BOLD_FLAG)
    is_italic = bool(font_flags & ITALIC_FLAG)
    
    logging.debug(f"🎨 Formatage détecté: flags={font_flags}, bold={is_bold}, italic={is_italic}")
    
    # Si pas de formatage, retourner la police de base
    if not is_bold and not is_italic:
        return base_font
    
    # Essayer d'appliquer le formatage
    try:
        # Appliquer le formatage selon la police de base
        if base_font == "helv":
            if is_bold and is_italic:
                result = "helv-bolditalic"
            elif is_bold:
                result = "helv-bold"
            elif is_italic:
                result = "helv-italic"
            else:
                result = "helv"
        elif base_font == "times":
            if is_bold and is_italic:
                result = "times-bolditalic"
            elif is_bold:
                result = "times-bold"
            elif is_italic:
                result = "times-italic"
            else:
                result = "times"
        elif base_font == "cour":
            if is_bold and is_italic:
                result = "cour-bolditalic"
            elif is_bold:
                result = "cour-bold"
            elif is_italic:
                result = "cour-italic"
            else:
                result = "cour"
        else:
            # Pour les autres polices, utiliser Helvetica avec formatage
            if is_bold and is_italic:
                result = "helv-bolditalic"
            elif is_bold:
                result = "helv-bold"
            elif is_italic:
                result = "helv-italic"
            else:
                result = "helv"
        
        # Tester si la police formatée est disponible
        try:
            fitz.Font(result)
            logging.debug(f"🎨 Police formatée disponible: '{base_font}' → '{result}'")
            return result
        except:
            logging.debug(f"⚠️ Police formatée non disponible: '{result}', utilisation de '{base_font}'")
            return base_font
            
    except Exception as e:
        logging.debug(f"⚠️ Erreur formatage police: {str(e)}, utilisation de '{base_font}'")
        return base_font


def _deanonymize_text_block_perfect_alignment(page, block, mapping: Dict[str, str]):
    """
    Dé-anonymise un bloc de texte en préservant parfaitement l'alignement et les polices originales.
    """
    import fitz
    
    for line in block["lines"]:
        # Traiter tous les spans d'une ligne ensemble pour maintenir l'alignement
        line_spans = []
        
        for span in line["spans"]:
            original_text = span["text"]
            
            if not original_text.strip():
                continue
                
            # Appliquer les remplacements du mapping avec remplacement sécurisé (balise → valeur originale)
            deanonymized_text, text_changed = _safe_replace_in_span_text(original_text, mapping)
            
            # Ajouter ce span à la liste des spans de la ligne
            line_spans.append({
                'span': span,
                'original_text': original_text,
                'deanonymized_text': deanonymized_text,
                'text_changed': text_changed
            })
        
        # Traiter tous les spans modifiés de la ligne
        for span_info in line_spans:
            if span_info['text_changed'] and span_info['deanonymized_text'] != span_info['original_text']:
                span = span_info['span']
                original_text = span_info['original_text']
                deanonymized_text = span_info['deanonymized_text']
                
                # Obtenir les propriétés du texte original
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]  # Important pour le formatage
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                
                # Vérifier et ajuster les marges droites
                page_rect = page.rect
                if bbox.x1 > page_rect.x1 - 50:  # Marge droite de 50 points
                    logging.warning(f"⚠️ Texte trop proche du bord droit: {bbox.x1} > {page_rect.x1 - 50}")
                    # Ajuster la largeur disponible
                    available_width = page_rect.x1 - bbox.x0 - 50
                    if available_width < 100:  # Minimum 100 points
                        available_width = 100
                    bbox = fitz.Rect(bbox.x0, bbox.y0, bbox.x0 + available_width, bbox.y1)
                
                # Calculer la position exacte pour préserver l'alignement
                text_position = _preserve_original_text_alignment(
                    bbox, original_text, deanonymized_text, font_name, font_size, page
                )
                
                # Effacer l'ancien texte avec un rectangle exact (sans padding excessif)
                try:
                    page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                except Exception as e:
                    logging.warning(f"⚠️ Erreur effacement rectangle: {str(e)}")
                
                # Insérer le nouveau texte dé-anonymisé avec formatage préservé
                success = False
                
                # Tentative 1: Utiliser la police originale exacte
                try:
                    # Normaliser la couleur pour PyMuPDF
                    normalized_color = _normalize_color(text_color)
                    
                    page.insert_text(
                        text_position,
                        deanonymized_text,
                        fontname=font_name,  # Police originale exacte
                        fontsize=font_size,
                        color=normalized_color
                    )
                    success = True
                    logging.debug(f"✅ Texte dé-anonymisé avec police originale: '{original_text}' → '{deanonymized_text}' (police: {font_name})")
                except Exception as e:
                    logging.debug(f"⚠️ Police originale échouée: {str(e)}")
                
                # Tentative 2: Utiliser une police de base avec formatage
                if not success:
                    try:
                        # Trouver la meilleure police correspondante
                        best_font = _get_best_matching_font(font_name, page)
                        
                        # Appliquer le formatage si possible
                        formatted_font = _apply_font_formatting_safe(best_font, font_flags)
                        
                        normalized_color = _normalize_color(text_color)
                        
                        page.insert_text(
                            text_position,
                            deanonymized_text,
                            fontname=formatted_font,
                            fontsize=font_size,
                            color=normalized_color
                        )
                        success = True
                        logging.debug(f"✅ Texte dé-anonymisé avec police formatée: '{original_text}' → '{deanonymized_text}' (police: {formatted_font})")
                    except Exception as e:
                        logging.debug(f"⚠️ Police formatée échouée: {str(e)}")
                
                # Tentative 3: Fallback avec police de base
                if not success:
                    try:
                        best_font = _get_best_matching_font(font_name, page)
                        normalized_color = _normalize_color(text_color)
                        
                        page.insert_text(
                            text_position,
                            deanonymized_text,
                            fontname=best_font,
                            fontsize=font_size,
                            color=normalized_color
                        )
                        success = True
                        logging.debug(f"✅ Texte dé-anonymisé avec police de base: '{original_text}' → '{deanonymized_text}' (police: {best_font})")
                    except Exception as e:
                        logging.debug(f"⚠️ Police de base échouée: {str(e)}")
                
                # Tentative 4: Dernier fallback avec Helvetica
                if not success:
                    try:
                        normalized_color = _normalize_color(text_color)
                        
                        page.insert_text(
                            text_position,
                            deanonymized_text,
                            fontname="helv",
                            fontsize=font_size,
                            color=normalized_color
                        )
                        success = True
                        logging.debug(f"✅ Texte dé-anonymisé avec Helvetica: '{original_text}' → '{deanonymized_text}'")
                    except Exception as e:
                        logging.error(f"❌ Impossible de dé-anonymiser le texte: {str(e)}")


# ===== FIN ANONYMISATION DIRECTE PDF =====

def _safe_replace_with_word_boundaries(text: str, old_value: str, new_value: str) -> str:
    """
    Remplace une valeur dans le texte de manière agressive pour l'anonymisation.
    
    Args:
        text: Texte dans lequel effectuer le remplacement
        old_value: Valeur à remplacer
        new_value: Nouvelle valeur
        
    Returns:
        str: Texte avec les remplacements effectués
    """
    # Échapper les caractères spéciaux pour les expressions régulières
    escaped_old = re.escape(old_value)
    
    # CORRECTION: Utiliser un pattern plus agressif pour l'anonymisation
    # Pattern 1: Avec limites de mots (pour les mots entiers)
    pattern1 = r'\b' + escaped_old + r'\b'
    result = re.sub(pattern1, new_value, text, flags=re.IGNORECASE)
    
    # Pattern 2: Sans limites de mots (pour capturer les cas manqués)
    # Utiliser des espaces ou ponctuation autour
    pattern2 = r'(\s|^)' + escaped_old + r'(\s|$|[.,;:!?])'
    result = re.sub(pattern2, r'\1' + new_value + r'\2', result, flags=re.IGNORECASE)
    
    # Pattern 3: Remplacement direct pour les cas restants
    # Utiliser une recherche simple mais avec vérification de contexte
    if old_value.lower() in result.lower():
        # Remplacer toutes les occurrences restantes
        result = result.replace(old_value, new_value)
        result = result.replace(old_value.upper(), new_value.upper())
        result = result.replace(old_value.lower(), new_value.lower())
        result = result.replace(old_value.title(), new_value.title())
    
    return result


def _safe_replace_in_span_text(span_text: str, mapping: Dict[str, str]) -> Tuple[str, bool]:
    """
    Remplace les valeurs dans un span de texte en utilisant des limites de mots.
    
    Args:
        span_text: Texte du span
        mapping: Mapping des remplacements {old_value: new_value}
        
    Returns:
        Tuple[str, bool]: (texte_modifié, changement_effectué)
    """
    modified_text = span_text
    text_changed = False
    
    # Trier les clés par longueur décroissante pour éviter les remplacements partiels
    sorted_items = sorted(mapping.items(), key=lambda x: len(x[0]), reverse=True)
    
    for old_value, new_value in sorted_items:
        # Utiliser le remplacement sécurisé avec limites de mots
        before_replace = modified_text
        modified_text = _safe_replace_with_word_boundaries(modified_text, old_value, new_value)
        
        if modified_text != before_replace:
            text_changed = True
            logging.debug(f"🔄 Remplacement sécurisé: '{old_value}' → '{new_value}'")
    
    return modified_text, text_changed


def _normalize_color(color_value):
    """
    Normalise une valeur de couleur pour PyMuPDF.
    
    Args:
        color_value: Valeur de couleur (peut être int, float, tuple, etc.)
        
    Returns:
        tuple: Couleur normalisée (R, G, B) avec des valeurs entre 0 et 1
    """
    if color_value is None:
        return (0, 0, 0)  # Noir par défaut
    
    # Si c'est déjà un tuple/liste de 3 valeurs
    if isinstance(color_value, (tuple, list)) and len(color_value) == 3:
        return tuple(float(c) for c in color_value)
    
    # Si c'est un entier (couleur RGB encodée)
    if isinstance(color_value, int):
        # Convertir l'entier en RGB
        r = ((color_value >> 16) & 0xFF) / 255.0
        g = ((color_value >> 8) & 0xFF) / 255.0
        b = (color_value & 0xFF) / 255.0
        return (r, g, b)
    
    # Si c'est un float (niveau de gris)
    if isinstance(color_value, float):
        if 0 <= color_value <= 1:
            return (color_value, color_value, color_value)
        else:
            # Normaliser si > 1
            normalized = color_value / 255.0 if color_value > 1 else color_value
            return (normalized, normalized, normalized)
    
    # Fallback: noir avec log détaillé
    logging.debug(f"🎨 Couleur non reconnue: {color_value} (type: {type(color_value)}), utilisation du noir")
    return (0, 0, 0)


def _apply_font_formatting_safe(base_font: str, font_flags: int) -> str:
    """
    Applique le formatage (gras, italique) à une police de base de manière sécurisée.
    Retourne la police de base si le formatage n'est pas disponible.
    
    Args:
        base_font: Police de base (helv, times, cour)
        font_flags: Flags de formatage PyMuPDF
        
    Returns:
        str: Nom de police avec formatage appliqué ou police de base
    """
    import fitz
    
    # Constantes PyMuPDF pour les flags
    BOLD_FLAG = 2**4   # 16
    ITALIC_FLAG = 2**5  # 32
    
    # Détecter le formatage
    is_bold = bool(font_flags & BOLD_FLAG)
    is_italic = bool(font_flags & ITALIC_FLAG)
    
    logging.debug(f"🎨 Formatage détecté: flags={font_flags}, bold={is_bold}, italic={is_italic}")
    
    # Si pas de formatage, retourner la police de base
    if not is_bold and not is_italic:
        return base_font
    
    # Essayer d'appliquer le formatage
    try:
        # Appliquer le formatage selon la police de base
        if base_font == "helv":
            if is_bold and is_italic:
                result = "helv-bolditalic"
            elif is_bold:
                result = "helv-bold"
            elif is_italic:
                result = "helv-italic"
            else:
                result = "helv"
        elif base_font == "times":
            if is_bold and is_italic:
                result = "times-bolditalic"
            elif is_bold:
                result = "times-bold"
            elif is_italic:
                result = "times-italic"
            else:
                result = "times"
        elif base_font == "cour":
            if is_bold and is_italic:
                result = "cour-bolditalic"
            elif is_bold:
                result = "cour-bold"
            elif is_italic:
                result = "cour-italic"
            else:
                result = "cour"
        else:
            # Pour les autres polices, utiliser Helvetica avec formatage
            if is_bold and is_italic:
                result = "helv-bolditalic"
            elif is_bold:
                result = "helv-bold"
            elif is_italic:
                result = "helv-italic"
            else:
                result = "helv"
        
        # Tester si la police formatée est disponible
        try:
            fitz.Font(result)
            logging.debug(f"🎨 Police formatée disponible: '{base_font}' → '{result}'")
            return result
        except:
            logging.debug(f"⚠️ Police formatée non disponible: '{result}', utilisation de '{base_font}'")
            return base_font
            
    except Exception as e:
        logging.debug(f"⚠️ Erreur formatage police: {str(e)}, utilisation de '{base_font}'")
        return base_font


def _anonymize_text_block_comprehensive(page, block, mapping: Dict[str, str]):
    """
    Anonymise un bloc de texte avec gestion complète des problèmes:
    - Marge droite respectée avec ajustement automatique
    - Formatage gras/couleur préservé
    - Gestion robuste des erreurs MuPDF
    Le mapping contient: {valeur_originale: balise_anonymisée}
    Ajout : logs détaillés pour chaque remplacement.
    """
    import fitz
    for line in block["lines"]:
        # Traiter tous les spans d'une ligne ensemble pour maintenir l'alignement
        line_spans = []
        for span in line["spans"]:
            original_text = span["text"]
            if not original_text.strip():
                continue
            # Appliquer les remplacements du mapping avec remplacement sécurisé
            anonymized_text, text_changed = _safe_replace_in_span_text(original_text, mapping)
            # Ajouter ce span à la liste des spans de la ligne
            line_spans.append({
                'span': span,
                'original_text': original_text,
                'anonymized_text': anonymized_text,
                'text_changed': text_changed
            })
        # Traiter tous les spans modifiés de la ligne
        for span_info in line_spans:
            if span_info['text_changed'] and span_info['anonymized_text'] != span_info['original_text']:
                span = span_info['span']
                original_text = span_info['original_text']
                anonymized_text = span_info['anonymized_text']
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                # LOG DÉTAILLÉ
                logging.info(f"🔄 Remplacement PDF: '{original_text}' → '{anonymized_text}' | Page: {page.number+1} | BBox: {bbox} | Police: {font_name} | Taille: {font_size} | Flags: {font_flags} | Couleur: {text_color}")
                # CORRECTION 1: Vérifier et ajuster les marges droites de manière robuste
                page_rect = page.rect
                margin_right = 50  # Marge droite de 50 points
                
                if bbox.x1 > page_rect.x1 - margin_right:
                    logging.warning(f"⚠️ Texte trop proche du bord droit: {bbox.x1} > {page_rect.x1 - margin_right}")
                    logging.info(f"📏 Texte original: '{original_text}' → Texte anonymisé: '{anonymized_text}'")
                    
                    # Ajuster la largeur disponible
                    available_width = page_rect.x1 - bbox.x0 - margin_right
                    if available_width < 100:  # Minimum 100 points
                        available_width = 100
                        logging.warning(f"⚠️ Largeur disponible très réduite: {available_width} points")
                    
                    # Créer un nouveau bbox avec la largeur ajustée
                    original_bbox = bbox
                    bbox = fitz.Rect(bbox.x0, bbox.y0, bbox.x0 + available_width, bbox.y1)
                    logging.info(f"📏 Bbox ajusté pour marge droite: {original_bbox} → {bbox}")
                    
                    # Vérifier si le texte anonymisé est plus long que l'original
                    if len(anonymized_text) > len(original_text):
                        logging.warning(f"⚠️ Texte anonymisé plus long que l'original: {len(anonymized_text)} > {len(original_text)}")
                        # Ajuster la taille de police si nécessaire
                        font_size = font_size * 0.9  # Réduire de 10%
                        logging.info(f"📏 Taille de police ajustée: {font_size:.1f}")
                
                # Calculer la position exacte pour préserver l'alignement
                text_position = _preserve_original_text_alignment(
                    bbox, original_text, anonymized_text, font_name, font_size, page
                )
                
                # Effacer l'ancien texte avec gestion d'erreur robuste
                try:
                    page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                except Exception as e:
                    logging.warning(f"⚠️ Erreur effacement rectangle: {str(e)}")
                    # Essayer avec un rectangle légèrement plus petit
                    try:
                        smaller_bbox = fitz.Rect(bbox.x0 + 1, bbox.y0 + 1, bbox.x1 - 1, bbox.y1 - 1)
                        page.draw_rect(smaller_bbox, color=None, fill=fitz.pdfcolor["white"])
                    except Exception as e2:
                        logging.warning(f"⚠️ Impossible d'effacer le rectangle: {str(e2)}")
                
                # CORRECTION 2: Insérer le nouveau texte avec formatage préservé dès l'anonymisation
                success = _insert_text_with_preserved_formatting(
                    page, text_position, anonymized_text, font_name, font_size, font_flags, text_color, original_text
                )
                
                if not success:
                    logging.error(f"❌ Impossible de remplacer le texte: '{original_text}' → '{anonymized_text}'")


def _deanonymize_text_block_comprehensive(page, block, mapping: Dict[str, str]):
    """
    Dé-anonymise un bloc de texte avec gestion complète des problèmes:
    - Marge droite respectée avec ajustement automatique
    - Formatage gras/couleur préservé et restauré
    - Gestion robuste des erreurs MuPDF
    Le mapping contient: {balise_anonymisée: valeur_originale}
    """
    import fitz
    
    for line in block["lines"]:
        # Traiter tous les spans d'une ligne ensemble pour maintenir l'alignement
        line_spans = []
        
        for span in line["spans"]:
            original_text = span["text"]
            
            if not original_text.strip():
                continue
                
            # Appliquer les remplacements du mapping avec remplacement sécurisé
            deanonymized_text, text_changed = _safe_replace_in_span_text(original_text, mapping)
            
            # Ajouter ce span à la liste des spans de la ligne
            line_spans.append({
                'span': span,
                'original_text': original_text,
                'deanonymized_text': deanonymized_text,
                'text_changed': text_changed
            })
        
        # Traiter tous les spans modifiés de la ligne
        for span_info in line_spans:
            if span_info['text_changed'] and span_info['deanonymized_text'] != span_info['original_text']:
                span = span_info['span']
                original_text = span_info['original_text']
                deanonymized_text = span_info['deanonymized_text']
                
                # Obtenir les propriétés du texte original
                font_name = span["font"]
                font_size = span["size"]
                font_flags = span["flags"]  # Important pour le formatage
                text_color = span["color"]
                bbox = fitz.Rect(span["bbox"])
                
                # CORRECTION 1: Vérifier et ajuster les marges droites de manière robuste
                page_rect = page.rect
                margin_right = 50  # Marge droite de 50 points
                
                if bbox.x1 > page_rect.x1 - margin_right:
                    logging.warning(f"⚠️ Texte trop proche du bord droit: {bbox.x1} > {page_rect.x1 - margin_right}")
                    # Ajuster la largeur disponible
                    available_width = page_rect.x1 - bbox.x0 - margin_right
                    if available_width < 100:  # Minimum 100 points
                        available_width = 100
                        logging.warning(f"⚠️ Largeur disponible très réduite: {available_width} points")
                    
                    # Créer un nouveau bbox avec la largeur ajustée
                    bbox = fitz.Rect(bbox.x0, bbox.y0, bbox.x0 + available_width, bbox.y1)
                    logging.info(f"📏 Bbox ajusté pour marge droite: {bbox}")
                
                # Calculer la position exacte pour préserver l'alignement
                text_position = _preserve_original_text_alignment(
                    bbox, original_text, deanonymized_text, font_name, font_size, page
                )
                
                # Effacer l'ancien texte avec gestion d'erreur robuste
                try:
                    page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                except Exception as e:
                    logging.warning(f"⚠️ Erreur effacement rectangle: {str(e)}")
                    # Essayer avec un rectangle légèrement plus petit
                    try:
                        smaller_bbox = fitz.Rect(bbox.x0 + 1, bbox.y0 + 1, bbox.x1 - 1, bbox.y1 - 1)
                        page.draw_rect(smaller_bbox, color=None, fill=fitz.pdfcolor["white"])
                    except Exception as e2:
                        logging.warning(f"⚠️ Impossible d'effacer le rectangle: {str(e2)}")
                
                # CORRECTION 2: Insérer le nouveau texte avec formatage préservé lors de la déanonymisation
                success = _insert_text_with_preserved_formatting(
                    page, text_position, deanonymized_text, font_name, font_size, font_flags, text_color, original_text
                )
                
                if not success:
                    logging.error(f"❌ Impossible de remplacer le texte: '{original_text}' → '{deanonymized_text}'")


def _insert_text_with_preserved_formatting(page, text_position, new_text, font_name, font_size, font_flags, text_color, original_text):
    """
    Insère du texte en préservant PRIORITAIREMENT la police originale, puis le formatage si possible.
    NOUVELLE STRATÉGIE: Police originale > Formatage gras/italique.
    
    Args:
        page: Page PyMuPDF
        text_position: Position (x, y) pour insérer le texte
        new_text: Nouveau texte à insérer
        font_name: Nom de la police originale
        font_size: Taille de la police
        font_flags: Flags de formatage (gras, italique)
        text_color: Couleur du texte original
        original_text: Texte original (pour le logging)
        
    Returns:
        bool: True si l'insertion a réussi, False sinon
    """
    import fitz
    
    # Normaliser la couleur pour PyMuPDF
    normalized_color = _normalize_color(text_color)
    
    # Détecter le formatage du texte original
    BOLD_FLAG = 2**4   # 16
    ITALIC_FLAG = 2**5  # 32
    is_bold = bool(font_flags & BOLD_FLAG)
    is_italic = bool(font_flags & ITALIC_FLAG)
    
    # Log détaillé du formatage détecté
    logging.info(f"🎨 NOUVELLE STRATÉGIE - Texte: '{original_text}' → '{new_text}'")
    logging.info(f"🎨 Police: {font_name}, Taille: {font_size}, Gras: {is_bold}, Italique: {is_italic}")
    logging.info(f"🎨 Couleur: {text_color} → {normalized_color}, Flags: {font_flags}")
    
    # PRIORITÉ 1: TOUJOURS essayer d'abord la police originale avec système de fallback intelligent
    if _try_original_font_with_fallback(page, text_position, new_text, font_name, font_size, font_flags, text_color, original_text):
        return True
    
    # PRIORITÉ 2: Si la police originale a totalement échoué, essayer de préserver le formatage gras/italique
    if is_bold or is_italic:
        logging.info(f"🎨 FALLBACK FORMATAGE - Police originale impossible, essai formatage gras/italique")
        
        try:
            # Utiliser l'équivalent PyMuPDF de la police
            equivalent_font = _get_pymupdf_font_equivalent(font_name)
            
            # FORCER l'application du formatage gras/italique
            if is_bold and is_italic:
                formatted_font = f"{equivalent_font}-boldoblique" if equivalent_font == "helv" else f"{equivalent_font}-bolditalic"
            elif is_bold:
                formatted_font = f"{equivalent_font}-bold"
            elif is_italic:
                formatted_font = f"{equivalent_font}-oblique" if equivalent_font == "helv" else f"{equivalent_font}-italic"
            else:
                formatted_font = equivalent_font
            
            logging.info(f"🎨 TENTATIVE FORMATAGE ÉQUIVALENT - Police: {font_name} → {equivalent_font} → {formatted_font}")
            
            page.insert_text(
                text_position,
                new_text,
                fontname=formatted_font,
                fontsize=font_size,
                color=normalized_color
            )
            logging.info(f"✅ FORMATAGE ÉQUIVALENT RÉUSSI - '{original_text}' → '{new_text}' (police: {formatted_font})")
            return True
        except Exception as e:
            logging.warning(f"⚠️ Police équivalente formatée échouée: {str(e)}")
        
        # PRIORITÉ 3: Forcer le gras avec les polices standards PyMuPDF
        if is_bold:
            try:
                # Essayer avec les polices standards PyMuPDF en gras
                standard_bold_fonts = ["helv-bold", "times-bold", "cour-bold"]
                
                for bold_font in standard_bold_fonts:
                    try:
                        page.insert_text(
                            text_position,
                            new_text,
                            fontname=bold_font,
                            fontsize=font_size,
                            color=normalized_color
                        )
                        logging.info(f"✅ FORMATAGE GRAS STANDARD - '{original_text}' → '{new_text}' (police: {bold_font})")
                        return True
                    except Exception as font_e:
                        logging.debug(f"⚠️ Police standard {bold_font} échouée: {str(font_e)}")
                        continue
                
            except Exception as e:
                logging.warning(f"⚠️ Toutes les polices standard gras ont échoué: {str(e)}")
    
    # PRIORITÉ 4: Au minimum préserver la couleur avec police équivalente
    try:
        equivalent_font = _get_pymupdf_font_equivalent(font_name)
        
        page.insert_text(
            text_position,
            new_text,
            fontname=equivalent_font,
            fontsize=font_size,
            color=normalized_color
        )
        logging.info(f"✅ COULEUR PRÉSERVÉE ÉQUIVALENTE - '{original_text}' → '{new_text}' (police: {font_name} → {equivalent_font}, couleur: {normalized_color})")
        return True
    except Exception as e:
        logging.warning(f"⚠️ Police équivalente échouée: {str(e)}")
    
    # Dernier recours: Helvetica avec couleur
    try:
        page.insert_text(
            text_position,
            new_text,
            fontname="helv",
            fontsize=font_size,
            color=normalized_color
        )
        logging.warning(f"⚠️ FALLBACK HELVETICA - Couleur préservée: '{original_text}' → '{new_text}' (couleur: {normalized_color})")
        return True
    except Exception as e:
        logging.error(f"❌ Dernier fallback échoué: {str(e)}")
    
    return False


def _apply_font_formatting_comprehensive(base_font: str, font_flags: int) -> str:
    """
    Applique le formatage (gras, italique) à une police de base de manière complète.
    Teste la disponibilité de chaque police avant de la retourner.
    
    Args:
        base_font: Police de base (helv, times, cour)
        font_flags: Flags de formatage PyMuPDF
        
    Returns:
        str: Nom de police avec formatage appliqué ou police de base
    """
    import fitz
    
    # Constantes PyMuPDF pour les flags
    BOLD_FLAG = 2**4   # 16
    ITALIC_FLAG = 2**5  # 32
    
    # Détecter le formatage
    is_bold = bool(font_flags & BOLD_FLAG)
    is_italic = bool(font_flags & ITALIC_FLAG)
    
    logging.debug(f"🎨 Formatage détecté: flags={font_flags}, bold={is_bold}, italic={is_italic}")
    
    # Si pas de formatage, retourner la police de base
    if not is_bold and not is_italic:
        return base_font
    
    # Mapping des polices avec formatage
    font_mapping = {
        "helv": {
            "bold": "helv-bold",
            "italic": "helv-oblique",
            "bold_italic": "helv-boldoblique"
        },
        "times": {
            "bold": "times-bold",
            "italic": "times-italic",
            "bold_italic": "times-bolditalic"
        },
        "cour": {
            "bold": "cour-bold",
            "italic": "cour-oblique",
            "bold_italic": "cour-boldoblique"
        }
    }
    
    # Déterminer la police formatée
    if base_font in font_mapping:
        font_variants = font_mapping[base_font]
        
        if is_bold and is_italic:
            formatted_font = font_variants.get("bold_italic", base_font)
        elif is_bold:
            formatted_font = font_variants.get("bold", base_font)
        elif is_italic:
            formatted_font = font_variants.get("italic", base_font)
        else:
            formatted_font = base_font
        
        logging.debug(f"🎨 Police formatée: {base_font} → {formatted_font}")
        return formatted_font
    
    # Si la police de base n'est pas reconnue, retourner telle quelle
    logging.debug(f"🎨 Police non reconnue, retour de la police de base: {base_font}")
    return base_font

# Dictionnaire des polices Microsoft Word les plus courantes avec leurs équivalents PyMuPDF
MICROSOFT_WORD_FONTS = {
    # Polices serif
    "times new roman": "times",
    "times-roman": "times",
    "timesnewroman": "times",
    "times": "times",
    "georgia": "times",  # Fallback vers Times
    "book antiqua": "times",
    "bookantiqua": "times",
    "garamond": "times",
    "palatino": "times",
    "palatino linotype": "times",
    "palatinolinotype": "times",
    
    # Polices sans-serif
    "arial": "helv",
    "helvetica": "helv",
    "calibri": "helv",  # Fallback vers Helvetica
    "verdana": "helv",
    "tahoma": "helv",
    "trebuchet ms": "helv",
    "trebuchetms": "helv",
    "franklin gothic medium": "helv",
    "franklingingothicmedium": "helv",
    "century gothic": "helv",
    "centurygothic": "helv",
    "lucida sans unicode": "helv",
    "lucidasansunicode": "helv",
    "ms sans serif": "helv",
    "mssansserif": "helv",
    "segoe ui": "helv",
    "segoeui": "helv",
    
    # Polices monospace
    "courier new": "cour",
    "courier": "cour",
    "couriernew": "cour",
    "consolas": "cour",
    "lucida console": "cour",
    "lucidaconsole": "cour",
    "monaco": "cour",
    "menlo": "cour",
    
    # Polices spéciales
    "comic sans ms": "helv",  # Fallback vers Helvetica
    "comicsansms": "helv",
    "impact": "helv",
    "papyrus": "helv",
    "brush script mt": "helv",
    "brushscriptmt": "helv",
    "chiller": "helv",
    "curlz mt": "helv",
    "curlzmt": "helv",
}

def _get_pymupdf_font_equivalent(font_name: str) -> str:
    """
    Trouve l'équivalent PyMuPDF d'une police Microsoft Word.
    
    Args:
        font_name: Nom de la police originale
        
    Returns:
        str: Nom de la police équivalente PyMuPDF (helv, times, cour)
    """
    if not font_name:
        return "helv"
    
    # Normaliser le nom de la police (minuscules, sans espaces)
    normalized_name = font_name.lower().replace(" ", "").replace("-", "")
    
    # Chercher dans le dictionnaire
    equivalent = MICROSOFT_WORD_FONTS.get(normalized_name)
    
    if equivalent:
        logging.debug(f"🔄 Police mappée: {font_name} → {equivalent}")
        return equivalent
    
    # Si pas trouvé, essayer de deviner par le nom
    if "times" in normalized_name or "roman" in normalized_name:
        logging.debug(f"🔄 Police devinée (serif): {font_name} → times")
        return "times"
    elif "courier" in normalized_name or "mono" in normalized_name or "console" in normalized_name:
        logging.debug(f"🔄 Police devinée (monospace): {font_name} → cour")
        return "cour"
    else:
        logging.debug(f"🔄 Police par défaut (sans-serif): {font_name} → helv")
        return "helv"

def _try_original_font_with_fallback(page, text_position, new_text, font_name, font_size, font_flags, text_color, original_text):
    """
    Essaie d'utiliser la police originale avec un système de fallback intelligent.
    
    Args:
        page: Page PyMuPDF
        text_position: Position (x, y) pour insérer le texte
        new_text: Nouveau texte à insérer
        font_name: Nom de la police originale
        font_size: Taille de la police
        font_flags: Flags de formatage (gras, italique)
        text_color: Couleur du texte original
        original_text: Texte original (pour le logging)
        
    Returns:
        bool: True si l'insertion a réussi, False sinon
    """
    import fitz
    
    # Normaliser la couleur pour PyMuPDF
    normalized_color = _normalize_color(text_color)
    
    # Détecter le formatage du texte original
    BOLD_FLAG = 2**4   # 16
    ITALIC_FLAG = 2**5  # 32
    is_bold = bool(font_flags & BOLD_FLAG)
    is_italic = bool(font_flags & ITALIC_FLAG)
    
    logging.info(f"🎨 TENTATIVE POLICE ORIGINALE - Texte: '{original_text}' → '{new_text}'")
    logging.info(f"🎨 Police: {font_name}, Taille: {font_size}, Gras: {is_bold}, Italique: {is_italic}")
    
    # ÉTAPE 1: Essayer la police originale exacte (priorité absolue)
    try:
        page.insert_text(
            text_position,
            new_text,
            fontname=font_name,
            fontsize=font_size,
            color=normalized_color
        )
        logging.info(f"✅ POLICE ORIGINALE EXACTE RÉUSSIE - '{original_text}' → '{new_text}' (police: {font_name})")
        return True
    except Exception as e:
        logging.debug(f"⚠️ Police originale exacte échouée: {str(e)}")
    
    # ÉTAPE 2: Si police originale échoue, essayer sans formatage (juste la police de base)
    try:
        # Retirer le formatage du nom de police (enlever -bold, -italic, etc.)
        base_font_name = font_name.replace("-bold", "").replace("-italic", "").replace("-oblique", "").replace("-bolditalic", "").replace("-boldoblique", "")
        
        page.insert_text(
            text_position,
            new_text,
            fontname=base_font_name,
            fontsize=font_size,
            color=normalized_color
        )
        logging.info(f"✅ POLICE ORIGINALE BASE RÉUSSIE - '{original_text}' → '{new_text}' (police: {base_font_name})")
        logging.warning(f"⚠️ FORMATAGE PERDU - Le gras/italique n'a pas pu être appliqué pour préserver la police originale")
        return True
    except Exception as e:
        logging.debug(f"⚠️ Police originale base échouée: {str(e)}")
    
    # ÉTAPE 3: Essayer l'équivalent PyMuPDF avec formatage préservé
    try:
        equivalent_font = _get_pymupdf_font_equivalent(font_name)
        
        # APPLIQUER LE FORMATAGE à la police équivalente
        if is_bold and is_italic:
            formatted_equivalent = f"{equivalent_font}-boldoblique" if equivalent_font == "helv" else f"{equivalent_font}-bolditalic"
        elif is_bold:
            formatted_equivalent = f"{equivalent_font}-bold"
        elif is_italic:
            formatted_equivalent = f"{equivalent_font}-oblique" if equivalent_font == "helv" else f"{equivalent_font}-italic"
        else:
            formatted_equivalent = equivalent_font
        
        logging.info(f"🎨 FORMATAGE ÉQUIVALENT - Police: {font_name} → {equivalent_font} → {formatted_equivalent}")
        
        page.insert_text(
            text_position,
            new_text,
            fontname=formatted_equivalent,
            fontsize=font_size,
            color=normalized_color
        )
        logging.info(f"✅ POLICE ÉQUIVALENTE + FORMATAGE RÉUSSI - '{original_text}' → '{new_text}' (police: {font_name} → {formatted_equivalent})")
        return True
    except Exception as e:
        logging.debug(f"⚠️ Police équivalente formatée échouée: {str(e)}")
    
    # ÉTAPE 4: Fallback police équivalente sans formatage
    try:
        equivalent_font = _get_pymupdf_font_equivalent(font_name)
        
        page.insert_text(
            text_position,
            new_text,
            fontname=equivalent_font,
            fontsize=font_size,
            color=normalized_color
        )
        logging.info(f"✅ POLICE ÉQUIVALENTE SANS FORMATAGE - '{original_text}' → '{new_text}' (police: {font_name} → {equivalent_font})")
        logging.warning(f"⚠️ FORMATAGE PERDU - Le gras/italique n'a pas pu être appliqué avec la police équivalente")
        return True
    except Exception as e:
        logging.debug(f"⚠️ Police équivalente sans formatage échouée: {str(e)}")
    
    return False