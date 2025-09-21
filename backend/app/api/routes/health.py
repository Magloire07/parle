"""
Routes de santé de l'API
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.health import HealthResponse

router = APIRouter()

@router.get("/", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)):
    """Vérification de l'état de santé de l'API"""
    try:
        # Test de la base de données
        db.execute("SELECT 1")
        db_status = "healthy"
    except Exception:
        db_status = "unhealthy"
    
    return HealthResponse(
        status="healthy",
        database=db_status,
        version="1.0.0"
    )
