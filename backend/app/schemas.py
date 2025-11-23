"""
Schémas Pydantic pour l'API
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# ========== User Schemas ==========
class UserBase(BaseModel):
    email: EmailStr
    name: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

# ========== Flashcard Schemas ==========
class FlashcardBase(BaseModel):
    language: str = Field(..., pattern="^(en|fr)$")
    front: str
    back: str
    audio_url: Optional[str] = None
    tags: List[str] = []
    category: str = Field(..., pattern="^(vocabulary|grammar|expression)$")

class FlashcardCreate(FlashcardBase):
    pass

class FlashcardUpdate(BaseModel):
    front: Optional[str] = None
    back: Optional[str] = None
    audio_url: Optional[str] = None
    tags: Optional[List[str]] = None
    category: Optional[str] = None

class FlashcardReview(BaseModel):
    quality: int = Field(..., ge=0, le=5)  # 0-5 (difficulté de la réponse)

class FlashcardResponse(FlashcardBase):
    id: str
    user_id: str
    next_review: datetime
    interval: int
    ease_factor: float
    review_count: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ========== Recording Schemas ==========
class RecordingBase(BaseModel):
    language: str = Field(..., pattern="^(en|fr)$")
    exercise_type: str = Field(..., pattern="^(monologue|shadowing|debate|dictation)$")
    duration: int = Field(..., gt=0)
    transcript: Optional[str] = None
    notes: Optional[str] = None

class RecordingCreate(RecordingBase):
    audio_url: str

class RecordingResponse(RecordingBase):
    id: str
    user_id: str
    audio_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== Journal Schemas ==========
class JournalEntryBase(BaseModel):
    content: str
    practiced: List[str] = []
    difficulties: List[str] = []
    improvements: List[str] = []
    new_phrases: List[str] = []

class JournalEntryCreate(JournalEntryBase):
    pass

class JournalEntryUpdate(BaseModel):
    content: Optional[str] = None
    practiced: Optional[List[str]] = None
    difficulties: Optional[List[str]] = None
    improvements: Optional[List[str]] = None
    new_phrases: Optional[List[str]] = None

class JournalEntryResponse(JournalEntryBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ========== Progress Schemas ==========
class ProgressBase(BaseModel):
    language: str = Field(..., pattern="^(en|fr)$")
    date: datetime
    hours_studied: float = Field(default=0.0, ge=0)
    cards_reviewed: int = Field(default=0, ge=0)
    exercises_completed: int = Field(default=0, ge=0)

class ProgressCreate(ProgressBase):
    pass

class ProgressUpdate(BaseModel):
    hours_studied: Optional[float] = Field(None, ge=0)
    cards_reviewed: Optional[int] = Field(None, ge=0)
    exercises_completed: Optional[int] = Field(None, ge=0)

class ProgressResponse(ProgressBase):
    id: str
    user_id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# ========== Schedule Schemas ==========
class ScheduleBlockBase(BaseModel):
    day_of_week: int = Field(..., ge=0, le=6)
    start_time: str = Field(..., pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    duration: int = Field(..., gt=0)
    activity_type: str = Field(..., pattern="^(speaking|listening|reading|writing|anki)$")
    activity_name: str
    completed: bool = False

class ScheduleBlockCreate(ScheduleBlockBase):
    pass

class ScheduleBlockUpdate(BaseModel):
    day_of_week: Optional[int] = Field(None, ge=0, le=6)
    start_time: Optional[str] = Field(None, pattern="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$")
    duration: Optional[int] = Field(None, gt=0)
    activity_type: Optional[str] = None
    activity_name: Optional[str] = None
    completed: Optional[bool] = None

class ScheduleBlockResponse(ScheduleBlockBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
