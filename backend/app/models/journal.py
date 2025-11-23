"""
Modèle entrée de journal
"""
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, ARRAY
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
from app.core.database import Base

def generate_uuid():
    return str(uuid.uuid4())

class JournalEntry(Base):
    """Modèle entrée de journal de progression"""
    __tablename__ = "journal_entries"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    user_id = Column(String, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content = Column(Text, nullable=False)  # Markdown
    practiced = Column(ARRAY(String), default=list)  # Activités pratiquées
    difficulties = Column(ARRAY(String), default=list)
    improvements = Column(ARRAY(String), default=list)
    new_phrases = Column(ARRAY(String), default=list)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relation
    user = relationship("User", back_populates="journal_entries")
