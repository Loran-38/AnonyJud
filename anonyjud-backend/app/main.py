from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import os
import tempfile
from pathlib import Path
import fitz  # PyMuPDF pour les PDF
from docx import Document  # python-docx pour les fichiers Word
import io
import re
from odf import text as odf_text, teletype
from odf.opendocument import load

from .anonymizer import anonymize_text
from .deanonymizer import deanonymize_text
from .models import TextAnonymizationRequest, TextDeanonymizationRequest

app = FastAPI()

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier l'origine exacte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "AnonyJud API is running"}

@app.post("/anonymize/text")
def anonymize_text_endpoint(request: TextAnonymizationRequest):
    """
    Anonymise un texte en utilisant les tiers fournis.
    """
    try:
        anonymized, mapping = anonymize_text(request.text, request.tiers)
        return {"anonymized_text": anonymized, "mapping": mapping}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deanonymize/text")
def deanonymize_text_endpoint(request: TextDeanonymizationRequest):
    """
    Dé-anonymise un texte en utilisant le mapping fourni.
    """
    try:
        deanonymized = deanonymize_text(request.anonymized_text, request.mapping)
        return {"deanonymized_text": deanonymized}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anonymize/file")
async def anonymize_file(
    file: UploadFile = File(...),
    tiers_json: str = Form(...)
):
    """
    Anonymise un fichier Word, PDF ou ODT en utilisant les tiers fournis.
    """
    try:
        # Convertir la chaîne JSON en liste de tiers
        tiers = json.loads(tiers_json)
        
        # Vérifier le type de fichier
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension == ".pdf":
            # Traitement des fichiers PDF
            content = await file.read()
            pdf_text, mapping = extract_and_anonymize_pdf(content, tiers)
            return {"text": pdf_text, "mapping": mapping}
            
        elif file_extension in [".doc", ".docx"]:
            # Traitement des fichiers Word
            content = await file.read()
            doc_text, mapping = extract_and_anonymize_docx(content, tiers)
            return {"text": doc_text, "mapping": mapping}
            
        elif file_extension == ".odt":
            # Traitement des fichiers ODT (OpenDocument Text)
            content = await file.read()
            odt_text, mapping = extract_and_anonymize_odt(content, tiers)
            return {"text": odt_text, "mapping": mapping}
            
        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anonymize/file/download")
async def anonymize_file_download(
    file: UploadFile = File(...),
    tiers_json: str = Form(...)
):
    """
    Anonymise un fichier Word et retourne le fichier modifié pour téléchargement.
    """
    try:
        # Convertir la chaîne JSON en liste de tiers
        tiers = json.loads(tiers_json)
        
        # Vérifier le type de fichier
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension in [".doc", ".docx"]:
            # Traitement des fichiers Word
            content = await file.read()
            anonymized_file, mapping = anonymize_docx_file(content, tiers)
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            anonymized_filename = f"{base_name}_ANONYM.docx"
            
            # Retourner le fichier modifié
            return StreamingResponse(
                io.BytesIO(anonymized_file),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={anonymized_filename}"}
            )
        else:
            raise HTTPException(status_code=400, detail="Seuls les fichiers Word (.docx) sont supportés pour le téléchargement.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deanonymize/file/download")
async def deanonymize_file_download(
    file: UploadFile = File(...),
    mapping_json: str = Form(...)
):
    """
    Dé-anonymise un fichier Word et retourne le fichier modifié pour téléchargement.
    """
    try:
        # Convertir la chaîne JSON en mapping
        mapping = json.loads(mapping_json)
        
        # Vérifier le type de fichier
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension in [".doc", ".docx"]:
            # Traitement des fichiers Word
            content = await file.read()
            deanonymized_file = deanonymize_docx_file(content, mapping)
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            # Retirer "_ANONYM" du nom si présent
            if base_name.endswith("_ANONYM"):
                base_name = base_name[:-7]
            deanonymized_filename = f"{base_name}_DESANONYM.docx"
            
            # Retourner le fichier modifié
            return StreamingResponse(
                io.BytesIO(deanonymized_file),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={deanonymized_filename}"}
            )
        else:
            raise HTTPException(status_code=400, detail="Seuls les fichiers Word (.docx) sont supportés pour le téléchargement.")
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def extract_and_anonymize_pdf(content: bytes, tiers: List[Dict[str, Any]]):
    """
    Extrait le texte d'un PDF et l'anonymise.
    """
    try:
        # Ouvrir le PDF depuis les bytes
        with fitz.open(stream=content, filetype="pdf") as pdf:
            text = ""
            # Extraire le texte de chaque page
            for page in pdf:
                text += page.get_text()
        
        # Anonymiser le texte extrait
        anonymized, mapping = anonymize_text(text, tiers)
        return anonymized, mapping
        
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du PDF: {str(e)}")

