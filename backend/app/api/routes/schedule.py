"""
Routes pour le planning hebdomadaire
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.models.user import User
from app.models.schedule import ScheduleBlock
from app.schemas import ScheduleBlockCreate, ScheduleBlockUpdate, ScheduleBlockResponse

router = APIRouter()

@router.post("/", response_model=ScheduleBlockResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule_block(
    block: ScheduleBlockCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Créer un nouveau bloc de planning"""
    db_block = ScheduleBlock(
        **block.model_dump(),
        user_id=current_user.id
    )
    db.add(db_block)
    db.commit()
    db.refresh(db_block)
    return db_block

@router.get("/", response_model=List[ScheduleBlockResponse])
async def get_schedule_blocks(
    day_of_week: int = Query(None, ge=0, le=6),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer les blocs de planning de l'utilisateur"""
    query = db.query(ScheduleBlock).filter(ScheduleBlock.user_id == current_user.id)
    
    if day_of_week is not None:
        query = query.filter(ScheduleBlock.day_of_week == day_of_week)
    
    blocks = query.order_by(ScheduleBlock.day_of_week, ScheduleBlock.start_time).offset(skip).limit(limit).all()
    return blocks

@router.get("/{block_id}", response_model=ScheduleBlockResponse)
async def get_schedule_block(
    block_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer un bloc de planning spécifique"""
    block = db.query(ScheduleBlock).filter(
        ScheduleBlock.id == block_id,
        ScheduleBlock.user_id == current_user.id
    ).first()
    
    if not block:
        raise HTTPException(status_code=404, detail="Schedule block not found")
    
    return block

@router.put("/{block_id}", response_model=ScheduleBlockResponse)
async def update_schedule_block(
    block_id: str,
    block_update: ScheduleBlockUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un bloc de planning"""
    db_block = db.query(ScheduleBlock).filter(
        ScheduleBlock.id == block_id,
        ScheduleBlock.user_id == current_user.id
    ).first()
    
    if not db_block:
        raise HTTPException(status_code=404, detail="Schedule block not found")
    
    update_data = block_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_block, field, value)
    
    db.commit()
    db.refresh(db_block)
    return db_block

@router.patch("/{block_id}/complete", response_model=ScheduleBlockResponse)
async def complete_schedule_block(
    block_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Marquer un bloc de planning comme complété"""
    db_block = db.query(ScheduleBlock).filter(
        ScheduleBlock.id == block_id,
        ScheduleBlock.user_id == current_user.id
    ).first()
    
    if not db_block:
        raise HTTPException(status_code=404, detail="Schedule block not found")
    
    db_block.completed = True
    db.commit()
    db.refresh(db_block)
    return db_block

@router.delete("/{block_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_schedule_block(
    block_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Supprimer un bloc de planning"""
    db_block = db.query(ScheduleBlock).filter(
        ScheduleBlock.id == block_id,
        ScheduleBlock.user_id == current_user.id
    ).first()
    
    if not db_block:
        raise HTTPException(status_code=404, detail="Schedule block not found")
    
    db.delete(db_block)
    db.commit()
    return None
