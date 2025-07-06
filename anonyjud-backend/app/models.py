# Modèles de données pour la gestion des projets, historiques, mappings

from pydantic import BaseModel
from typing import Dict, List, Any, Optional

class Projet:
    """
    Représente un projet d'expertise avec base de correspondance, historique, etc.
    """
    def __init__(self, nom, mot_de_passe):
        self.nom = nom
        self.mot_de_passe = mot_de_passe
        self.mapping = {}
        self.historique = []

class TextAnonymizationRequest(BaseModel):
    """
    Modèle pour la requête d'anonymisation de texte.
    """
    text: str
    tiers: List[Dict[str, Any]] = []

class TextDeanonymizationRequest(BaseModel):
    """
    Modèle pour la requête de dé-anonymisation de texte.
    """
    anonymized_text: str
    mapping: Dict[str, str] 