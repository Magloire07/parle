"""
Configuration des tests pour le backend
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base
from app.core.config import settings

# Base de données de test
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Session de base de données pour les tests"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db_session):
    """Client de test FastAPI"""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client

@pytest.fixture
def sample_image():
    """Image de test pour les tests OCR"""
    import io
    from PIL import Image
    
    # Création d'une image de test simple
    img = Image.new('RGB', (100, 100), color='white')
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return img_bytes.getvalue()

@pytest.fixture
def sample_audio():
    """Audio de test pour les tests de parole"""
    import io
    import wave
    import numpy as np
    
    # Création d'un fichier audio de test simple
    sample_rate = 44100
    duration = 1.0
    frequency = 440.0
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    wave_data = np.sin(frequency * 2 * np.pi * t)
    wave_data = (wave_data * 32767).astype(np.int16)
    
    audio_bytes = io.BytesIO()
    with wave.open(audio_bytes, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(wave_data.tobytes())
    
    audio_bytes.seek(0)
    return audio_bytes.getvalue()

@pytest.fixture
def sample_text():
    """Texte de test pour les tests de résumé"""
    return """
    Ceci est un texte de test pour l'application Parle. 
    Il contient plusieurs paragraphes pour permettre de tester 
    les fonctionnalités de lecture et de résumé.
    
    Le deuxième paragraphe permet de tester la segmentation 
    et l'analyse des résumés oraux.
    """
