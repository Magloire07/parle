"""
Modèles pour les endpoints de santé
"""
from pydantic import BaseModel

class HealthResponse(BaseModel):
    """Réponse de l'endpoint de santé"""
    status: str
    database: str
    version: str
