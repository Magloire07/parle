"""
Routes pour la progression
"""
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.progress import Progress
from app.schemas import ProgressCreate, ProgressUpdate, ProgressResponse

router = APIRouter()

@router.post("/", response_model=ProgressResponse, status_code=status.HTTP_201_CREATED)
async def create_progress(
    progress: ProgressCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Créer une entrée de progression"""
    db_progress = Progress(
        **progress.model_dump(),
        user_id=current_user.id
    )
    db.add(db_progress)
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.get("/", response_model=List[ProgressResponse])
async def get_progress(
    language: str = Query(None, pattern="^(en|fr)$"),
    start_date: datetime = Query(None),
    end_date: datetime = Query(None),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer les entrées de progression de l'utilisateur"""
    query = db.query(Progress).filter(Progress.user_id == current_user.id)
    
    if language:
        query = query.filter(Progress.language == language)
    if start_date:
        query = query.filter(Progress.date >= start_date)
    if end_date:
        query = query.filter(Progress.date <= end_date)
    
    progress = query.order_by(Progress.date.desc()).offset(skip).limit(limit).all()
    return progress

@router.get("/stats")
async def get_progress_stats(
    language: str = Query(None, pattern="^(en|fr)$"),
    days: int = Query(7, ge=1, le=365),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir les statistiques de progression"""
    start_date = datetime.utcnow() - timedelta(days=days)
    
    query = db.query(Progress).filter(
        Progress.user_id == current_user.id,
        Progress.date >= start_date
    )
    
    if language:
        query = query.filter(Progress.language == language)
    
    progress_entries = query.all()
    
    total_hours = sum(p.hours_studied for p in progress_entries)
    total_cards = sum(p.cards_reviewed for p in progress_entries)
    total_exercises = sum(p.exercises_completed for p in progress_entries)
    
    return {
        "period_days": days,
        "total_hours_studied": round(total_hours, 2),
        "total_cards_reviewed": total_cards,
        "total_exercises_completed": total_exercises,
        "avg_hours_per_day": round(total_hours / days, 2),
        "entries_count": len(progress_entries)
    }

@router.get("/{progress_id}", response_model=ProgressResponse)
async def get_progress_entry(
    progress_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer une entrée de progression spécifique"""
    progress = db.query(Progress).filter(
        Progress.id == progress_id,
        Progress.user_id == current_user.id
    ).first()
    
    if not progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    
    return progress

@router.put("/{progress_id}", response_model=ProgressResponse)
async def update_progress(
    progress_id: str,
    progress_update: ProgressUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour une entrée de progression"""
    db_progress = db.query(Progress).filter(
        Progress.id == progress_id,
        Progress.user_id == current_user.id
    ).first()
    
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    
    update_data = progress_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_progress, field, value)
    
    db.commit()
    db.refresh(db_progress)
    return db_progress

@router.delete("/{progress_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_progress(
    progress_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Supprimer une entrée de progression"""
    db_progress = db.query(Progress).filter(
        Progress.id == progress_id,
        Progress.user_id == current_user.id
    ).first()
    
    if not db_progress:
        raise HTTPException(status_code=404, detail="Progress entry not found")
    
    db.delete(db_progress)
    db.commit()
    return None
