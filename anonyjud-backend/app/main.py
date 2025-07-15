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
from odf import text as odf_text, teletype
from odf.opendocument import load
import re # Added for regex in deanonymize_docx_file
import time

# Logs de démarrage pour diagnostic
print("🚀 Démarrage de l'application AnonyJud Backend...")
print("📝 Chargement des modules d'anonymisation...")

try:
    from .anonymizer import anonymize_text, anonymize_pdf_file, deanonymize_pdf_file, anonymize_pdf_enhanced_pipeline, deanonymize_pdf_enhanced_pipeline, anonymize_pdf_direct, deanonymize_pdf_direct, PDF_REDACTOR_AVAILABLE
    print("✓ Modules d'anonymisation de base chargés")
    print(f"📊 PDF-Redactor dans anonymizer.py: {'✓ Disponible' if PDF_REDACTOR_AVAILABLE else '❌ Non disponible'}")
except Exception as e:
    print(f"❌ Erreur lors du chargement des modules d'anonymisation de base: {e}")
    raise

try:
    from .anonymizer import anonymize_pdf_with_redactor
    print("✓ Module pdf-redactor chargé")
except Exception as e:
    print(f"⚠ Module pdf-redactor non disponible: {e}")

try:
    from .deanonymizer import deanonymize_text
    print("✓ Module de désanonymisation chargé")
except Exception as e:
    print(f"❌ Erreur lors du chargement du module de désanonymisation: {e}")
    raise

try:
    from .models import TextAnonymizationRequest, TextDeanonymizationRequest
    print("✓ Modèles Pydantic chargés")
except Exception as e:
    print(f"❌ Erreur lors du chargement des modèles: {e}")
    raise

print("🎯 Initialisation de FastAPI...")
app = FastAPI(title="AnonyJud Backend", version="1.0.0")
print("✓ FastAPI initialisé")

# Configuration CORS pour permettre les requêtes depuis le frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifier l'origine exacte
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("🌐 Configuration CORS appliquée")
print("🚀 AnonyJud Backend démarré avec succès!")
print("📊 État des modules:")
print(f"   - pdf-redactor: {'✓ Disponible' if PDF_REDACTOR_AVAILABLE else '❌ Non disponible'}")
print("🔗 API prête à recevoir les requêtes")

