"""
Routes pour les cartes flash (flashcards)
"""
from typing import List
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.flashcard import Flashcard
from app.schemas import FlashcardCreate, FlashcardUpdate, FlashcardResponse, FlashcardReview

router = APIRouter()

def calculate_next_review(quality: int, interval: int, ease_factor: float):
    """
    Algorithme de répétition espacée (simplifié SM-2)
    quality: 0-5 (0=total oubli, 5=parfait)
    """
    if quality < 3:
        # Mauvaise réponse: on recommence
        new_interval = 1
        new_ease = max(1.3, ease_factor - 0.2)
    else:
        # Bonne réponse
        if interval == 1:
            new_interval = 6
        else:
            new_interval = int(interval * ease_factor)
        
        # Ajustement ease_factor selon la qualité
        new_ease = ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
        new_ease = max(1.3, new_ease)
    
    next_review = datetime.utcnow() + timedelta(days=new_interval)
    return new_interval, new_ease, next_review

@router.post("/", response_model=FlashcardResponse, status_code=status.HTTP_201_CREATED)
async def create_flashcard(
    flashcard: FlashcardCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Créer une nouvelle carte flash"""
    db_flashcard = Flashcard(
        **flashcard.model_dump(),
        user_id=current_user.id
    )
    db.add(db_flashcard)
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

@router.get("/", response_model=List[FlashcardResponse])
async def get_flashcards(
    language: str = Query(None, pattern="^(en|fr)$"),
    category: str = Query(None),
    due: bool = Query(False, description="Only cards due for review"),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer les cartes flash de l'utilisateur"""
    query = db.query(Flashcard).filter(Flashcard.user_id == current_user.id)
    
    if language:
        query = query.filter(Flashcard.language == language)
    if category:
        query = query.filter(Flashcard.category == category)
    if due:
        query = query.filter(Flashcard.next_review <= datetime.utcnow())
    
    flashcards = query.offset(skip).limit(limit).all()
    return flashcards

@router.get("/{flashcard_id}", response_model=FlashcardResponse)
async def get_flashcard(
    flashcard_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer une carte flash spécifique"""
    flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    return flashcard

@router.put("/{flashcard_id}", response_model=FlashcardResponse)
async def update_flashcard(
    flashcard_id: str,
    flashcard_update: FlashcardUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour une carte flash"""
    db_flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    update_data = flashcard_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_flashcard, field, value)
    
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

@router.post("/{flashcard_id}/review", response_model=FlashcardResponse)
async def review_flashcard(
    flashcard_id: str,
    review: FlashcardReview,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Réviser une carte et calculer le prochain intervalle"""
    db_flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    # Calculer le prochain intervalle
    new_interval, new_ease, next_review = calculate_next_review(
        review.quality,
        db_flashcard.interval,
        db_flashcard.ease_factor
    )
    
    db_flashcard.interval = new_interval
    db_flashcard.ease_factor = new_ease
    db_flashcard.next_review = next_review
    db_flashcard.review_count += 1
    
    db.commit()
    db.refresh(db_flashcard)
    return db_flashcard

@router.delete("/{flashcard_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_flashcard(
    flashcard_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Supprimer une carte flash"""
    db_flashcard = db.query(Flashcard).filter(
        Flashcard.id == flashcard_id,
        Flashcard.user_id == current_user.id
    ).first()
    
    if not db_flashcard:
        raise HTTPException(status_code=404, detail="Flashcard not found")
    
    db.delete(db_flashcard)
    db.commit()
    return None