def extract_and_anonymize_docx(content: bytes, tiers: List[Dict[str, Any]]):
    """
    Extrait le texte d'un document Word et l'anonymise.
    """
    try:
        # Ouvrir le document Word depuis les bytes
        doc = Document(io.BytesIO(content))
        text = ""
        
        # Extraire le texte de chaque paragraphe
        for para in doc.paragraphs:
            text += para.text + "\n"
            
        # Anonymiser le texte extrait
        anonymized, mapping = anonymize_text(text, tiers)
        return anonymized, mapping
        
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du document Word: {str(e)}")

def extract_and_anonymize_odt(content: bytes, tiers: List[Dict[str, Any]]):
    """
    Extrait le texte d'un document OpenDocument Text (ODT) et l'anonymise.
    """
    try:
        # Créer un fichier temporaire pour stocker le contenu ODT
        with tempfile.NamedTemporaryFile(delete=False, suffix=".odt") as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Charger le document ODT
            doc = load(temp_path)
            
            # Extraire le texte du document
            text = ""
            
            # Parcourir tous les éléments de texte dans le document
            for paragraph in doc.getElementsByType(odf_text.P):
                text += teletype.extractText(paragraph) + "\n"
            
            # Anonymiser le texte extrait
            anonymized, mapping = anonymize_text(text, tiers)
            
            return anonymized, mapping
            
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du document ODT: {str(e)}") 

def anonymize_docx_file(content: bytes, tiers: List[Dict[str, Any]]):
    """
    Anonymise directement un fichier Word en modifiant son contenu.
    Retourne le fichier modifié et le mapping d'anonymisation.
    """
    try:
        print(f"DEBUG: Début anonymize_docx_file avec {len(tiers)} tiers")
        
        # Ouvrir le document Word depuis les bytes
        doc = Document(io.BytesIO(content))
        
        # Collecter tout le texte du document
        full_text = ""
        for para in doc.paragraphs:
            full_text += para.text + "\n"
        
        print(f"DEBUG: Texte extrait (premiers 200 chars): {full_text[:200]}...")
        
        # Anonymiser le texte complet pour obtenir le mapping
        anonymized_text, mapping = anonymize_text(full_text, tiers)
        
        print(f"DEBUG: Mapping généré: {mapping}")
        print(f"DEBUG: Texte anonymisé (premiers 200 chars): {anonymized_text[:200]}...")
        
        # Appliquer les anonymisations directement dans le document
        for para in doc.paragraphs:
            if para.text.strip():  # Seulement pour les paragraphes non vides
                original_text = para.text
                modified_text = original_text
                
                # Appliquer chaque remplacement du mapping (inverser pour que les tags remplacent les originaux)
                for tag, original_value in mapping.items():
                    modified_text = modified_text.replace(original_value, tag)
                
                # Remplacer le texte du paragraphe seulement si modifié
                if modified_text != original_text:
                    print(f"DEBUG: Paragraphe modifié: '{original_text}' -> '{modified_text}'")
                    para.clear()
                    para.add_run(modified_text)
        
        # Traiter également les tableaux
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if para.text.strip():
                            original_text = para.text
                            modified_text = original_text
                            
                            # Appliquer chaque remplacement du mapping
                            for tag, original_value in mapping.items():
                                modified_text = modified_text.replace(original_value, tag)
                            
                            # Remplacer le texte du paragraphe seulement si modifié
                            if modified_text != original_text:
                                print(f"DEBUG: Cellule modifiée: '{original_text}' -> '{modified_text}'")
                                para.clear()
                                para.add_run(modified_text)
        
        # Sauvegarder le document modifié en bytes
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        print(f"DEBUG: Fichier anonymisé généré avec succès")
        return output.getvalue(), mapping
        
    except Exception as e:
        print(f"DEBUG: Erreur dans anonymize_docx_file: {str(e)}")
        raise Exception(f"Erreur lors de l'anonymisation du fichier Word: {str(e)}")