@app.get("/")
def read_root():
    return {
        "message": "AnonyJud API is running",
        "pdf_redactor_available": PDF_REDACTOR_AVAILABLE,
        "status": "healthy"
    }

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
    Si aucun mapping n'est fourni, tente de générer le mapping à partir des tiers.
    """
    try:
        print(f"🔍 DEANONYMIZE_TEXT_ENDPOINT - Début du traitement")
        print(f"📝 Texte reçu (premiers 200 chars): {request.anonymized_text[:200]}...")
        print(f"🗂️ Mapping reçu: {request.mapping}")
        print(f"👥 Tiers reçus: {request.tiers}")
        print(f"🔄 A mapping: {request.has_mapping}")
        
        # Si le mapping est vide, générer le mapping à partir des tiers
        if not request.has_mapping or not request.mapping or len(request.mapping) == 0:
            print(f"⚠️ Mapping vide détecté, génération à partir des tiers...")
            if request.tiers and len(request.tiers) > 0:
                mapping = generate_mapping_from_tiers(request.tiers)
                print(f"🔧 Mapping généré à partir des tiers: {mapping}")
            else:
                print(f"❌ Aucun tiers disponible pour générer le mapping")
                # Fallback: essayer de détecter automatiquement
                print(f"🔍 Tentative de détection automatique...")
                mapping = detect_anonymized_patterns(request.anonymized_text)
                print(f"🔍 Patterns détectés automatiquement: {mapping}")
                
                if not mapping:
                    print(f"❌ Aucun pattern d'anonymisation détecté")
                    return {"deanonymized_text": request.anonymized_text, "mapping": {}, "message": "Aucun pattern d'anonymisation détecté dans le texte"}
        else:
            # Utiliser le mapping fourni
            mapping = request.mapping
            print(f"✅ Utilisation du mapping fourni: {mapping}")
        
        print(f"🔄 Début de la dé-anonymisation avec mapping: {mapping}")
        deanonymized = deanonymize_text(request.anonymized_text, mapping)
        print(f"✅ Dé-anonymisation terminée avec succès")
        
        return {"deanonymized_text": deanonymized, "mapping": mapping}
        
    except Exception as e:
        print(f"❌ Erreur dans deanonymize_text_endpoint: {str(e)}")
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
            # Traitement sécurisé des fichiers PDF : pipeline PDF → Word → Anonymisation → PDF
            content = await file.read()
            anonymized_file, mapping = anonymize_pdf_enhanced_pipeline(content, tiers)
            return {"text": "PDF anonymisé via pipeline sécurisé", "mapping": mapping}
            
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

def detect_anonymized_patterns(text: str) -> Dict[str, str]:
    """
    Détecte automatiquement les patterns d'anonymisation dans un texte.
    Utilise les mêmes patterns que l'anonymisation (NOM1, PRENOM1, etc.)
    Retourne un mapping des patterns détectés.
    """
    import re
    
    print(f"🔍 DETECT_ANONYMIZED_PATTERNS - Début de la détection")
    print(f"📝 Texte à analyser (premiers 500 chars): {text[:500]}...")
    
    mapping = {}
    
    # Patterns pour détecter les champs anonymisés (même format que l'anonymisation)
    patterns = [
        (r'\bNOM(\d+)\b', 'NOM'),
        (r'\bPRENOM(\d+)\b', 'PRENOM'),
        (r'\bADRESSE(\d+)\b', 'ADRESSE'),
        (r'\bNUMERO(\d+)\b', 'NUMERO'),
        (r'\bVOIE(\d+)\b', 'VOIE'),
        (r'\bCODEPOSTAL(\d+)\b', 'CODEPOSTAL'),
        (r'\bVILLE(\d+)\b', 'VILLE'),
        (r'\bTEL(\d+)\b', 'TEL'),
        (r'\bPORTABLE(\d+)\b', 'PORTABLE'),
        (r'\bEMAIL(\d+)\b', 'EMAIL'),
        (r'\bSOCIETE(\d+)\b', 'SOCIETE'),
        (r'\bPERSO(\d+)\b', 'PERSO'),
        # Patterns génériques pour les champs personnalisés
        (r'\b([A-Z]+)(\d+)\b', 'CUSTOM'),
    ]
    
    # Chercher tous les patterns dans le texte
    for pattern, field_type in patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        print(f"🔍 Pattern '{pattern}' -> {len(matches)} correspondances trouvées")
        
        for match in matches:
            if field_type == 'CUSTOM':
                # Pour les patterns personnalisés, match est un tuple (prefix, number)
                prefix, number = match
                tag = f"{prefix.upper()}{number}"
            else:
                # Pour les patterns standards, match est juste le numéro
                number = match if isinstance(match, str) else match
                tag = f"{field_type}{number}"
            
            # Créer un mapping de base (tag -> tag pour l'instant)
            # En réalité, nous n'avons pas les valeurs originales, donc on garde les tags
            mapping[tag] = tag
            print(f"✅ Pattern détecté: '{tag}'")
    
    print(f"📊 Total des patterns détectés: {len(mapping)}")
    print(f"🗂️ Mapping généré: {mapping}")
    print(f"🏁 DETECT_ANONYMIZED_PATTERNS - Fin de la détection")
    
    return mapping

def generate_mapping_from_tiers(tiers: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Génère le mapping d'anonymisation à partir des tiers.
    Utilise la même logique que l'anonymisation pour créer les balises.
    """
    import re
    
    print(f"🔧 GENERATE_MAPPING_FROM_TIERS - Début de la génération")
    print(f"📊 Nombre de tiers reçus: {len(tiers)}")
    
    mapping = {}
    
    for tier_index, tier in enumerate(tiers):
        # Utiliser le numéro fixe du tiers ou fallback sur l'index + 1
        tier_number = tier.get("numero", tier_index + 1)
        print(f"🔍 Traitement du tiers {tier_number}: {tier}")
        
        # Traiter le nom
        if tier.get("nom"):
            nom = tier["nom"].strip()
            if nom and len(nom) > 1:
                tag = f"NOM{tier_number}"
                mapping[tag] = nom
                print(f"✅ Ajouté: {tag} -> {nom}")
        
        # Traiter le prénom
        if tier.get("prenom"):
            prenom = tier["prenom"].strip()
            if prenom and len(prenom) > 1:
                tag = f"PRENOM{tier_number}"
                mapping[tag] = prenom
                print(f"✅ Ajouté: {tag} -> {prenom}")
        
        # Traiter les composants de l'adresse
        if tier.get("adresse_numero"):
            numero = tier["adresse_numero"].strip()
            if numero and len(numero) > 0:
                tag = f"NUMERO{tier_number}"
                mapping[tag] = numero
                print(f"✅ Ajouté: {tag} -> {numero}")
        
        if tier.get("adresse_voie"):
            voie = tier["adresse_voie"].strip()
            if voie and len(voie) > 2:
                tag = f"VOIE{tier_number}"
                mapping[tag] = voie
                print(f"✅ Ajouté: {tag} -> {voie}")
        
        if tier.get("adresse_code_postal"):
            code_postal = tier["adresse_code_postal"].strip()
            if code_postal and len(code_postal) > 0:
                tag = f"CODEPOSTAL{tier_number}"
                mapping[tag] = code_postal
                print(f"✅ Ajouté: {tag} -> {code_postal}")
        
        if tier.get("adresse_ville"):
            ville = tier["adresse_ville"].strip()
            if ville and len(ville) > 1:
                tag = f"VILLE{tier_number}"
                mapping[tag] = ville
                print(f"✅ Ajouté: {tag} -> {ville}")
        
        # Traiter la ville (format simple, pour compatibilité)
        if tier.get("ville") and not tier.get("adresse_ville"):
            ville = tier["ville"].strip()
            if ville and len(ville) > 1:
                tag = f"VILLE{tier_number}"
                mapping[tag] = ville
                print(f"✅ Ajouté: {tag} -> {ville}")
        
        # Traiter l'adresse complète (compatibilité)
        if tier.get("adresse"):
            adresse = tier["adresse"].strip()
            if adresse and len(adresse) > 5:
                tag = f"ADRESSE{tier_number}"
                mapping[tag] = adresse
                print(f"✅ Ajouté: {tag} -> {adresse}")
        
        # Traiter le téléphone
        if tier.get("telephone"):
            tel = tier["telephone"].strip()
            if tel and len(tel) > 5:
                tag = f"TEL{tier_number}"
                mapping[tag] = tel
                print(f"✅ Ajouté: {tag} -> {tel}")
        
        # Traiter le portable
        if tier.get("portable"):
            portable = tier["portable"].strip()
            if portable and len(portable) > 5:
                tag = f"PORTABLE{tier_number}"
                mapping[tag] = portable
                print(f"✅ Ajouté: {tag} -> {portable}")
        
        # Traiter l'email
        if tier.get("email"):
            email = tier["email"].strip()
            if email and '@' in email:
                tag = f"EMAIL{tier_number}"
                mapping[tag] = email
                print(f"✅ Ajouté: {tag} -> {email}")
        
        # Traiter la société
        if tier.get("societe"):
            societe = tier["societe"].strip()
            if societe and len(societe) > 1:
                tag = f"SOCIETE{tier_number}"
                mapping[tag] = societe
                print(f"✅ Ajouté: {tag} -> {societe}")
        
        # Traiter les champs personnalisés
        if tier.get("customFields") and isinstance(tier["customFields"], list):
            for custom_field in tier["customFields"]:
                if isinstance(custom_field, dict):
                    champ_value = custom_field.get("value")
                    champ_label = custom_field.get("label")
                    
                    if champ_value and isinstance(champ_value, str):
                        champ_value = champ_value.strip()
                        if champ_value and len(champ_value) > 1:
                            label_base = "PERSO"
                            if champ_label and isinstance(champ_label, str):
                                label_perso = champ_label.strip()
                                if label_perso:
                                    label_base = re.sub(r'[^A-Za-z]', '', label_perso.upper())
                                    if not label_base:
                                        label_base = "PERSO"
                            
                            tag = f"{label_base}{tier_number}"
                            mapping[tag] = champ_value
                            print(f"✅ Ajouté: {tag} -> {champ_value}")
        
        # Traiter le champ personnalisé (ancien format)
        if tier.get("champPerso"):
            champ_perso = tier["champPerso"]
            if champ_perso and isinstance(champ_perso, str):
                champ_perso = champ_perso.strip()
                if champ_perso and len(champ_perso) > 1:
                    label_base = "PERSO"
                    if tier.get("labelChampPerso") and isinstance(tier["labelChampPerso"], str):
                        label_perso = tier["labelChampPerso"].strip()
                        if label_perso:
                            label_base = re.sub(r'[^A-Za-z]', '', label_perso.upper())
                            if not label_base:
                                label_base = "PERSO"
                    
                    tag = f"{label_base}{tier_number}"
                    mapping[tag] = champ_perso
                    print(f"✅ Ajouté: {tag} -> {champ_perso}")
    
    print(f"🏁 GENERATE_MAPPING_FROM_TIERS - Mapping généré avec {len(mapping)} éléments")
    print(f"🗂️ Mapping final: {mapping}")
    return mapping

