"""
Utilitaires pour le traitement sécurisé des PDFs
Gère les erreurs get_text() et autres problèmes de traitement PDF
"""
import fitz  # PyMuPDF
from typing import Tuple, Optional
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def safe_extract_text_from_pdf(content: bytes) -> Tuple[str, bool]:
    """
    Extrait le texte d'un PDF de manière sécurisée.
    
    Args:
        content: Contenu du PDF en bytes
        
    Returns:
        Tuple[str, bool]: (texte_extrait, succès)
        - texte_extrait: Le texte extrait ou une chaîne vide si erreur
        - succès: True si l'extraction a réussi, False sinon
    """
    text = ""
    success = True
    
    try:
        logger.info("🔍 SAFE_EXTRACT_TEXT_FROM_PDF - Début de l'extraction")
        
        # Validation du contenu
        if not content or len(content) == 0:
            logger.error("❌ Contenu PDF vide ou None")
            return "", False
            
        if len(content) < 100:  # Un PDF valide fait au moins quelques centaines d'octets
            logger.error(f"❌ Contenu PDF trop petit: {len(content)} bytes")
            return "", False
        
        # Vérifier la signature PDF
        if not content.startswith(b'%PDF'):
            logger.error("❌ Signature PDF invalide")
            return "", False
            
        logger.info(f"✅ Validation PDF passée, taille: {len(content)} bytes")
        
        # Ouvrir le PDF avec gestion d'erreur
        try:
            pdf_doc = fitz.open(stream=content, filetype="pdf")
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'ouverture du PDF: {str(e)}")
            return "", False
            
        # Vérifier si le PDF est protégé
        if pdf_doc.needs_pass:
            logger.error("❌ PDF protégé par mot de passe")
            pdf_doc.close()
            return "", False
            
        # Vérifier le nombre de pages
        if pdf_doc.page_count == 0:
            logger.error("❌ PDF sans pages")
            pdf_doc.close()
            return "", False
            
        logger.info(f"📄 PDF ouvert avec succès: {pdf_doc.page_count} pages")
        
        # Extraire le texte page par page avec gestion d'erreur individuelle
        pages_processed = 0
        pages_failed = 0
        
        for page_num in range(pdf_doc.page_count):
            try:
                logger.debug(f"📖 Traitement page {page_num + 1}/{pdf_doc.page_count}")
                
                # Obtenir la page
                page = pdf_doc[page_num]
                
                # Vérifier que la page est valide
                if page is None:
                    logger.warning(f"⚠️ Page {page_num + 1} est None, passage à la suivante")
                    pages_failed += 1
                    continue
                
                # Tentative d'extraction avec plusieurs méthodes
                page_text = ""
                
                # Méthode 1: get_text() standard
                try:
                    page_text = page.get_text()
                    if page_text:
                        logger.debug(f"✅ Page {page_num + 1}: texte extrait avec get_text() ({len(page_text)} chars)")
                except Exception as e:
                    logger.warning(f"⚠️ Page {page_num + 1}: get_text() a échoué: {str(e)}")
                    
                    # Méthode 2: get_text("text") alternative
                    try:
                        page_text = page.get_text("text")
                        if page_text:
                            logger.debug(f"✅ Page {page_num + 1}: texte extrait avec get_text('text') ({len(page_text)} chars)")
                    except Exception as e2:
                        logger.warning(f"⚠️ Page {page_num + 1}: get_text('text') a aussi échoué: {str(e2)}")
                        
                        # Méthode 3: Extraction par blocs
                        try:
                            text_dict = page.get_text("dict")
                            page_text = ""
                            for block in text_dict.get("blocks", []):
                                if "lines" in block:
                                    for line in block["lines"]:
                                        for span in line["spans"]:
                                            page_text += span.get("text", "")
                            
                            if page_text:
                                logger.debug(f"✅ Page {page_num + 1}: texte extrait par blocs ({len(page_text)} chars)")
                        except Exception as e3:
                            logger.error(f"❌ Page {page_num + 1}: toutes les méthodes d'extraction ont échoué: {str(e3)}")
                            pages_failed += 1
                            continue
                
                # Ajouter le texte de la page
                if page_text:
                    text += page_text + "\n"
                    pages_processed += 1
                else:
                    logger.warning(f"⚠️ Page {page_num + 1}: aucun texte extrait")
                    pages_failed += 1
                    
            except Exception as e:
                logger.error(f"❌ Erreur inattendue lors du traitement de la page {page_num + 1}: {str(e)}")
                pages_failed += 1
                continue
        
        # Fermer le document
        try:
            pdf_doc.close()
        except Exception as e:
            logger.warning(f"⚠️ Erreur lors de la fermeture du PDF: {str(e)}")
        
        # Évaluer le succès
        if pages_processed == 0:
            logger.error(f"❌ Aucune page traitée avec succès (0/{pdf_doc.page_count})")
            success = False
        elif pages_failed > 0:
            logger.warning(f"⚠️ Traitement partiel: {pages_processed}/{pdf_doc.page_count} pages réussies, {pages_failed} échecs")
            # On considère que c'est un succès partiel si au moins 50% des pages sont traitées
            success = pages_processed >= (pdf_doc.page_count / 2)
        else:
            logger.info(f"✅ Toutes les pages traitées avec succès: {pages_processed}/{pdf_doc.page_count}")
        
        logger.info(f"📊 Résultat final: {len(text)} caractères extraits, succès: {success}")
        
        return text.strip(), success
        
    except Exception as e:
        logger.error(f"❌ Erreur générale dans safe_extract_text_from_pdf: {str(e)}")
        return "", False