def deanonymize_docx_file(content: bytes, mapping: Dict[str, str]):
    """
    Dé-anonymise directement un fichier Word en utilisant le mapping fourni.
    Retourne le fichier modifié.
    """
    try:
        print(f"DEBUG: Début deanonymize_docx_file avec mapping: {mapping}")
        
        # Ouvrir le document Word depuis les bytes
        doc = Document(io.BytesIO(content))
        
        # Le mapping contient tag -> valeur_originale
        # Pour la désanonymisation, on remplace les tags par les valeurs originales
        
        # Trier les balises par longueur décroissante pour éviter les remplacements partiels
        sorted_tags = sorted(mapping.keys(), key=len, reverse=True)
        print(f"DEBUG: Balises triées: {sorted_tags}")
        
        # Appliquer les dé-anonymisations dans les paragraphes
        for para in doc.paragraphs:
            if para.text.strip():  # Seulement pour les paragraphes non vides
                original_text = para.text
                modified_text = original_text
                
                print(f"DEBUG: Traitement paragraphe: '{original_text}'")
                
                # Appliquer chaque remplacement du mapping : tag -> valeur originale
                # Utiliser la même logique que deanonymize_text
                for tag in sorted_tags:
                    original_value = mapping[tag]
                    # Utiliser une expression régulière pour remplacer la balise exacte
                    pattern = re.compile(r'\b' + re.escape(tag) + r'\b')
                    before_replace = modified_text
                    modified_text = pattern.sub(original_value, modified_text)
                    if before_replace != modified_text:
                        print(f"DEBUG: Remplacement effectué: '{tag}' -> '{original_value}' dans '{before_replace}' -> '{modified_text}'")
                
                # Remplacer le texte du paragraphe seulement si modifié
                if modified_text != original_text:
                    print(f"DEBUG: Paragraphe dé-anonymisé: '{original_text}' -> '{modified_text}'")
                    para.clear()
                    para.add_run(modified_text)
        
        # Traiter également les tableaux
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if para.text.strip():
                            original_text = para.text
                            modified_text = original_text
                            
                            print(f"DEBUG: Traitement cellule: '{original_text}'")
                            
                            # Appliquer chaque remplacement du mapping : tag -> valeur originale
                            # Utiliser la même logique que deanonymize_text
                            for tag in sorted_tags:
                                original_value = mapping[tag]
                                # Utiliser une expression régulière pour remplacer la balise exacte
                                pattern = re.compile(r'\b' + re.escape(tag) + r'\b')
                                before_replace = modified_text
                                modified_text = pattern.sub(original_value, modified_text)
                                if before_replace != modified_text:
                                    print(f"DEBUG: Remplacement effectué dans cellule: '{tag}' -> '{original_value}' dans '{before_replace}' -> '{modified_text}'")
                            
                            # Remplacer le texte du paragraphe seulement si modifié
                            if modified_text != original_text:
                                print(f"DEBUG: Cellule dé-anonymisée: '{original_text}' -> '{modified_text}'")
                                para.clear()
                                para.add_run(modified_text)
        
        # Sauvegarder le document modifié en bytes
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        print(f"DEBUG: Fichier dé-anonymisé généré avec succès")
        return output.getvalue()
        
    except Exception as e:
        print(f"DEBUG: Erreur dans deanonymize_docx_file: {str(e)}")
        raise Exception(f"Erreur lors de la dé-anonymisation du fichier Word: {str(e)}") 