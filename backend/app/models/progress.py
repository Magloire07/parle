"""
Modèle suivi de progression
"""
from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Progress(Base):
    """Modèle suivi de progression quotidienne"""
    __tablename__ = "progress"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)  # "en" | "fr"
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    
    hours_studied = Column(Float, default=0.0)
    cards_reviewed = Column(Integer, default=0)
    exercises_completed = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relation
    user = relationship("User", back_populates="progress")
