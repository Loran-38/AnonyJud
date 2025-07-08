from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Any, Optional
import json
import os
import tempfile
from pathlib import Path
import fitz  # PyMuPDF pour les PDF
from docx import Document  # python-docx pour les fichiers Word
import io
from odf import text as odf_text, teletype
from odf.opendocument import load
import time
import logging

from .anonymizer import anonymize_text
from .deanonymizer import deanonymize_text
from .models import TextAnonymizationRequest, TextDeanonymizationRequest

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration FastAPI optimisée
app = FastAPI(
    title="AnonyJud API",
    description="API d'anonymisation de documents juridiques",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier l'origine exacte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Variables globales pour le monitoring
startup_time = time.time()

@app.on_event("startup")
async def startup_event():
    """Événement de démarrage pour initialiser l'application"""
    global startup_time
    startup_time = time.time()
    logger.info("🚀 AnonyJud API démarrée avec succès")

@app.get("/")
def read_root():
    """Endpoint racine"""
    return {
        "message": "AnonyJud API is running",
        "version": "1.0.0",
        "status": "healthy",
        "uptime": time.time() - startup_time
    }

@app.get("/health")
def health_check():
    """Endpoint de healthcheck pour Railway"""
    try:
        uptime = time.time() - startup_time
        return JSONResponse(
            status_code=200,
            content={
                "status": "healthy",
                "service": "anonyjud-backend",
                "version": "1.0.0",
                "uptime": uptime,
                "timestamp": time.time()
            }
        )
    except Exception as e:
        logger.error(f"Erreur healthcheck: {e}")
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "error": str(e),
                "timestamp": time.time()
            }
        )

@app.get("/status")
def get_status():
    """Endpoint de statut détaillé"""
    return {
        "service": "anonyjud-backend",
        "status": "running",
        "version": "1.0.0",
        "uptime": time.time() - startup_time,
        "features": {
            "text_anonymization": True,
            "file_anonymization": True,
            "deanonymization": True,
            "supported_formats": ["pdf", "docx", "odt"]
        }
    }

@app.post("/anonymize/text")
async def anonymize_text_endpoint(request: TextAnonymizationRequest):
    """Endpoint pour anonymiser du texte"""
    try:
        logger.info(f"Anonymisation de texte demandée - {len(request.text)} caractères")
        start_time = time.time()
        
        anonymized_text, mapping = anonymize_text(request.text, request.tiers)
        
        processing_time = time.time() - start_time
        logger.info(f"Anonymisation terminée en {processing_time:.2f}s")
        
        return {
            "anonymized_text": anonymized_text,
            "mapping": mapping,
            "processing_time": processing_time,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Erreur lors de l'anonymisation: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de l'anonymisation: {str(e)}")

@app.post("/deanonymize/text")
async def deanonymize_text_endpoint(request: TextDeanonymizationRequest):
    """Endpoint pour dé-anonymiser du texte"""
    try:
        logger.info(f"Dé-anonymisation de texte demandée - {len(request.anonymized_text)} caractères")
        start_time = time.time()
        
        result = deanonymize_text(request.anonymized_text, request.mapping)
        
        processing_time = time.time() - start_time
        logger.info(f"Dé-anonymisation terminée en {processing_time:.2f}s")
        
        return {
            "deanonymized_text": result,
            "processing_time": processing_time,
            "status": "success"
        }
    except Exception as e:
        logger.error(f"Erreur lors de la dé-anonymisation: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur lors de la dé-anonymisation: {str(e)}")

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
                text += page.get_text() if hasattr(page, 'get_text') else ""
        
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