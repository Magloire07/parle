"""
Modèle enregistrement audio
"""
from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Recording(Base):
    """Modèle enregistrement audio pour exercices"""
    __tablename__ = "recordings"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    language = Column(String(2), nullable=False)  # "en" | "fr"
    exercise_type = Column(String, nullable=False)  # "monologue" | "shadowing" | "debate" | "dictation" | "pronunciation"
    audio_url = Column(String, nullable=False)
    duration = Column(Integer, nullable=False)  # Secondes
    transcript = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Versioning
    parent_id = Column(String, ForeignKey("recordings.id", ondelete="CASCADE"), nullable=True)
    version = Column(Integer, default=1, nullable=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relation
    user = relationship("User", back_populates="recordings")
    versions = relationship("Recording", backref="parent", remote_side=[id])
