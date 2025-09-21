"""
Modèles pour les endpoints de synthèse vocale
"""
from pydantic import BaseModel
from typing import Optional

class TTSRequest(BaseModel):
    """Requête pour la génération de parole"""
    text: str
    language: str = "fr"
    slow: bool = False
    duration: Optional[float] = None

class TTSResponse(BaseModel):
    """Réponse de l'endpoint TTS"""
    success: bool
    audio_url: str
    duration: Optional[float]
    language: str
