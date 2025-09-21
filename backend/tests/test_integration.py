"""
Tests d'intégration pour l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestHealthEndpoint:
    """Tests pour l'endpoint de santé"""
    
    def test_health_check(self):
        """Test de l'endpoint de santé"""
        response = client.get("/health/")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "version" in data

class TestOCREndpoint:
    """Tests pour l'endpoint OCR"""
    
    def test_ocr_upload_invalid_file(self):
        """Test upload de fichier invalide"""
        response = client.post("/ocr/upload", files={"file": ("test.txt", b"test content", "text/plain")})
        assert response.status_code == 400
        assert "image" in response.json()["detail"].lower()
    
    def test_ocr_analyze_text(self):
        """Test analyse de texte"""
        response = client.post("/ocr/analyze", json={"text": "Test text"})
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "text" in data
        assert "paragraphs" in data

class TestSpeechEndpoint:
    """Tests pour l'endpoint de traitement de la parole"""
    
    def test_speech_analyze_invalid_file(self):
        """Test analyse de fichier audio invalide"""
        response = client.post("/speech/analyze", files={"audio_file": ("test.txt", b"test content", "text/plain")})
        assert response.status_code == 400
        assert "audio" in response.json()["detail"].lower()

class TestTTSEndpoint:
    """Tests pour l'endpoint de synthèse vocale"""
    
    def test_tts_generate_speech(self):
        """Test génération de parole"""
        response = client.post("/tts/read", json={
            "text": "Test text",
            "language": "fr",
            "slow": False
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "audio_url" in data

class TestSummaryEndpoint:
    """Tests pour l'endpoint d'évaluation des résumés"""
    
    def test_summary_generate_suggestions(self):
        """Test génération de suggestions de résumé"""
        response = client.post("/summary/generate", json={
            "source_text": "Test source text"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert "suggestions" in data
        assert "transitions" in data
