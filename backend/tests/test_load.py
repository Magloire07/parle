"""
Tests de charge pour l'API
"""
import pytest
import asyncio
import aiohttp
import time
from concurrent.futures import ThreadPoolExecutor

class TestLoad:
    """Tests de charge"""
    
    @pytest.mark.slow
    def test_concurrent_health_checks(self):
        """Test de requêtes simultanées sur l'endpoint de santé"""
        def make_request():
            import requests
            response = requests.get("http://localhost:8000/health/")
            return response.status_code == 200
        
        # Exécuter 50 requêtes simultanées
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [executor.submit(make_request) for _ in range(50)]
            results = [future.result() for future in futures]
        
        # Vérifier que toutes les requêtes ont réussi
        assert all(results)
    
    @pytest.mark.slow
    def test_ocr_analyze_load(self):
        """Test de charge pour l'analyse OCR"""
        def make_request():
            import requests
            response = requests.post(
                "http://localhost:8000/ocr/analyze",
                json={"text": "Test text for load testing"}
            )
            return response.status_code == 200
        
        # Exécuter 20 requêtes simultanées
        with ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [future.result() for future in futures]
        
        # Vérifier que la plupart des requêtes ont réussi
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.9  # 90% de succès minimum
    
    @pytest.mark.slow
    def test_tts_generate_load(self):
        """Test de charge pour la génération TTS"""
        def make_request():
            import requests
            response = requests.post(
                "http://localhost:8000/tts/read",
                json={
                    "text": "Test text for TTS load testing",
                    "language": "fr",
                    "slow": False
                }
            )
            return response.status_code == 200
        
        # Exécuter 10 requêtes simultanées
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(10)]
            results = [future.result() for future in futures]
        
        # Vérifier que la plupart des requêtes ont réussi
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.8  # 80% de succès minimum
    
    @pytest.mark.slow
    def test_memory_usage(self):
        """Test d'utilisation mémoire"""
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss
        
        # Exécuter plusieurs opérations
        for _ in range(100):
            import requests
            response = requests.post(
                "http://localhost:8000/ocr/analyze",
                json={"text": "Test text for memory testing"}
            )
            assert response.status_code == 200
        
        final_memory = process.memory_info().rss
        memory_increase = final_memory - initial_memory
        
        # Vérifier que l'augmentation mémoire est raisonnable
        assert memory_increase < 100 * 1024 * 1024  # Moins de 100MB