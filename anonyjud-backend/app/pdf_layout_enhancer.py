"""
Module d'amélioration de la mise en page PDF après anonymisation
Préserve les images, tableaux et éléments graphiques tout en gardant le texte éditable
"""

import fitz  # PyMuPDF
import io
import logging
from typing import Dict, List, Tuple, Any, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
import tempfile
import os

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PDFLayoutEnhancer:
    """
    Classe pour améliorer la mise en page des PDFs après anonymisation
    """
    
    def __init__(self):
        self.temp_files = []  # Pour nettoyer les fichiers temporaires
    
    def extract_visual_elements(self, pdf_content: bytes) -> Dict[str, Any]:
        """
        Extrait tous les éléments visuels d'un PDF (images, tableaux, graphiques)
        sans le texte sensible.
        
        Args:
            pdf_content: Contenu du PDF original en bytes
            
        Returns:
            Dict contenant les éléments visuels par page
        """
        logger.info("🎨 EXTRACT_VISUAL_ELEMENTS - Début de l'extraction")
        
        visual_elements = {
            "pages": [],
            "metadata": {}
        }
        
        try:
            doc = fitz.open(stream=pdf_content, filetype="pdf")
            
            # Métadonnées du document
            visual_elements["metadata"] = {
                "page_count": doc.page_count,
                "title": doc.metadata.get("title", ""),
                "subject": doc.metadata.get("subject", ""),
                "creator": doc.metadata.get("creator", "")
            }
            
            logger.info(f"📄 Document analysé: {doc.page_count} pages")
            
            for page_num in range(doc.page_count):
                page = doc[page_num]
                page_elements = self._extract_page_visual_elements(page, page_num)
                visual_elements["pages"].append(page_elements)
                
            doc.close()
            
            logger.info(f"✅ Extraction terminée: {len(visual_elements['pages'])} pages traitées")
            return visual_elements
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des éléments visuels: {str(e)}")
            raise
    
    def _extract_page_visual_elements(self, page: fitz.Page, page_num: int) -> Dict[str, Any]:
        """
        Extrait les éléments visuels d'une page spécifique.
        """
        page_elements = {
            "page_number": page_num,
            "page_size": {
                "width": page.rect.width,
                "height": page.rect.height
            },
            "images": [],
            "tables": [],
            "vector_graphics": [],
            "text_layout": []  # Positions et styles de texte sans contenu sensible
        }
        
        # 1. Extraire les images
        self._extract_images(page, page_elements)
        
        # 2. Extraire les tableaux
        self._extract_tables(page, page_elements)
        
        # 3. Extraire les graphiques vectoriels
        self._extract_vector_graphics(page, page_elements)
        
        # 4. Extraire la structure de mise en page du texte (sans contenu)
        self._extract_text_layout(page, page_elements)
        
        return page_elements
    
    def _extract_images(self, page: fitz.Page, page_elements: Dict):
        """Extrait les images avec leurs positions exactes."""
        try:
            image_list = page.get_images(full=True)
            logger.info(f"🖼️ Page {page_elements['page_number']}: {len(image_list)} images trouvées")
            
            for img_index, img in enumerate(image_list):
                try:
                    xref = img[0]
                    # Obtenir l'image comme Pixmap
                    pix = fitz.Pixmap(page.parent, xref)
                    
                    # Convertir en PNG
                    if pix.n < 5:  # GRAY ou RGB
                        img_data = pix.tobytes("png")
                    else:  # CMYK: convertir d'abord
                        pix1 = fitz.Pixmap(fitz.csRGB, pix)
                        img_data = pix1.tobytes("png")
                        pix1 = None
                    
                    # Obtenir la position sur la page - méthode alternative
                    try:
                        img_rect = page.get_image_bbox(img)
                    except:
                        # Fallback: utiliser une position par défaut
                        img_rect = fitz.Rect(0, 0, 100, 100)
                    
                    # Sauvegarder temporairement l'image
                    temp_img_path = self._save_temp_image(img_data, img_index, page_elements['page_number'])
                    
                    image_element = {
                        "index": img_index,
                        "data": img_data,
                        "temp_path": temp_img_path,
                        "bbox": {
                            "x0": img_rect.x0,
                            "y0": img_rect.y0,
                            "x1": img_rect.x1,
                            "y1": img_rect.y1,
                            "width": img_rect.width,
                            "height": img_rect.height
                        },
                        "xref": xref,
                        "colorspace": pix.colorspace.name if pix.colorspace and pix.colorspace else "unknown"
                    }
                    
                    page_elements["images"].append(image_element)
                    pix = None
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erreur extraction image {img_index}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des images: {str(e)}")
    
    def _extract_tables(self, page: fitz.Page, page_elements: Dict):
        """Extrait les tableaux structurés."""
        try:
            # Utiliser les tables détectées par PyMuPDF (méthode sécurisée)
            try:
                tables = page.find_tables()
                if hasattr(tables, '__len__'):
                    table_count = len(tables)
                elif hasattr(tables, '__iter__'):
                    table_list = list(tables)
                    table_count = len(table_list)
                    tables = table_list
                else:
                    table_count = 0
                    tables = []
            except:
                # Fallback si find_tables() n'est pas disponible
                table_count = 0
                tables = []
            
            logger.info(f"📊 Page {page_elements['page_number']}: {table_count} tableaux trouvés")
            
            for table_index, table in enumerate(tables):
                try:
                    # Extraire la structure du tableau sans le contenu textuel sensible
                    table_data = {
                        "index": table_index,
                        "bbox": {
                            "x0": getattr(table.bbox, 'x0', 0),
                            "y0": getattr(table.bbox, 'y0', 0),
                            "x1": getattr(table.bbox, 'x1', 100),
                            "y1": getattr(table.bbox, 'y1', 100),
                            "width": getattr(table.bbox, 'width', 100),
                            "height": getattr(table.bbox, 'height', 100)
                        },
                        "rows": 0,
                        "cols": 0,
                        "cell_layout": []  # Structure sans contenu
                    }
                    
                    # Extraire la structure des cellules de manière sécurisée
                    try:
                        table_content = table.extract()
                        if table_content:
                            table_data["rows"] = len(table_content)
                            table_data["cols"] = len(table_content[0]) if table_content[0] else 0
                            
                            # Structure des cellules
                            for row_idx, row in enumerate(table_content):
                                row_layout = []
                                for col_idx, cell in enumerate(row):
                                    cell_layout = {
                                        "row": row_idx,
                                        "col": col_idx,
                                        "is_empty": not bool(cell and str(cell).strip())
                                    }
                                    row_layout.append(cell_layout)
                                table_data["cell_layout"].append(row_layout)
                    except:
                        logger.warning(f"⚠️ Impossible d'extraire le contenu du tableau {table_index}")
                    
                    page_elements["tables"].append(table_data)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erreur extraction tableau {table_index}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des tableaux: {str(e)}")
    
    def _extract_vector_graphics(self, page: fitz.Page, page_elements: Dict):
        """Extrait les graphiques vectoriels (lignes, formes, etc.)."""
        try:
            drawings = page.get_drawings()
            logger.info(f"🎯 Page {page_elements['page_number']}: {len(drawings)} éléments vectoriels")
            
            for drawing_index, drawing in enumerate(drawings):
                try:
                    # Simplifier et nettoyer les données de dessin
                    clean_drawing = {
                        "index": drawing_index,
                        "type": drawing.get("type", "unknown"),
                        "bbox": drawing.get("rect", [0, 0, 0, 0]),
                        "items": [],
                        "fill": drawing.get("fill", None),
                        "stroke": drawing.get("stroke", None),
                        "width": drawing.get("width", 1)
                    }
                    
                    # Traiter les éléments du dessin
                    for item in drawing.get("items", []):
                        if len(item) >= 2:
                            clean_item = {
                                "command": item[0],
                                "points": item[1] if isinstance(item[1], list) else []
                            }
                            clean_drawing["items"].append(clean_item)
                    
                    page_elements["vector_graphics"].append(clean_drawing)
                    
                except Exception as e:
                    logger.warning(f"⚠️ Erreur extraction dessin {drawing_index}: {str(e)}")
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction des graphiques vectoriels: {str(e)}")
    
    def _extract_text_layout(self, page: fitz.Page, page_elements: Dict):
        """Extrait la structure de mise en page du texte sans le contenu sensible."""
        try:
            text_dict = page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" in block:  # Bloc de texte
                    block_layout = {
                        "bbox": block["bbox"],
                        "lines": []
                    }
                    
                    for line in block["lines"]:
                        line_layout = {
                            "bbox": line["bbox"],
                            "spans": []
                        }
                        
                        for span in line["spans"]:
                            # Seulement les informations de style, pas le texte
                            span_layout = {
                                "bbox": span["bbox"],
                                "font": span["font"],
                                "size": span["size"],
                                "flags": span["flags"],
                                "color": span.get("color", 0),
                                "text_length": len(span["text"])  # Longueur pour réserver l'espace
                            }
                            line_layout["spans"].append(span_layout)
                        
                        block_layout["lines"].append(line_layout)
                    
                    page_elements["text_layout"].append(block_layout)
                    
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'extraction de la mise en page: {str(e)}")
    
    def _save_temp_image(self, img_data: bytes, img_index: int, page_num: int) -> str:
        """Sauvegarde temporairement une image extraite."""
        try:
            temp_file = tempfile.NamedTemporaryFile(
                delete=False, 
                suffix=f"_p{page_num}_img{img_index}.png",
                prefix="pdf_extract_"
            )
            temp_file.write(img_data)
            temp_file.close()
            
            self.temp_files.append(temp_file.name)
            return temp_file.name
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur sauvegarde image temporaire: {str(e)}")
            return ""
    
    def enhance_anonymized_pdf(self, anonymized_pdf_content: bytes, 
                              visual_elements: Dict[str, Any]) -> bytes:
        """
        Améliore un PDF anonymisé en réinjectant les éléments visuels.
        
        Args:
            anonymized_pdf_content: PDF avec texte anonymisé
            visual_elements: Éléments visuels extraits du PDF original
            
        Returns:
            PDF amélioré avec texte anonymisé + éléments visuels
        """
        logger.info("🚀 ENHANCE_ANONYMIZED_PDF - Début de l'amélioration")
        
        try:
            # Ouvrir le PDF anonymisé
            anonymized_doc = fitz.open(stream=anonymized_pdf_content, filetype="pdf")
            
            # Créer un nouveau PDF amélioré
            enhanced_pdf = self._create_enhanced_pdf(anonymized_doc, visual_elements)
            
            anonymized_doc.close()
            
            logger.info("✅ PDF amélioré créé avec succès")
            return enhanced_pdf
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'amélioration du PDF: {str(e)}")
            raise
    
    def _create_enhanced_pdf(self, anonymized_doc: fitz.Document, 
                           visual_elements: Dict[str, Any]) -> bytes:
        """Crée le PDF amélioré en combinant texte anonymisé et éléments visuels."""
        
        buffer = io.BytesIO()
        
        # Utiliser ReportLab pour créer le PDF final
        from reportlab.pdfgen import canvas as rl_canvas
        from reportlab.lib.pagesizes import A4
        
        # Créer le canvas
        c = rl_canvas.Canvas(buffer)
        
        page_count = min(anonymized_doc.page_count, len(visual_elements["pages"]))
        
        for page_num in range(page_count):
            logger.info(f"📄 Traitement page {page_num + 1}/{page_count}")
            
            anonymized_page = anonymized_doc[page_num]
            visual_page = visual_elements["pages"][page_num]
            
            # Définir la taille de la page
            page_width = visual_page["page_size"]["width"]
            page_height = visual_page["page_size"]["height"]
            c.setPageSize((page_width, page_height))
            
            # 1. Ajouter les images en arrière-plan
            self._add_images_to_canvas(c, visual_page["images"], page_height)
            
            # 2. Ajouter les graphiques vectoriels
            self._add_vector_graphics_to_canvas(c, visual_page["vector_graphics"], page_height)
            
            # 3. Ajouter les tableaux (structure)
            self._add_tables_to_canvas(c, visual_page["tables"], page_height)
            
            # 4. Ajouter le texte anonymisé du PDF anonymisé
            self._add_anonymized_text_to_canvas(c, anonymized_page, page_height)
            
            # Passer à la page suivante
            if page_num < page_count - 1:
                c.showPage()
        
        # Finaliser le PDF
        c.save()
        
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        return pdf_bytes
    
    def _add_images_to_canvas(self, canvas_obj, images: List[Dict], page_height: float):
        """Ajoute les images extraites au canvas."""
        for img in images:
            try:
                if img["temp_path"] and os.path.exists(img["temp_path"]):
                    bbox = img["bbox"]
                    
                    # Conversion des coordonnées (PyMuPDF -> ReportLab)
                    x = bbox["x0"]
                    y = page_height - bbox["y1"]  # Inversion Y
                    width = bbox["width"]
                    height = bbox["height"]
                    
                    # Ajouter l'image
                    canvas_obj.drawImage(
                        img["temp_path"],
                        x, y, width, height,
                        preserveAspectRatio=True
                    )
                    
                    logger.debug(f"🖼️ Image ajoutée: {width}x{height} à ({x}, {y})")
                    
            except Exception as e:
                logger.warning(f"⚠️ Erreur ajout image: {str(e)}")
    
    def _add_vector_graphics_to_canvas(self, canvas_obj, graphics: List[Dict], page_height: float):
        """Ajoute les graphiques vectoriels au canvas."""
        for graphic in graphics:
            try:
                if graphic["type"] == "l":  # Ligne
                    for item in graphic["items"]:
                        if item["command"] == "l" and len(item["points"]) >= 2:
                            points = item["points"]
                            canvas_obj.line(
                                points[0], page_height - points[1],
                                points[2], page_height - points[3]
                            )
                            
                elif graphic["type"] == "re":  # Rectangle
                    bbox = graphic["bbox"]
                    if len(bbox) == 4:
                        x, y, x1, y1 = bbox
                        canvas_obj.rect(
                            x, page_height - y1,
                            x1 - x, y1 - y
                        )
                        
            except Exception as e:
                logger.warning(f"⚠️ Erreur ajout graphique: {str(e)}")
    
    def _add_tables_to_canvas(self, canvas_obj, tables: List[Dict], page_height: float):
        """Ajoute la structure des tableaux au canvas."""
        for table in tables:
            try:
                bbox = table["bbox"]
                
                # Dessiner le contour du tableau
                canvas_obj.rect(
                    bbox["x0"], page_height - bbox["y1"],
                    bbox["width"], bbox["height"],
                    stroke=1, fill=0
                )
                
                # Dessiner une grille basique pour la structure
                rows = table["rows"]
                cols = table["cols"]
                
                if rows > 1 and cols > 1:
                    cell_width = bbox["width"] / cols
                    cell_height = bbox["height"] / rows
                    
                    # Lignes horizontales
                    for row in range(1, rows):
                        y = page_height - bbox["y0"] - (row * cell_height)
                        canvas_obj.line(bbox["x0"], y, bbox["x1"], y)
                    
                    # Lignes verticales
                    for col in range(1, cols):
                        x = bbox["x0"] + (col * cell_width)
                        canvas_obj.line(x, page_height - bbox["y0"], x, page_height - bbox["y1"])
                        
            except Exception as e:
                logger.warning(f"⚠️ Erreur ajout tableau: {str(e)}")
    
    def _add_anonymized_text_to_canvas(self, canvas_obj, anonymized_page: fitz.Page, page_height: float):
        """Ajoute le texte anonymisé au canvas."""
        try:
            text_dict = anonymized_page.get_text("dict")
            
            for block in text_dict.get("blocks", []):
                if "lines" in block:  # Bloc de texte
                    for line in block["lines"]:
                        for span in line["spans"]:
                            text = span["text"].strip()
                            if text:
                                bbox = span["bbox"]
                                font_size = span["size"]
                                
                                # Position du texte
                                x = bbox[0]
                                y = page_height - bbox[1] - font_size  # Ajustement Y
                                
                                # Configuration de la police
                                try:
                                    canvas_obj.setFont("Helvetica", font_size)
                                except:
                                    canvas_obj.setFont("Helvetica", 12)  # Police par défaut
                                
                                # Ajouter le texte anonymisé
                                canvas_obj.drawString(x, y, text)
                                
        except Exception as e:
            logger.warning(f"⚠️ Erreur ajout texte anonymisé: {str(e)}")
    
    def cleanup_temp_files(self):
        """Nettoie les fichiers temporaires créés."""
        for temp_file in self.temp_files:
            try:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
                    logger.debug(f"🗑️ Fichier temporaire supprimé: {temp_file}")
            except Exception as e:
                logger.warning(f"⚠️ Erreur suppression fichier temporaire {temp_file}: {str(e)}")
        
        self.temp_files.clear()
    
    def __del__(self):
        """Destructeur pour nettoyer automatiquement."""
        self.cleanup_temp_files()


