"""
Routes pour les enregistrements audio
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File
from sqlalchemy.orm import Session
import aiofiles
import os
from pathlib import Path
import uuid

from app.core.database import get_db
from app.core.auth import get_current_active_user
from app.core.config import settings
from app.models.user import User
from app.models.recording import Recording
from app.schemas import RecordingCreate, RecordingUpdate, RecordingResponse

router = APIRouter()

@router.post("/upload")
async def upload_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_active_user)
):
    """Upload un fichier audio"""
    # Vérifier le type de fichier
    allowed_types = ["audio/mpeg", "audio/wav", "audio/mp3", "audio/webm", "audio/ogg"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # Générer un nom de fichier unique
    file_ext = Path(file.filename).suffix
    filename = f"{uuid.uuid4()}{file_ext}"
    
    audio_dir = Path(settings.AUDIO_DIR) if not settings.DEBUG else Path("audio")
    filepath = audio_dir / filename
    
    # Sauvegarder le fichier
    async with aiofiles.open(filepath, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"audio_url": f"/audio/{filename}"}

@router.post("/", response_model=RecordingResponse, status_code=status.HTTP_201_CREATED)
async def create_recording(
    recording: RecordingCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Créer un nouvel enregistrement"""
    db_recording = Recording(
        **recording.model_dump(),
        user_id=current_user.id
    )
    db.add(db_recording)
    db.commit()
    db.refresh(db_recording)
    return db_recording

@router.get("/", response_model=List[RecordingResponse])
async def get_recordings(
    language: str = Query(None, pattern="^(en|fr)$"),
    exercise_type: str = Query(None),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer les enregistrements de l'utilisateur"""
    query = db.query(Recording).filter(Recording.user_id == current_user.id)
    
    if language:
        query = query.filter(Recording.language == language)
    if exercise_type:
        query = query.filter(Recording.exercise_type == exercise_type)
    
    recordings = query.order_by(Recording.created_at.desc()).offset(skip).limit(limit).all()
    return recordings

@router.get("/{recording_id}", response_model=RecordingResponse)
async def get_recording(
    recording_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Récupérer un enregistrement spécifique"""
    recording = db.query(Recording).filter(
        Recording.id == recording_id,
        Recording.user_id == current_user.id
    ).first()
    
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    return recording

@router.put("/{recording_id}", response_model=RecordingResponse)
async def update_recording(
    recording_id: str,
    recording_update: RecordingUpdate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Mettre à jour un enregistrement"""
    db_recording = db.query(Recording).filter(
        Recording.id == recording_id,
        Recording.user_id == current_user.id
    ).first()
    
    if not db_recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    # Mettre à jour uniquement les champs fournis
    update_data = recording_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_recording, field, value)
    
    db.commit()
    db.refresh(db_recording)
    return db_recording

@router.delete("/{recording_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_recording(
    recording_id: str,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Supprimer un enregistrement"""
    db_recording = db.query(Recording).filter(
        Recording.id == recording_id,
        Recording.user_id == current_user.id
    ).first()
    
    if not db_recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    
    # Supprimer le fichier audio aussi
    audio_path = Path(settings.AUDIO_DIR) / Path(db_recording.audio_url).name
    if audio_path.exists():
        os.remove(audio_path)
    
    db.delete(db_recording)
    db.commit()
    return None
