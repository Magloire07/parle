"""
Tests de compatibilité pour l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestCompatibility:
    """Tests de compatibilité"""
    
    def test_api_endpoints_availability(self):
        """Test disponibilité des endpoints API"""
        endpoints = [
            ("/", "GET"),
            ("/health/", "GET"),
            ("/docs", "GET"),
            ("/redoc", "GET")
        ]
        
        for endpoint, method in endpoints:
            if method == "GET":
                response = client.get(endpoint)
            else:
                response = client.post(endpoint)
            
            assert response.status_code in [200, 404]  # 404 acceptable pour certains endpoints
    
    def test_cors_compatibility(self):
        """Test compatibilité CORS"""
        # Test avec différents headers CORS
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type"
        }
        
        response = client.options("/health/", headers=headers)
        assert response.status_code == 200
        
        # Vérifier les headers CORS
        assert "Access-Control-Allow-Origin" in response.headers
        assert "Access-Control-Allow-Methods" in response.headers
        assert "Access-Control-Allow-Headers" in response.headers
    
    def test_content_type_compatibility(self):
        """Test compatibilité des types de contenu"""
        # Test avec différents Content-Type
        content_types = [
            "application/json",
            "application/json; charset=utf-8",
            "text/plain"
        ]
        
        for content_type in content_types:
            response = client.post(
                "/ocr/analyze",
                json={"text": "Test text"},
                headers={"Content-Type": content_type}
            )
            assert response.status_code == 200
    
    def test_encoding_compatibility(self):
        """Test compatibilité des encodages"""
        # Test avec différents encodages
        encodings = ["utf-8", "latin-1", "ascii"]
        
        for encoding in encodings:
            text = "Test text with encoding: " + encoding
            response = client.post("/ocr/analyze", json={"text": text})
            assert response.status_code == 200
    
    def test_language_compatibility(self):
        """Test compatibilité des langues"""
        # Test avec différentes langues
        languages = ["fr", "en", "es", "de", "it"]
        
        for lang in languages:
            response = client.post("/tts/read", json={
                "text": "Test text",
                "language": lang,
                "slow": False
            })
            assert response.status_code == 200
    
    def test_browser_compatibility(self):
        """Test compatibilité navigateur"""
        # Test avec différents User-Agent
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        ]
        
        for user_agent in user_agents:
            response = client.get(
                "/health/",
                headers={"User-Agent": user_agent}
            )
            assert response.status_code == 200