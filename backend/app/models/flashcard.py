"""
Modèle carte flash (système SRS type Anki)
"""
from sqlalchemy import Column, String, Text, Float, Integer, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Flashcard(Base):
    """Modèle carte flash avec algorithme de répétition espacée"""
    __tablename__ = "flashcards"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)  # "en" | "fr"
    front = Column(Text, nullable=False)
    back = Column(Text, nullable=False)
    audio_url = Column(String, nullable=True)
    tags = Column(ARRAY(String), default=list)
    category = Column(String, nullable=False)  # "vocabulary" | "grammar" | "expression"
    
    # Algorithme de répétition espacée (SRS)
    next_review = Column(DateTime, nullable=False, default=datetime.utcnow)
    interval = Column(Integer, default=1)  # Jours
    ease_factor = Column(Float, default=2.5)
    review_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    user = relationship("User", back_populates="flashcards")
