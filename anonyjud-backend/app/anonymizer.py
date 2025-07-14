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
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Extraire tout le texte pour générer le mapping
        for page in doc:
            full_text += page.get_text() + "\n"
        
        doc.close()
        
        # Générer le mapping d'anonymisation
        anonymized_text, mapping = anonymize_text(full_text, tiers)
        logging.info(f"📊 Mapping généré: {len(mapping)} remplacements - {list(mapping.keys())}")
        
        # Inverser le mapping pour avoir {valeur_originale: balise_anonymisée}
        reverse_mapping = {v: k for k, v in mapping.items()}
        logging.info(f"📊 Mapping inversé: {reverse_mapping}")
        
        # Ouvrir le PDF pour modification
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Parcourir chaque page
        for page_num in range(len(doc)):
            page = doc[page_num]
            logging.info(f"📄 Traitement page {page_num + 1}/{len(doc)}")
            
            # Obtenir tous les blocs de texte de la page
            text_blocks = page.get_text("dict")
            
            # Parcourir chaque bloc de texte
            for block in text_blocks["blocks"]:
                if "lines" in block:  # Bloc de texte
                    _anonymize_text_block_direct(page, block, reverse_mapping)
        
        # Sauvegarder le PDF modifié
        anonymized_pdf = doc.tobytes()
        doc.close()
        
        logging.info(f"✅ Anonymisation PDF directe terminée avec succès")
        logging.info(f"📊 Taille PDF anonymisé: {len(anonymized_pdf)} bytes")
        
        return anonymized_pdf, mapping
        
    except Exception as e:
        logging.error(f"❌ Erreur lors de l'anonymisation PDF directe: {str(e)}")
        raise Exception(f"Erreur anonymisation PDF directe: {str(e)}")


def _anonymize_text_block_direct(page, block, mapping: Dict[str, str]):
    """
    Anonymise un bloc de texte directement dans la page PDF.
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
                
                # Effacer l'ancien texte en le couvrant avec un rectangle blanc
                page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                
                # Insérer le nouveau texte anonymisé avec les mêmes propriétés
                try:
                    page.insert_text(
                        bbox.tl,  # Position top-left
                        anonymized_text,
                        fontname=font_name,
                        fontsize=font_size,
                        color=text_color
                    )
                    logging.debug(f"✅ Texte remplacé: '{original_text}' → '{anonymized_text}'")
                except Exception as e:
                    logging.warning(f"⚠️ Erreur remplacement texte: {str(e)}")
                    # Fallback: utiliser une police par défaut
                    try:
                        page.insert_text(
                            bbox.tl,
                            anonymized_text,
                            fontname="helv",  # Police par défaut
                            fontsize=font_size,
                            color=text_color
                        )
                        logging.debug(f"✅ Texte remplacé avec police par défaut")
                    except Exception as e2:
                        logging.error(f"❌ Impossible de remplacer le texte: {str(e2)}")


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
    
    logging.info("🔓 Début dé-anonymisation PDF directe avec PyMuPDF")
    logging.info(f"📊 Taille PDF d'entrée: {len(pdf_content)} bytes")
    logging.info(f"🔢 Nombre de balises dans le mapping: {len(mapping)}")
    
    try:
        # Ouvrir le PDF pour modification
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Parcourir chaque page
        for page_num in range(len(doc)):
            page = doc[page_num]
            logging.info(f"📄 Traitement page {page_num + 1}/{len(doc)}")
            
            # Obtenir tous les blocs de texte de la page
            text_blocks = page.get_text("dict")
            
            # Parcourir chaque bloc de texte
            for block in text_blocks["blocks"]:
                if "lines" in block:  # Bloc de texte
                    _deanonymize_text_block_direct(page, block, mapping)
        
        # Sauvegarder le PDF modifié
        deanonymized_pdf = doc.tobytes()
        doc.close()
        
        logging.info(f"✅ Dé-anonymisation PDF directe terminée avec succès")
        logging.info(f"📊 Taille PDF dé-anonymisé: {len(deanonymized_pdf)} bytes")
        
        return deanonymized_pdf
        
    except Exception as e:
        logging.error(f"❌ Erreur lors de la dé-anonymisation PDF directe: {str(e)}")
        raise Exception(f"Erreur dé-anonymisation PDF directe: {str(e)}")


def _deanonymize_text_block_direct(page, block, mapping: Dict[str, str]):
    """
    Dé-anonymise un bloc de texte directement dans la page PDF.
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
                
                # Effacer l'ancien texte en le couvrant avec un rectangle blanc
                page.draw_rect(bbox, color=None, fill=fitz.pdfcolor["white"])
                
                # Insérer le nouveau texte dé-anonymisé avec les mêmes propriétés
                try:
                    page.insert_text(
                        bbox.tl,  # Position top-left
                        deanonymized_text,
                        fontname=font_name,
                        fontsize=font_size,
                        color=text_color
                    )
                    logging.debug(f"✅ Texte dé-anonymisé: '{original_text}' → '{deanonymized_text}'")
                except Exception as e:
                    logging.warning(f"⚠️ Erreur dé-anonymisation texte: {str(e)}")
                    # Fallback: utiliser une police par défaut
                    try:
                        page.insert_text(
                            bbox.tl,
                            deanonymized_text,
                            fontname="helv",  # Police par défaut
                            fontsize=font_size,
                            color=text_color
                        )
                        logging.debug(f"✅ Texte dé-anonymisé avec police par défaut")
                    except Exception as e2:
                        logging.error(f"❌ Impossible de dé-anonymiser le texte: {str(e2)}")


# ===== FIN ANONYMISATION DIRECTE PDF ===== 