def validate_pdf_content(content: bytes) -> Tuple[bool, str]:
    """
    Valide un contenu PDF sans l'ouvrir complètement.
    
    Args:
        content: Contenu du PDF en bytes
        
    Returns:
        Tuple[bool, str]: (est_valide, message_erreur)
    """
    try:
        if not content:
            return False, "Contenu vide"
            
        if len(content) < 100:
            return False, f"Contenu trop petit: {len(content)} bytes"
            
        if not content.startswith(b'%PDF'):
            return False, "Signature PDF manquante"
            
        # Test d'ouverture rapide
        try:
            with fitz.open(stream=content, filetype="pdf") as pdf:
                if pdf.needs_pass:
                    return False, "PDF protégé par mot de passe"
                if pdf.page_count == 0:
                    return False, "PDF sans pages"
                    
            return True, "PDF valide"
            
        except Exception as e:
            return False, f"Erreur d'ouverture: {str(e)}"
            
    except Exception as e:
        return False, f"Erreur de validation: {str(e)}"

def safe_pdf_operation(content: bytes, operation_name: str = "opération PDF"):
    """
    Décorateur/context manager pour les opérations PDF sécurisées.
    """
    class SafePDFContext:
        def __init__(self, content: bytes, operation_name: str):
            self.content = content
            self.operation_name = operation_name
            self.pdf_doc = None
            
        def __enter__(self):
            logger.info(f"🔒 Début de l'opération sécurisée: {self.operation_name}")
            
            # Validation du PDF
            is_valid, error_msg = validate_pdf_content(self.content)
            if not is_valid:
                raise ValueError(f"PDF invalide: {error_msg}")
            
            # Ouverture sécurisée
            try:
                self.pdf_doc = fitz.open(stream=self.content, filetype="pdf")
                logger.info(f"✅ PDF ouvert pour {self.operation_name}")
                return self.pdf_doc
            except Exception as e:
                logger.error(f"❌ Erreur ouverture PDF pour {self.operation_name}: {str(e)}")
                raise
                
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.pdf_doc:
                try:
                    self.pdf_doc.close()
                    logger.info(f"🔒 PDF fermé après {self.operation_name}")
                except Exception as e:
                    logger.warning(f"⚠️ Erreur fermeture PDF: {str(e)}")
            
            if exc_type:
                logger.error(f"❌ Erreur dans {self.operation_name}: {exc_val}")
            else:
                logger.info(f"✅ {self.operation_name} terminée avec succès")
    
    return SafePDFContext(content, operation_name) 