@app.post("/deanonymize/file")
async def deanonymize_file(
    file: UploadFile = File(...),
    mapping_json: str = Form(...),
    tiers_json: str = Form("[]"),
    has_mapping: str = Form("true")
):
    """
    Dé-anonymise un fichier Word, PDF ou ODT en utilisant le mapping fourni.
    Si le mapping est vide, essaie de détecter automatiquement les patterns.
    """
    try:
        print(f"🚀 DEANONYMIZE_FILE ENDPOINT - Début du traitement")
        print(f"📁 Fichier reçu: {file.filename}")
        print(f"🗂️ Mapping JSON brut: {mapping_json}")
        print(f"🗂️ Tiers JSON brut: {tiers_json}")
        print(f"🔄 A mapping: {has_mapping}")
        
        # Convertir la chaîne JSON en mapping
        mapping = json.loads(mapping_json)
        tiers = json.loads(tiers_json)
        print(f"🗂️ Mapping parsé: {mapping}")
        print(f"📊 Nombre de balises dans le mapping: {len(mapping)}")
        print(f"👥 Nombre de tiers: {len(tiers)}")
        
        # Vérifier le type de fichier
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        print(f"📄 Extension du fichier: {file_extension}")
        
        # Lire le contenu du fichier
        content = await file.read()
        print(f"📦 Taille du fichier: {len(content)} bytes")
        
        # Si le mapping est vide, générer le mapping à partir des tiers
        if has_mapping.lower() == "false" or not mapping or len(mapping) == 0:
            print(f"⚠️ Mapping vide détecté, génération à partir des tiers...")
            if tiers and len(tiers) > 0:
                mapping = generate_mapping_from_tiers(tiers)
                print(f"🔧 Mapping généré à partir des tiers: {mapping}")
            else:
                print(f"❌ Aucun tiers disponible pour générer le mapping")
                # Fallback: essayer de détecter automatiquement
                print(f"🔍 Tentative de détection automatique...")
                # Extraire d'abord le texte pour détecter les patterns
                if file_extension == ".pdf":
                    with fitz.open(stream=content, filetype="pdf") as pdf:
                        text = ""
                        for page in pdf:
                            text += page.get_text()
                elif file_extension in [".doc", ".docx"]:
                    doc = Document(io.BytesIO(content))
                    text = ""
                    for para in doc.paragraphs:
                        text += para.text + "\n"
                elif file_extension == ".odt":
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".odt") as temp_file:
                        temp_file.write(content)
                        temp_path = temp_file.name
                    try:
                        doc = load(temp_path)
                        text = ""
                        for paragraph in doc.getElementsByType(odf_text.P):
                            text += teletype.extractText(paragraph) + "\n"
                    finally:
                        if os.path.exists(temp_path):
                            os.unlink(temp_path)
                else:
                    raise HTTPException(status_code=400, detail="Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.")
                
                # Détecter les patterns anonymisés automatiquement
                mapping = detect_anonymized_patterns(text)
                print(f"🔍 Patterns détectés automatiquement: {mapping}")
                
                if not mapping:
                    print(f"❌ Aucun pattern d'anonymisation détecté")
                    return {"text": text, "mapping": {}, "message": "Aucun pattern d'anonymisation détecté dans le fichier"}
        
        print(f"🔄 Début de la désanonymisation avec mapping: {mapping}")
        
        # Procéder à la dé-anonymisation
        if file_extension == ".pdf":
            print(f"📄 Traitement PDF...")
            pdf_text = extract_and_deanonymize_docx(content, mapping) # Changed to docx as per new_code
            print(f"✅ PDF désanonymisé avec succès")
            return {"text": pdf_text, "mapping": mapping}
            
        elif file_extension in [".doc", ".docx"]:
            print(f"📄 Traitement DOCX...")
            doc_text = extract_and_deanonymize_docx(content, mapping)
            print(f"✅ DOCX désanonymisé avec succès")
            return {"text": doc_text, "mapping": mapping}
            
        elif file_extension == ".odt":
            print(f"📄 Traitement ODT...")
            odt_text = extract_and_deanonymize_odt(content, mapping)
            print(f"✅ ODT désanonymisé avec succès")
            return {"text": odt_text, "mapping": mapping}
            
        else:
            raise HTTPException(status_code=400, detail="Format de fichier non supporté. Utilisez PDF, DOCX ou ODT.")
            
    except Exception as e:
        print(f"❌ Erreur dans deanonymize_file endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anonymize/file/download")
