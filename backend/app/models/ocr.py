"""
Modèles pour les endpoints OCR
"""
from pydantic import BaseModel
from typing import List, Optional

class OCRRequest(BaseModel):
    """Requête pour l'analyse de texte"""
    text: str

class OCRResponse(BaseModel):
    """Réponse de l'endpoint OCR"""
    success: bool
    text: str
    paragraphs: List[str]
    confidence: float
    language: str
