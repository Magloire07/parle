"""
Tests de performance pour l'API
"""
import pytest
import time
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestPerformance:
    """Tests de performance"""
    
    def test_health_endpoint_performance(self):
        """Test performance de l'endpoint de santé"""
        start_time = time.time()
        response = client.get("/health/")
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 1.0  # Moins d'1 seconde
    
    def test_ocr_analyze_performance(self):
        """Test performance de l'analyse OCR"""
        start_time = time.time()
        response = client.post("/ocr/analyze", json={"text": "Test text"})
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Moins de 2 secondes
    
    def test_tts_generate_performance(self):
        """Test performance de la génération TTS"""
        start_time = time.time()
        response = client.post("/tts/read", json={
            "text": "Test text",
            "language": "fr",
            "slow": False
        })
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 5.0  # Moins de 5 secondes
    
    def test_summary_generate_performance(self):
        """Test performance de la génération de résumé"""
        start_time = time.time()
        response = client.post("/summary/generate", json={
            "source_text": "Test source text for summary generation"
        })
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 10.0  # Moins de 10 secondes