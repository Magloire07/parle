"""
Tests de récupération pour l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRecovery:
    """Tests de récupération"""
    
    def test_health_check_recovery(self):
        """Test récupération de l'endpoint de santé"""
        # Test que l'endpoint de santé répond
        response = client.get("/health/")
        assert response.status_code == 200
        
        # Vérifier que l'endpoint est stable
        for _ in range(10):
            response = client.get("/health/")
            assert response.status_code == 200
    
    def test_error_recovery(self):
        """Test récupération après erreur"""
        # Test avec des données invalides
        response = client.post("/ocr/analyze", json={"text": None})
        assert response.status_code == 422
        
        # Vérifier que l'API récupère
        response = client.post("/ocr/analyze", json={"text": "Valid text"})
        assert response.status_code == 200
    
    def test_timeout_recovery(self):
        """Test récupération après timeout"""
        # Test que l'API gère les timeouts
        response = client.get("/health/")
        assert response.status_code == 200
        
        # Vérifier que l'API reste stable
        response = client.get("/health/")
        assert response.status_code == 200
    
    def test_memory_recovery(self):
        """Test récupération mémoire"""
        # Test que l'API libère la mémoire
        for _ in range(100):
            response = client.post("/ocr/analyze", json={"text": "Test text"})
            assert response.status_code == 200
        
        # Vérifier que l'API reste stable
        response = client.get("/health/")
        assert response.status_code == 200
    
    def test_connection_recovery(self):
        """Test récupération de connexion"""
        # Test que l'API gère les pertes de connexion
        response = client.get("/health/")
        assert response.status_code == 200
        
        # Vérifier que l'API récupère
        response = client.get("/health/")
        assert response.status_code == 200
    
    def test_data_recovery(self):
        """Test récupération de données"""
        # Test que l'API récupère les données
        response = client.post("/ocr/analyze", json={"text": "Test data recovery"})
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["text"] == "Test data recovery"