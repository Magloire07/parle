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
from app.models.flashcard import Flashcard
from app.models.recording import Recording
from app.models.journal import JournalEntry
from app.models.schedule import ScheduleBlock
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
    period: str = Query("month", pattern="^(week|month|3months|year|all)$"),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Obtenir les statistiques globales de progression"""
    # Calculer la date de début selon la période
    now = datetime.utcnow()
    period_map = {
        "week": 7,
        "month": 30,
        "3months": 90,
        "year": 365,
        "all": None
    }
    
    days = period_map.get(period)
    start_date = now - timedelta(days=days) if days else None
    
    # Statistiques Flashcards
    flashcards_query = db.query(Flashcard).filter(Flashcard.user_id == current_user.id)
    if language:
        flashcards_query = flashcards_query.filter(Flashcard.language == language)
    if start_date:
        flashcards_query = flashcards_query.filter(Flashcard.created_at >= start_date)
    
    total_flashcards = flashcards_query.count()
    total_reviews = db.query(func.sum(Flashcard.review_count)).filter(
        Flashcard.user_id == current_user.id
    ).scalar() or 0
    
    # Répartition par catégorie
    flashcards_by_category = db.query(
        Flashcard.category,
        func.count(Flashcard.id)
    ).filter(
        Flashcard.user_id == current_user.id
    ).group_by(Flashcard.category).all()
    
    category_stats = {cat: count for cat, count in flashcards_by_category}
    
    # Progression par catégorie au fil du temps
    progression_data = {}
    categories = ['vocabulary', 'grammar', 'expression']
    
    if days:
        # Créer des intervalles de temps
        date_ranges = []
        interval = max(1, days // 10)  # Max 10 points sur le graphique
        
        for i in range(0, days, interval):
            date_ranges.append(now - timedelta(days=days-i))
        
        for category in categories:
            category_progression = []
            for date in date_ranges:
                count = db.query(func.count(Flashcard.id)).filter(
                    Flashcard.user_id == current_user.id,
                    Flashcard.category == category,
                    Flashcard.created_at <= date
                ).scalar() or 0
                category_progression.append(count)
            
            progression_data[category] = {
                'dates': [d.strftime('%Y-%m-%d') for d in date_ranges],
                'counts': category_progression
            }
    
    # Statistiques Enregistrements
    recordings_query = db.query(Recording).filter(Recording.user_id == current_user.id)
    if language:
        recordings_query = recordings_query.filter(Recording.language == language)
    if start_date:
        recordings_query = recordings_query.filter(Recording.created_at >= start_date)
    
    total_recordings = recordings_query.count()
    total_recording_time = db.query(func.sum(Recording.duration)).filter(
        Recording.user_id == current_user.id
    ).scalar() or 0
    
    # Statistiques Journal
    journal_query = db.query(JournalEntry).filter(JournalEntry.user_id == current_user.id)
    if language:
        journal_query = journal_query.filter(JournalEntry.language == language)
    if start_date:
        journal_query = journal_query.filter(JournalEntry.created_at >= start_date)
    
    total_journal_entries = journal_query.count()
    
    # Statistiques Planning
    schedule_query = db.query(ScheduleBlock).filter(ScheduleBlock.user_id == current_user.id)
    completed_blocks = schedule_query.filter(ScheduleBlock.completed == True).count()
    total_blocks = schedule_query.count()
    
    # Temps d'étude total (durée des enregistrements + temps de planning complété)
    completed_schedule_time = db.query(func.sum(ScheduleBlock.duration)).filter(
        ScheduleBlock.user_id == current_user.id,
        ScheduleBlock.completed == True
    ).scalar() or 0
    
    total_study_time_minutes = (total_recording_time // 60) + completed_schedule_time
    
    # Jours d'étude uniques
    study_days_query = db.query(func.date(Flashcard.created_at)).filter(
        Flashcard.user_id == current_user.id
    )
    if start_date:
        study_days_query = study_days_query.filter(Flashcard.created_at >= start_date)
    
    study_days = study_days_query.distinct().count()
    
    return {
        "total_flashcards": total_flashcards,
        "total_reviews": int(total_reviews),
        "total_recordings": total_recordings,
        "total_recording_time_seconds": total_recording_time,
        "total_journal_entries": total_journal_entries,
        "total_schedule_blocks": total_blocks,
        "completed_schedule_blocks": completed_blocks,
        "total_study_time_minutes": total_study_time_minutes,
        "study_days": study_days,
        "flashcards_by_category": category_stats,
        "progression_data": progression_data,
        "period": period,
        "language": language or "all"
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
