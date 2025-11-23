"""
Modèle bloc de planning hebdomadaire
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class ScheduleBlock(Base):
    """Modèle bloc de planning hebdomadaire"""
    __tablename__ = "schedule_blocks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    day_of_week = Column(Integer, nullable=False)  # 0-6 (lundi=0)
    start_time = Column(String, nullable=False)  # "09:00"
    duration = Column(Integer, nullable=False)  # Minutes
    activity_type = Column(String, nullable=False)  # "speaking" | "listening" | "reading" | "writing" | "anki"
    activity_name = Column(String, nullable=False)
    completed = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    user = relationship("User", back_populates="schedule_blocks")
