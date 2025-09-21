"""
Modèles pour les endpoints de traitement de la parole
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SpeechAnalysisRequest(BaseModel):
    """Requête pour l'analyse de la parole"""
    audio_file: str
    expected_text: str

class SpeechAnalysisResponse(BaseModel):
    """Réponse de l'endpoint d'analyse de la parole"""
    success: bool
    transcription: str
    alignment: Dict[str, Any]
    errors: List[Dict[str, Any]]
    prosody: Dict[str, Any]
    confidence: float
