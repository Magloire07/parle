"""
Modèles pour les endpoints d'évaluation des résumés
"""
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class SummaryEvaluationRequest(BaseModel):
    """Requête pour l'évaluation de résumé"""
    source_text: str

class LLMEvaluationRequest(BaseModel):
    """Requête d'évaluation LLM détaillée (sépare texte source et résumé)."""
    source_text: str
    summary_text: str

class SummaryEvaluationResponse(BaseModel):
    """Réponse de l'endpoint d'évaluation de résumé"""
    success: bool
    transcription: str
    relevance_score: float
    quality_score: float
    suggestions: List[str]
    errors: List[Dict[str, Any]]
    transitions: List[str]
