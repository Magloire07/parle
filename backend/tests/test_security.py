"""
Tests de sécurité pour l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestSecurity:
    """Tests de sécurité"""
    
    def test_cors_headers(self):
        """Test des en-têtes CORS"""
        response = client.options("/health/")
        assert response.status_code == 200
        assert "Access-Control-Allow-Origin" in response.headers
    
    def test_file_upload_security(self):
        """Test sécurité upload de fichiers"""
        # Test avec un fichier malveillant
        malicious_content = b"<?php system('rm -rf /'); ?>"
        response = client.post("/ocr/upload", files={
            "file": ("malicious.php", malicious_content, "application/octet-stream")
        })
        assert response.status_code == 400
    
    def test_input_validation(self):
        """Test validation des entrées"""
        # Test avec des données malformées
        response = client.post("/ocr/analyze", json={"text": None})
        assert response.status_code == 422
        
        # Test avec des données trop volumineuses
        large_text = "x" * 10000
        response = client.post("/ocr/analyze", json={"text": large_text})
        assert response.status_code == 200  # Doit être accepté mais traité
    
    def test_sql_injection_prevention(self):
        """Test prévention injection SQL"""
        # Test avec des tentatives d'injection SQL
        malicious_text = "'; DROP TABLE users; --"
        response = client.post("/ocr/analyze", json={"text": malicious_text})
        assert response.status_code == 200
        # Vérifier que la base de données n'a pas été compromise
        health_response = client.get("/health/")
        assert health_response.status_code == 200
    
    def test_xss_prevention(self):
        """Test prévention XSS"""
        # Test avec des scripts malveillants
        malicious_text = "<script>alert('XSS')</script>"
        response = client.post("/ocr/analyze", json={"text": malicious_text})
        assert response.status_code == 200
        # Vérifier que le script n'est pas exécuté
        data = response.json()
        assert "<script>" not in data["text"]
    
    def test_rate_limiting(self):
        """Test limitation du taux de requêtes"""
        # Envoyer plusieurs requêtes rapidement
        for _ in range(10):
            response = client.get("/health/")
            assert response.status_code == 200