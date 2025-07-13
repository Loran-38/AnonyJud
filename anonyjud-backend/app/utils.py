# Fonctions utilitaires pour la gestion des fichiers, chiffrement, etc.
import fitz  # PyMuPDF
import logging
from typing import Optional

def lire_fichier(path):
    """Lit le contenu d'un fichier."""
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def ecrire_fichier(path, contenu):
    """Écrit du contenu dans un fichier."""
    with open(path, 'w', encoding='utf-8') as f:
        f.write(contenu)

def extract_text_from_pdf(pdf_content: bytes) -> str:
    """
    Extrait le texte d'un fichier PDF.
    
    Args:
        pdf_content: Le contenu du fichier PDF en bytes
        
    Returns:
        str: Le texte extrait du PDF
    """
    try:
        logging.info("Début extraction de texte PDF")
        
        # Ouvrir le PDF depuis les bytes
        doc = fitz.open(stream=pdf_content, filetype="pdf")
        
        # Extraire le texte de toutes les pages
        text = ""
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            page_text = page.get_text()
            text += page_text + "\n\n"
            logging.debug(f"Page {page_num + 1}: {len(page_text)} caractères extraits")
        
        doc.close()
        
        logging.info(f"Extraction terminée - Total: {len(text)} caractères")
        return text.strip()
        
    except Exception as e:
        logging.error(f"Erreur lors de l'extraction de texte PDF: {str(e)}")
        raise Exception(f"Impossible d'extraire le texte du PDF: {str(e)}") 