async def anonymize_file_download(
    file: UploadFile = File(...),
    tiers_json: str = Form(...)
):
    """
    Anonymise un fichier Word, ODT ou PDF et retourne le fichier modifié pour téléchargement.
    """
    try:
        print(f"🚀 ANONYMIZE_FILE_DOWNLOAD - Début du traitement")
        print(f"📁 Fichier reçu: {file.filename}")
        
        # Convertir la chaîne JSON en liste de tiers
        tiers = json.loads(tiers_json)
        print(f"👥 Nombre de tiers: {len(tiers)}")
        
        # Vérifier le type de fichier
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        print(f"📄 Extension du fichier: {file_extension}")
        
        if file_extension in [".doc", ".docx"]:
            print(f"📄 Traitement fichier Word...")
            # Traitement des fichiers Word
            content = await file.read()
            anonymized_file, mapping = anonymize_docx_file(content, tiers)
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            anonymized_filename = f"{base_name}_ANONYM.docx"
            
            print(f"✅ Fichier Word anonymisé: {anonymized_filename}")
            
            # Retourner le fichier modifié
            return StreamingResponse(
                io.BytesIO(anonymized_file),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={anonymized_filename}"}
            )
        elif file_extension == ".odt":
            print(f"📄 Traitement fichier ODT...")
            # Traitement des fichiers ODT
            content = await file.read()
            anonymized_file, mapping = anonymize_odt_file(content, tiers)
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            anonymized_filename = f"{base_name}_ANONYM.odt"
            
            print(f"✅ Fichier ODT anonymisé: {anonymized_filename}")
            
            # Retourner le fichier modifié
            return StreamingResponse(
                io.BytesIO(anonymized_file),
                media_type="application/vnd.oasis.opendocument.text",
                headers={"Content-Disposition": f"attachment; filename={anonymized_filename}"}
            )
        elif file_extension == ".pdf":
            print(f"📄 Traitement fichier PDF avec pipeline sécurisé PDF → Word → PDF...")
            content = await file.read()
            anonymized_file, mapping = anonymize_pdf_enhanced_pipeline(content, tiers)
            base_name = os.path.splitext(filename)[0]
            anonymized_filename = f"{base_name}_ANONYM.pdf"
            print(f"✅ Fichier PDF anonymisé: {anonymized_filename}")
            return StreamingResponse(
                io.BytesIO(anonymized_file),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={anonymized_filename}"}
            )
        else:
            print(f"❌ Format de fichier non supporté: {file_extension}")
            raise HTTPException(status_code=400, detail="Seuls les fichiers Word (.docx), ODT (.odt) et PDF (.pdf) sont supportés pour le téléchargement.")
        
    except Exception as e:
        print(f"❌ Erreur dans anonymize_file_download: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/deanonymize/file/download")
async def deanonymize_file_download(
    file: UploadFile = File(...),
    mapping_json: str = Form(...)
):
    """
    Dé-anonymise un fichier Word, ODT ou PDF et retourne le fichier modifié pour téléchargement.
    """
    try:
        print(f"🚀 DEANONYMIZE_FILE_DOWNLOAD - Début du traitement")
        print(f"📁 Fichier reçu: {file.filename}")
        
        # Convertir la chaîne JSON en mapping
        mapping = json.loads(mapping_json)
        print(f"🗂️ Mapping reçu: {mapping}")
        print(f"📊 Nombre de balises dans le mapping: {len(mapping)}")
        
        # Vérifier le type de fichier
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        print(f"📄 Extension du fichier: {file_extension}")
        
        if file_extension in [".doc", ".docx"]:
            print(f"📄 Traitement fichier Word...")
            # Traitement des fichiers Word
            content = await file.read()
            deanonymized_file = deanonymize_docx_file(content, mapping)
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            # Retirer "_ANONYM" du nom si présent
            if base_name.endswith("_ANONYM"):
                base_name = base_name[:-7]
            deanonymized_filename = f"{base_name}_DESANONYM.docx"
            
            print(f"✅ Fichier Word dé-anonymisé: {deanonymized_filename}")
            
            # Retourner le fichier modifié
            return StreamingResponse(
                io.BytesIO(deanonymized_file),
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                headers={"Content-Disposition": f"attachment; filename={deanonymized_filename}"}
            )
        elif file_extension == ".odt":
            print(f"📄 Traitement fichier ODT...")
            # Traitement des fichiers ODT
            content = await file.read()
            deanonymized_file = deanonymize_odt_file(content, mapping)
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            # Retirer "_ANONYM" du nom si présent
            if base_name.endswith("_ANONYM"):
                base_name = base_name[:-7]
            deanonymized_filename = f"{base_name}_DESANONYM.odt"
            
            print(f"✅ Fichier ODT dé-anonymisé: {deanonymized_filename}")
            
            # Retourner le fichier modifié
            return StreamingResponse(
                io.BytesIO(deanonymized_file),
                media_type="application/vnd.oasis.opendocument.text",
                headers={"Content-Disposition": f"attachment; filename={deanonymized_filename}"}
            )
        elif file_extension == ".pdf":
            print(f"📄 Traitement fichier PDF avec pipeline sécurisé PDF → Word → PDF...")
            content = await file.read()
            deanonymized_file = deanonymize_pdf_enhanced_pipeline(content, mapping)
            base_name = os.path.splitext(filename)[0]
            if base_name.endswith("_ANONYM"):
                base_name = base_name[:-7]
            deanonymized_filename = f"{base_name}_DESANONYM.pdf"
            print(f"✅ Fichier PDF dé-anonymisé: {deanonymized_filename}")
            return StreamingResponse(
                io.BytesIO(deanonymized_file),
                media_type="application/pdf",
                headers={"Content-Disposition": f"attachment; filename={deanonymized_filename}"}
            )
        else:
            print(f"❌ Format de fichier non supporté: {file_extension}")
            raise HTTPException(status_code=400, detail="Seuls les fichiers Word (.docx), ODT (.odt) et PDF (.pdf) sont supportés pour le téléchargement.")
            
    except Exception as e:
        print(f"❌ Erreur dans deanonymize_file_download: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anonymize/pdf/redactor")
async def anonymize_pdf_with_redactor_endpoint(
    file: UploadFile = File(...),
    tiers_json: str = Form(...)
):
    """
    Anonymise un fichier PDF avec pdf-redactor pour une préservation optimale de la mise en page.
    Cette méthode est spécialement conçue pour conserver parfaitement le formatage original.
    """
    try:
        print(f"🚀 ANONYMIZE_PDF_REDACTOR - Début du traitement")
        
        # Vérifier que le module pdf-redactor est disponible
        if not PDF_REDACTOR_AVAILABLE:
            print(f"❌ Module pdf-redactor non disponible")
            raise HTTPException(
                status_code=503, 
                detail="Le module pdf-redactor n'est pas disponible sur ce serveur. Utilisez l'endpoint /anonymize/pdf/auto à la place."
            )
        
        print(f"📁 Fichier reçu: {file.filename}")
        
        # Vérifier que c'est bien un PDF
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension != ".pdf":
            raise HTTPException(status_code=400, detail="Cet endpoint ne supporte que les fichiers PDF (.pdf)")
        
        # Convertir la chaîne JSON en liste de tiers
        tiers = json.loads(tiers_json)
        print(f"👥 Nombre de tiers: {len(tiers)}")
        
        # Lire le contenu du fichier PDF
        content = await file.read()
        print(f"📦 Taille du fichier: {len(content)} bytes")
        
        # Anonymiser avec pdf-redactor
        print(f"🔄 Anonymisation avec pdf-redactor...")
        anonymized_pdf, mapping = anonymize_pdf_with_redactor(content, tiers)
        
        print(f"✅ Anonymisation pdf-redactor réussie!")
        print(f"📊 Taille original: {len(content)} bytes")
        print(f"📊 Taille anonymisé: {len(anonymized_pdf)} bytes")
        print(f"📊 Mapping généré: {len(mapping)} remplacements")
        
        # Créer un nom de fichier pour le téléchargement
        base_name = os.path.splitext(filename)[0]
        anonymized_filename = f"{base_name}_REDACTOR_ANONYM.pdf"
        
        print(f"💾 Fichier prêt pour téléchargement: {anonymized_filename}")
        
        # Retourner le fichier anonymisé pour téléchargement
        return StreamingResponse(
            io.BytesIO(anonymized_pdf),
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename={anonymized_filename}"}
        )
        
    except Exception as e:
        print(f"❌ Erreur dans anonymize_pdf_with_redactor_endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/anonymize/pdf/auto")
