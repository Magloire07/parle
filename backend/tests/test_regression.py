"""
Tests de régression pour l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestRegression:
    """Tests de régression"""
    
    def test_ocr_analyze_consistency(self):
        """Test de cohérence de l'analyse OCR"""
        text = "Test text for consistency"
        
        # Exécuter plusieurs fois la même analyse
        responses = []
        for _ in range(5):
            response = client.post("/ocr/analyze", json={"text": text})
            assert response.status_code == 200
            responses.append(response.json())
        
        # Vérifier que les résultats sont cohérents
        first_result = responses[0]
        for result in responses[1:]:
            assert result["success"] == first_result["success"]
            assert result["text"] == first_result["text"]
            assert result["language"] == first_result["language"]
    
    def test_tts_generate_consistency(self):
        """Test de cohérence de la génération TTS"""
        text = "Test text for TTS consistency"
        
        # Exécuter plusieurs fois la même génération
        responses = []
        for _ in range(3):
            response = client.post("/tts/read", json={
                "text": text,
                "language": "fr",
                "slow": False
            })
            assert response.status_code == 200
            responses.append(response.json())
        
        # Vérifier que les résultats sont cohérents
        first_result = responses[0]
        for result in responses[1:]:
            assert result["success"] == first_result["success"]
            assert result["language"] == first_result["language"]
    
    def test_summary_generate_consistency(self):
        """Test de cohérence de la génération de résumé"""
        source_text = "Test source text for summary consistency"
        
        # Exécuter plusieurs fois la même génération
        responses = []
        for _ in range(3):
            response = client.post("/summary/generate", json={
                "source_text": source_text
            })
            assert response.status_code == 200
            responses.append(response.json())
        
        # Vérifier que les résultats sont cohérents
        first_result = responses[0]
        for result in responses[1:]:
            assert result["success"] == first_result["success"]
            assert "suggestions" in result
            assert "transitions" in result
    
    def test_error_handling_consistency(self):
        """Test de cohérence de la gestion d'erreurs"""
        # Test avec des données invalides
        invalid_responses = []
        
        # Test OCR avec données invalides
        response = client.post("/ocr/analyze", json={"text": None})
        invalid_responses.append(response.status_code)
        
        # Test TTS avec données invalides
        response = client.post("/tts/read", json={})
        invalid_responses.append(response.status_code)
        
        # Test Summary avec données invalides
        response = client.post("/summary/generate", json={})
        invalid_responses.append(response.status_code)
        
        # Vérifier que toutes les erreurs sont gérées de manière cohérente
        for status_code in invalid_responses:
            assert status_code in [400, 422]  # Erreur client
    
    def test_api_version_consistency(self):
        """Test de cohérence de la version API"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"
        
        # Vérifier que la version est cohérente dans tous les endpoints
        health_response = client.get("/health/")
        assert health_response.status_code == 200
        health_data = health_response.json()
        assert health_data["version"] == "1.0.0"