def enhance_pdf_layout_after_anonymization(original_pdf: bytes, 
                                         anonymized_pdf: bytes) -> bytes:
    """
    Fonction utilitaire pour améliorer la mise en page d'un PDF après anonymisation.
    
    Args:
        original_pdf: PDF original avec images/tableaux
        anonymized_pdf: PDF avec texte anonymisé mais mise en page dégradée
        
    Returns:
        PDF amélioré avec texte anonymisé + éléments visuels préservés
    """
    enhancer = PDFLayoutEnhancer()
    
    try:
        # 1. Extraire les éléments visuels du PDF original
        logger.info("🎨 Extraction des éléments visuels du PDF original")
        visual_elements = enhancer.extract_visual_elements(original_pdf)
        
        # 2. Améliorer le PDF anonymisé
        logger.info("🚀 Amélioration du PDF anonymisé")
        enhanced_pdf = enhancer.enhance_anonymized_pdf(anonymized_pdf, visual_elements)
        
        return enhanced_pdf
        
    finally:
        # 3. Nettoyer les fichiers temporaires
        enhancer.cleanup_temp_files()


# Exemple de preuve de concept minimale
def proof_of_concept_extract_reinject_images(pdf_content: bytes) -> bytes:
    """
    Preuve de concept : extrait les images d'un PDF et les réinjecte dans un nouveau PDF.
    
    Args:
        pdf_content: Contenu du PDF source
        
    Returns:
        Nouveau PDF avec seulement les images réinjectées
    """
    logger.info("🧪 PROOF_OF_CONCEPT - Extraction et réinjection d'images")
    
    enhancer = PDFLayoutEnhancer()
    
    try:
        # Extraire les éléments visuels
        visual_elements = enhancer.extract_visual_elements(pdf_content)
        
        # Créer un PDF minimal avec seulement les images
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer)
        
        for page_data in visual_elements["pages"]:
            page_width = page_data["page_size"]["width"]
            page_height = page_data["page_size"]["height"]
            c.setPageSize((page_width, page_height))
            
            # Ajouter seulement les images
            enhancer._add_images_to_canvas(c, page_data["images"], page_height)
            
            # Ajouter un texte de test
            c.setFont("Helvetica", 14)
            c.drawString(50, page_height - 50, f"Page {page_data['page_number'] + 1} - Images extraites et réinjectées")
            
            if page_data["page_number"] < len(visual_elements["pages"]) - 1:
                c.showPage()
        
        c.save()
        result = buffer.getvalue()
        buffer.close()
        
        logger.info("✅ Preuve de concept terminée")
        return result
        
    finally:
        enhancer.cleanup_temp_files() 