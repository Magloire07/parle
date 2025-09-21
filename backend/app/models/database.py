"""
Modèles de base de données SQLAlchemy
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    """Modèle utilisateur"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relations
    texts = relationship("Text", back_populates="user")
    readings = relationship("Reading", back_populates="user")
    summaries = relationship("Summary", back_populates="user")
    stats = relationship("Stat", back_populates="user")

class Text(Base):
    """Modèle texte extrait"""
    __tablename__ = "texts"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    paragraphs = Column(Text)  # JSON string des paragraphes
    language = Column(String(10), default="fr")
    confidence = Column(Float, default=0.0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="texts")
    readings = relationship("Reading", back_populates="text")

class Reading(Base):
    """Modèle enregistrement de lecture"""
    __tablename__ = "readings"
    
    id = Column(Integer, primary_key=True, index=True)
    text_id = Column(Integer, ForeignKey("texts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    audio_file = Column(String(255), nullable=False)
    transcription = Column(Text)
    confidence = Column(Float, default=0.0)
    errors = Column(Text)  # JSON string des erreurs
    prosody = Column(Text)  # JSON string des données prosodiques
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    text = relationship("Text", back_populates="readings")
    user = relationship("User", back_populates="readings")

class Summary(Base):
    """Modèle résumé oral"""
    __tablename__ = "summaries"
    
    id = Column(Integer, primary_key=True, index=True)
    text_id = Column(Integer, ForeignKey("texts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    audio_file = Column(String(255), nullable=False)
    transcription = Column(Text)
    relevance_score = Column(Float, default=0.0)
    quality_score = Column(Float, default=0.0)
    suggestions = Column(Text)  # JSON string des suggestions
    errors = Column(Text)  # JSON string des erreurs
    transitions = Column(Text)  # JSON string des transitions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    text = relationship("Text")
    user = relationship("User", back_populates="summaries")

class Stat(Base):
    """Modèle statistiques de progression"""
    __tablename__ = "stats"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), server_default=func.now())
    total_readings = Column(Integer, default=0)
    total_summaries = Column(Integer, default=0)
    average_confidence = Column(Float, default=0.0)
    common_errors = Column(Text)  # JSON string des erreurs fréquentes
    improvement_areas = Column(Text)  # JSON string des domaines d'amélioration
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relations
    user = relationship("User", back_populates="stats")