async def anonymize_pdf_auto_method(
    file: UploadFile = File(...),
    tiers_json: str = Form(...),
    force_method: str = Form(default="auto")
):
    """
    Anonymise un PDF en choisissant automatiquement la meilleure méthode selon la taille.
    
    force_method peut être: "auto", "redactor", "pipeline", "direct"
    - auto: choix automatique selon la taille (recommandé)
    - redactor: force l'utilisation de pdf-redactor
    - pipeline: force l'utilisation du pipeline PDF→Word→PDF  
    - direct: force l'utilisation de PyMuPDF direct
    """
    try:
        print(f"🚀 ANONYMIZE_PDF_AUTO - Début du traitement")
        print(f"📁 Fichier reçu: {file.filename}")
        print(f"🔧 Méthode forcée: {force_method}")
        
        # Vérifier que c'est bien un PDF
        filename = file.filename or ""
        file_extension = os.path.splitext(filename)[1].lower()
        
        if file_extension != ".pdf":
            raise HTTPException(status_code=400, detail="Cet endpoint ne supporte que les fichiers PDF (.pdf)")
        
        # Convertir la chaîne JSON en liste de tiers
        tiers = json.loads(tiers_json)
        print(f"👥 Nombre de tiers: {len(tiers)}")
        
        # Lire le contenu du fichier PDF
        content = await file.read()
        file_size_mb = len(content) / 1024 / 1024
        
        print(f"📦 Taille du fichier: {len(content):,} bytes ({file_size_mb:.1f} MB)")
        
        # === CHOIX AUTOMATIQUE DE LA MÉTHODE ===
        chosen_method = force_method
        method_reason = ""
        
        if force_method == "auto":
            if file_size_mb > 4000:  # > 4GB
                raise HTTPException(status_code=413, 
                    detail=f"Fichier trop volumineux: {file_size_mb:.1f}MB > 4GB. "
                           f"Segmentez le fichier en parties plus petites.")
            elif file_size_mb > 1000:  # > 1GB 
                if PDF_REDACTOR_AVAILABLE:
                    chosen_method = "redactor"
                    method_reason = "Fichier > 1GB: pdf-redactor recommandé (plus direct)"
                else:
                    chosen_method = "direct"
                    method_reason = "Fichier > 1GB: PyMuPDF direct (pdf-redactor non disponible)"
            elif file_size_mb > 500:  # > 500MB
                if PDF_REDACTOR_AVAILABLE:
                    chosen_method = "redactor" 
                    method_reason = "Fichier > 500MB: pdf-redactor recommandé (évite conversions)"
                else:
                    chosen_method = "direct"
                    method_reason = "Fichier > 500MB: PyMuPDF direct (pdf-redactor non disponible)"
            elif file_size_mb > 100:  # > 100MB
                chosen_method = "pipeline"
                method_reason = "Fichier > 100MB: pipeline Word recommandé (équilibre qualité/performance)"
            else:  # <= 100MB
                if PDF_REDACTOR_AVAILABLE:
                    chosen_method = "redactor"
                    method_reason = "Fichier petit: pdf-redactor recommandé (plus rapide et préserve mieux)"
                else:
                    chosen_method = "pipeline"
                    method_reason = "Fichier petit: pipeline Word (pdf-redactor non disponible)"
        else:
            method_reason = f"Méthode forcée par l'utilisateur: {force_method}"
        
        print(f"🎯 Méthode choisie: {chosen_method}")
        print(f"📝 Raison: {method_reason}")
        
        # === EXÉCUTION DE LA MÉTHODE CHOISIE ===
        start_time = time.time()
        
        try:
            if chosen_method == "redactor":
                if not PDF_REDACTOR_AVAILABLE:
                    print(f"⚠ pdf-redactor demandé mais non disponible, basculement vers pipeline")
                    chosen_method = "pipeline"
                    method_reason += " → Basculé vers pipeline (pdf-redactor non disponible)"
                    anonymized_pdf, mapping = anonymize_pdf_enhanced_pipeline(content, tiers)
                    method_suffix = "PIPELINE"
                else:
                    print(f"🔄 Anonymisation avec pdf-redactor...")
                    anonymized_pdf, mapping = anonymize_pdf_with_redactor(content, tiers)
                    method_suffix = "REDACTOR"
                
            elif chosen_method == "pipeline":
                print(f"🔄 Anonymisation avec pipeline PDF→Word→PDF...")
                anonymized_pdf, mapping = anonymize_pdf_enhanced_pipeline(content, tiers)
                method_suffix = "PIPELINE"
                
            elif chosen_method == "direct":
                print(f"🔄 Anonymisation directe avec PyMuPDF...")
                anonymized_pdf, mapping = anonymize_pdf_direct(content, tiers)
                method_suffix = "DIRECT"
                
            else:
                raise HTTPException(status_code=400, 
                    detail=f"Méthode inconnue: {chosen_method}. "
                           f"Valeurs acceptées: auto, redactor, pipeline, direct")
            
            processing_time = time.time() - start_time
            
            print(f"✅ Anonymisation {chosen_method} réussie en {processing_time:.2f}s!")
            print(f"📊 Taille original: {len(content):,} bytes ({file_size_mb:.1f} MB)")
            print(f"📊 Taille anonymisé: {len(anonymized_pdf):,} bytes ({len(anonymized_pdf)/1024/1024:.1f} MB)")
            print(f"📊 Mapping généré: {len(mapping)} remplacements")
            print(f"🎯 Méthode utilisée: {chosen_method} - {method_reason}")
            
            # Créer un nom de fichier pour le téléchargement
            base_name = os.path.splitext(filename)[0]
            anonymized_filename = f"{base_name}_{method_suffix}_ANONYM.pdf"
            
            print(f"💾 Fichier prêt pour téléchargement: {anonymized_filename}")
            
            # Retourner le fichier anonymisé pour téléchargement
            return StreamingResponse(
                io.BytesIO(anonymized_pdf),
                media_type="application/pdf",
                headers={
                    "Content-Disposition": f"attachment; filename={anonymized_filename}",
                    "X-Method-Used": chosen_method,
                    "X-Method-Reason": method_reason,
                    "X-Processing-Time": f"{processing_time:.2f}s",
                    "X-File-Size-MB": f"{file_size_mb:.1f}",
                    "X-Mapping-Count": str(len(mapping))
                }
            )
            
        except Exception as method_error:
            processing_time = time.time() - start_time
            print(f"❌ Échec méthode {chosen_method} après {processing_time:.2f}s: {str(method_error)}")
            
            # Si méthode auto et échec, essayer une méthode alternative
            if force_method == "auto" and chosen_method != "pipeline":
                print(f"🔄 Tentative de fallback vers pipeline PDF→Word→PDF...")
                try:
                    fallback_start = time.time()
                    anonymized_pdf, mapping = anonymize_pdf_enhanced_pipeline(content, tiers)
                    fallback_time = time.time() - fallback_start
                    
                    print(f"✅ Fallback pipeline réussi en {fallback_time:.2f}s!")
                    
                    base_name = os.path.splitext(filename)[0]
                    anonymized_filename = f"{base_name}_PIPELINE_FALLBACK_ANONYM.pdf"
                    
                    return StreamingResponse(
                        io.BytesIO(anonymized_pdf),
                        media_type="application/pdf",
                        headers={
                            "Content-Disposition": f"attachment; filename={anonymized_filename}",
                            "X-Method-Used": "pipeline-fallback",
                            "X-Method-Reason": f"Fallback après échec {chosen_method}",
                            "X-Processing-Time": f"{fallback_time:.2f}s",
                            "X-Original-Error": str(method_error)[:100]
                        }
                    )
                except Exception as fallback_error:
                    print(f"❌ Échec fallback pipeline: {str(fallback_error)}")
                    raise HTTPException(status_code=500, 
                        detail=f"Échec méthode {chosen_method}: {str(method_error)}. "
                               f"Échec fallback pipeline: {str(fallback_error)}")
            else:
                raise HTTPException(status_code=500, detail=str(method_error))
        
    except HTTPException:
        raise  # Re-raise HTTP exceptions
    except Exception as e:
        print(f"❌ Erreur générale dans anonymize_pdf_auto_method: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

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
    Préserve le formatage (police, style, majuscules/minuscules, mise en page).
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
        
        # Fonction pour anonymiser un run en préservant son formatage
        def anonymize_run_preserving_format(run, mapping):
            """Anonymise le texte d'un run en préservant son formatage"""
            if not run.text:
                return
                
            original_text = run.text
            modified_text = original_text
            
            # Appliquer chaque remplacement du mapping (inverser pour que les tags remplacent les originaux)
            for tag, original_value in mapping.items():
                if original_value in modified_text:
                    # Préserver la casse du texte original
                    if original_value.isupper():
                        modified_text = modified_text.replace(original_value, tag.upper())
                    elif original_value.islower():
                        modified_text = modified_text.replace(original_value, tag.lower())
                    elif original_value.istitle():
                        modified_text = modified_text.replace(original_value, tag.title())
                    else:
                        modified_text = modified_text.replace(original_value, tag)
            
            # Remplacer le texte du run seulement si modifié (le formatage est automatiquement préservé)
            if modified_text != original_text:
                print(f"DEBUG: Run modifié: '{original_text}' -> '{modified_text}'")
                run.text = modified_text
        
        # Appliquer les anonymisations directement dans le document en préservant le formatage
        paragraphs_processed = 0
        for para in doc.paragraphs:
            if para.text.strip():  # Seulement pour les paragraphes non vides
                # Traiter chaque run individuellement pour préserver le formatage
                for run in para.runs:
                    anonymize_run_preserving_format(run, mapping)
                paragraphs_processed += 1
        
        # Traiter également les tableaux
        cells_processed = 0
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if para.text.strip():
                            # Traiter chaque run individuellement pour préserver le formatage
                            for run in para.runs:
                                anonymize_run_preserving_format(run, mapping)
                            cells_processed += 1
        
        print(f"DEBUG: Traitement terminé - {paragraphs_processed} paragraphes, {cells_processed} cellules")
        
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
    Préserve le formatage (police, style, majuscules/minuscules, mise en page).
    Retourne le fichier modifié.
    """
    try:
        print(f"🔍 DEANONYMIZE_DOCX_FILE - Début du processus")
        print(f"🗂️ Mapping reçu: {mapping}")
        print(f"📊 Nombre de balises dans le mapping: {len(mapping)}")
        
        # Ouvrir le document Word depuis les bytes
        doc = Document(io.BytesIO(content))
        
        # Extraire tout le texte du document pour analyse
        full_text = ""
        for para in doc.paragraphs:
            full_text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        full_text += para.text + "\n"
        
        print(f"📝 Texte extrait du document (premiers 300 chars): {full_text[:300]}...")
        
        # Analyser quelles balises sont présentes dans le texte
        found_tags = []
        for tag in mapping.keys():
            if tag in full_text:
                found_tags.append(tag)
                print(f"✅ Balise '{tag}' trouvée dans le document")
            else:
                print(f"❌ Balise '{tag}' NON trouvée dans le document")
        
        print(f"📋 Résumé: {len(found_tags)}/{len(mapping)} balises trouvées: {found_tags}")
        
        # Le mapping est déjà dans le bon sens (balise -> valeur_originale)
        # Pas besoin d'inverser car generate_mapping_from_tiers() crée déjà le mapping correct
        print(f"🔄 Mapping reçu (balise -> valeur): {mapping}")
        
        # Vérifier si le mapping est dans le bon sens
        sample_key = list(mapping.keys())[0] if mapping else ""
        if sample_key and not sample_key.isupper():
            # Le mapping semble être dans le mauvais sens (valeur -> balise), l'inverser
            reverse_mapping = {v: k for k, v in mapping.items()}
            print(f"🔄 Mapping inversé car dans le mauvais sens: {reverse_mapping}")
        else:
            # Le mapping est dans le bon sens (balise -> valeur)
            reverse_mapping = mapping
            print(f"🔄 Mapping utilisé tel quel: {reverse_mapping}")
        
        # Trier les balises par longueur décroissante pour éviter les remplacements partiels
        sorted_tags = sorted(reverse_mapping.keys(), key=len, reverse=True)
        print(f"🔢 Balises triées par longueur: {sorted_tags}")
        
        # Fonction pour dé-anonymiser un run en préservant son formatage
        def deanonymize_run_preserving_format(run, mapping, sorted_tags):
            """Dé-anonymise le texte d'un run en préservant son formatage"""
            if not run.text:
                return False
                
            original_text = run.text
            modified_text = original_text
            has_changes = False
            
            # Appliquer chaque remplacement du mapping (balise -> valeur originale)
            for balise in sorted_tags:
                valeur_originale = mapping[balise]
                
                # Chercher la balise dans toutes les variantes de casse possibles
                balise_variants = [
                    balise,           # PRENOM1
                    balise.lower(),   # prenom1
                    balise.title(),   # Prenom1
                    balise.capitalize() # Prenom1 (même résultat que title pour ce cas)
                ]
                
                for variant in balise_variants:
                    if variant in modified_text:
                        count_before = modified_text.count(variant)
                        
                        # Utiliser une expression régulière pour remplacer la balise exacte (pas de remplacement partiel)
                        pattern = re.compile(r'\b' + re.escape(variant) + r'\b')
                        modified_text_new = pattern.sub(valeur_originale, modified_text)
                        
                        count_after = modified_text_new.count(variant)
                        actual_replacements = count_before - count_after
                        
                        if actual_replacements > 0:
                            print(f"✅ Run: {actual_replacements} occurrence(s) de '{variant}' remplacée(s) par '{valeur_originale}'")
                            modified_text = modified_text_new
                            has_changes = True
                            break  # Sortir de la boucle des variants une fois qu'on a trouvé et remplacé
                        else:
                            print(f"⚠️ Run: Aucun remplacement de mot entier pour '{variant}', tentative de remplacement simple")
                            # Fallback: remplacement simple si le pattern de mot entier ne fonctionne pas
                            if variant in modified_text:
                                modified_text = modified_text.replace(variant, valeur_originale)
                                print(f"🔄 Run: Remplacement simple effectué pour '{variant}'")
                                has_changes = True
                                break  # Sortir de la boucle des variants
            
            # Remplacer le texte du run seulement si modifié (le formatage est automatiquement préservé)
            if has_changes:
                print(f"📝 Run modifié: '{original_text}' -> '{modified_text}'")
                run.text = modified_text
            
            return has_changes
        
        paragraphs_modified = 0
        runs_modified = 0
        
        # Appliquer les dé-anonymisations dans les paragraphes
        for i, para in enumerate(doc.paragraphs):
            if para.text.strip():  # Seulement pour les paragraphes non vides
                para_has_changes = False
                # Traiter chaque run individuellement pour préserver le formatage
                for run in para.runs:
                    if deanonymize_run_preserving_format(run, reverse_mapping, sorted_tags):
                        runs_modified += 1
                        para_has_changes = True
                
                if para_has_changes:
                    paragraphs_modified += 1
        
        # Traiter également les tableaux
        cells_modified = 0
        for table_idx, table in enumerate(doc.tables):
            for row_idx, row in enumerate(table.rows):
                for cell_idx, cell in enumerate(row.cells):
                    for para_idx, para in enumerate(cell.paragraphs):
                        if para.text.strip():
                            cell_has_changes = False
                            # Traiter chaque run individuellement pour préserver le formatage
                            for run in para.runs:
                                if deanonymize_run_preserving_format(run, reverse_mapping, sorted_tags):
                                    runs_modified += 1
                                    cell_has_changes = True
                            
                            if cell_has_changes:
                                cells_modified += 1
        
        print(f"📈 Résultats: {paragraphs_modified} paragraphes, {cells_modified} cellules, {runs_modified} runs modifiés")
        
        # Sauvegarder le document modifié en bytes
        output = io.BytesIO()
        doc.save(output)
        output.seek(0)
        
        print(f"🏁 DEANONYMIZE_DOCX_FILE - Fichier modifié généré avec succès")
        return output.getvalue()
        
    except Exception as e:
        print(f"❌ Erreur dans deanonymize_docx_file: {str(e)}")
        raise Exception(f"Erreur lors de la dé-anonymisation du fichier Word: {str(e)}")

def extract_and_deanonymize_docx(content: bytes, mapping: Dict[str, str]):
    """
    Extrait le texte d'un document Word et le dé-anonymise.
    """
    try:
        print(f"🔍 EXTRACT_AND_DEANONYMIZE_DOCX - Début du processus")
        print(f"🗂️ Mapping reçu: {mapping}")
        
        # Ouvrir le document Word depuis les bytes
        doc = Document(io.BytesIO(content))
        text = ""
        
        # Extraire le texte de chaque paragraphe
        paragraph_count = 0
        for para in doc.paragraphs:
            if para.text.strip():
                text += para.text + "\n"
                paragraph_count += 1
        
        # Extraire le texte des tableaux aussi
        table_count = 0
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    for para in cell.paragraphs:
                        if para.text.strip():
                            text += para.text + "\n"
                            table_count += 1
        
        print(f"📝 Texte extrait: {paragraph_count} paragraphes, {table_count} cellules de tableau")
        print(f"📝 Texte complet (premiers 300 chars): {text[:300]}...")
        print(f"📊 Longueur totale du texte: {len(text)} caractères")
            
        # Dé-anonymiser le texte extrait
        print(f"🔄 Appel de deanonymize_text...")
        deanonymized = deanonymize_text(text, mapping)
        print(f"✅ Désanonymisation terminée")
        
        return deanonymized
        
    except Exception as e:
        print(f"❌ Erreur dans extract_and_deanonymize_docx: {str(e)}")
        raise Exception(f"Erreur lors du traitement du document Word: {str(e)}")

def extract_and_deanonymize_odt(content: bytes, mapping: Dict[str, str]):
    """
    Extrait le texte d'un document OpenDocument Text (ODT) et le dé-anonymise.
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
            
            # Dé-anonymiser le texte extrait
            deanonymized = deanonymize_text(text, mapping)
            
            return deanonymized
            
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        raise Exception(f"Erreur lors du traitement du document ODT: {str(e)}") 

def anonymize_odt_file(content: bytes, tiers: List[Dict[str, Any]]):
    """
    Anonymise directement un fichier ODT en modifiant son contenu.
    Préserve le formatage et retourne le fichier modifié et le mapping d'anonymisation.
    """
    try:
        print(f"🚀 DEBUG: Début anonymize_odt_file avec {len(tiers)} tiers")
        
        # Créer un fichier temporaire pour stocker le contenu ODT
        with tempfile.NamedTemporaryFile(delete=False, suffix=".odt") as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Charger le document ODT
            doc = load(temp_path)
            
            # Collecter tout le texte du document
            full_text = ""
            for paragraph in doc.getElementsByType(odf_text.P):
                full_text += teletype.extractText(paragraph) + "\n"
            
            print(f"📝 DEBUG: Texte extrait (premiers 200 chars): {full_text[:200]}...")
            
            # Anonymiser le texte complet pour obtenir le mapping
            anonymized_text, mapping = anonymize_text(full_text, tiers)
            
            print(f"🗂️ DEBUG: Mapping généré: {mapping}")
            print(f"📝 DEBUG: Texte anonymisé (premiers 200 chars): {anonymized_text[:200]}...")
            
            # Appliquer l'anonymisation au document ODT
            paragraphs_processed = 0
            for paragraph in doc.getElementsByType(odf_text.P):
                paragraph_text = teletype.extractText(paragraph)
                if paragraph_text.strip():
                    # Anonymiser le texte du paragraphe
                    anonymized_paragraph = anonymize_text(paragraph_text, tiers)[0]
                    
                    # Remplacer le contenu du paragraphe de manière sécurisée
                    try:
                        # Vider le paragraphe
                        paragraph.childNodes = []
                        # Ajouter le texte anonymisé
                        paragraph.addText(anonymized_paragraph)
                        paragraphs_processed += 1
                    except Exception as e:
                        print(f"⚠️ DEBUG: Erreur lors du traitement du paragraphe: {str(e)}")
                        # Continuer avec le paragraphe suivant
                        continue
            
            print(f"📊 DEBUG: Traitement terminé - {paragraphs_processed} paragraphes")
            
            # Sauvegarder le document modifié
            output_path = temp_path + "_anonym"
            doc.save(output_path)
            
            # Lire le fichier anonymisé
            with open(output_path, 'rb') as f:
                anonymized_file_content = f.read()
            
            # Nettoyer les fichiers temporaires
            if os.path.exists(output_path):
                os.unlink(output_path)
            
            print(f"✅ DEBUG: Fichier ODT anonymisé généré avec succès")
            return anonymized_file_content, mapping
            
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"❌ DEBUG: Erreur dans anonymize_odt_file: {str(e)}")
        raise Exception(f"Erreur lors de l'anonymisation du fichier ODT: {str(e)}")

def deanonymize_odt_file(content: bytes, mapping: Dict[str, str]):
    """
    Dé-anonymise directement un fichier ODT en utilisant le mapping fourni.
    Préserve le formatage et retourne le fichier modifié.
    """
    try:
        print(f"🚀 DEBUG: Début deanonymize_odt_file")
        print(f"🗂️ DEBUG: Mapping reçu: {mapping}")
        print(f"📊 DEBUG: Nombre de balises dans le mapping: {len(mapping)}")
        
        # Créer un fichier temporaire pour stocker le contenu ODT
        with tempfile.NamedTemporaryFile(delete=False, suffix=".odt") as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name
        
        try:
            # Charger le document ODT
            doc = load(temp_path)
            
            # Extraire tout le texte du document pour analyse
            full_text = ""
            for paragraph in doc.getElementsByType(odf_text.P):
                full_text += teletype.extractText(paragraph) + "\n"
            
            print(f"📝 DEBUG: Texte extrait (premiers 300 chars): {full_text[:300]}...")
            
            # Analyser quelles balises sont présentes dans le texte
            found_tags = []
            for tag in mapping.keys():
                if tag in full_text:
                    found_tags.append(tag)
                    print(f"✅ DEBUG: Balise '{tag}' trouvée dans le document")
                else:
                    print(f"❌ DEBUG: Balise '{tag}' NON trouvée dans le document")
            
            print(f"📋 DEBUG: Résumé: {len(found_tags)}/{len(mapping)} balises trouvées: {found_tags}")
            
            # Appliquer la dé-anonymisation au document ODT
            paragraphs_processed = 0
            for paragraph in doc.getElementsByType(odf_text.P):
                paragraph_text = teletype.extractText(paragraph)
                if paragraph_text.strip():
                    # Dé-anonymiser le texte du paragraphe
                    deanonymized_paragraph = deanonymize_text(paragraph_text, mapping)
                    
                    # Si le texte a changé, le remplacer
                    if deanonymized_paragraph != paragraph_text:
                        try:
                            # Vider le paragraphe
                            paragraph.childNodes = []
                            # Ajouter le texte dé-anonymisé
                            paragraph.addText(deanonymized_paragraph)
                            paragraphs_processed += 1
                        except Exception as e:
                            print(f"⚠️ DEBUG: Erreur lors du traitement du paragraphe: {str(e)}")
                            # Continuer avec le paragraphe suivant
                            continue
            
            print(f"📊 DEBUG: Traitement terminé - {paragraphs_processed} paragraphes modifiés")
            
            # Sauvegarder le document modifié
            output_path = temp_path + "_deanonym"
            doc.save(output_path)
            
            # Lire le fichier dé-anonymisé
            with open(output_path, 'rb') as f:
                deanonymized_file_content = f.read()
            
            # Nettoyer les fichiers temporaires
            if os.path.exists(output_path):
                os.unlink(output_path)
            
            print(f"✅ DEBUG: Fichier ODT dé-anonymisé généré avec succès")
            return deanonymized_file_content
            
        finally:
            # Supprimer le fichier temporaire
            if os.path.exists(temp_path):
                os.unlink(temp_path)
        
    except Exception as e:
        print(f"❌ DEBUG: Erreur dans deanonymize_odt_file: {str(e)}")
        raise Exception(f"Erreur lors de la dé-anonymisation du fichier ODT: {str(e)}") 