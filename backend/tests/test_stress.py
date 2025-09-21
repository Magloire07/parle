"""
Tests de stress pour l'API
"""
import pytest
import time
import threading
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestStress:
    """Tests de stress"""
    
    @pytest.mark.slow
    def test_high_frequency_requests(self):
        """Test requêtes haute fréquence"""
        def make_request():
            response = client.get("/health/")
            return response.status_code == 200
        
        # Exécuter 1000 requêtes
        start_time = time.time()
        results = []
        for _ in range(1000):
            results.append(make_request())
        end_time = time.time()
        
        # Vérifier que toutes les requêtes ont réussi
        assert all(results)
        
        # Vérifier que le temps total est raisonnable
        total_time = end_time - start_time
        assert total_time < 60  # Moins d'1 minute
    
    @pytest.mark.slow
    def test_concurrent_requests(self):
        """Test requêtes simultanées"""
        def make_request():
            response = client.get("/health/")
            return response.status_code == 200
        
        # Exécuter 100 requêtes simultanées
        threads = []
        results = []
        
        def worker():
            result = make_request()
            results.append(result)
        
        start_time = time.time()
        for _ in range(100):
            thread = threading.Thread(target=worker)
            threads.append(thread)
            thread.start()
        
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        
        # Vérifier que toutes les requêtes ont réussi
        assert all(results)
        
        # Vérifier que le temps total est raisonnable
        total_time = end_time - start_time
        assert total_time < 30  # Moins de 30 secondes
    
    @pytest.mark.slow
    def test_memory_stress(self):
        """Test stress mémoire"""
        def make_request():
            response = client.post("/ocr/analyze", json={"text": "Test text for memory stress"})
            return response.status_code == 200
        
        # Exécuter 500 requêtes pour stresser la mémoire
        start_time = time.time()
        results = []
        for _ in range(500):
            results.append(make_request())
        end_time = time.time()
        
        # Vérifier que toutes les requêtes ont réussi
        assert all(results)
        
        # Vérifier que le temps total est raisonnable
        total_time = end_time - start_time
        assert total_time < 120  # Moins de 2 minutes
    
    @pytest.mark.slow
    def test_cpu_stress(self):
        """Test stress CPU"""
        def make_request():
            response = client.post("/tts/read", json={
                "text": "Test text for CPU stress",
                "language": "fr",
                "slow": False
            })
            return response.status_code == 200
        
        # Exécuter 50 requêtes pour stresser le CPU
        start_time = time.time()
        results = []
        for _ in range(50):
            results.append(make_request())
        end_time = time.time()
        
        # Vérifier que la plupart des requêtes ont réussi
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.8  # 80% de succès minimum
        
        # Vérifier que le temps total est raisonnable
        total_time = end_time - start_time
        assert total_time < 300  # Moins de 5 minutes
    
    @pytest.mark.slow
    def test_io_stress(self):
        """Test stress I/O"""
        def make_request():
            response = client.post("/summary/generate", json={
                "source_text": "Test source text for IO stress"
            })
            return response.status_code == 200
        
        # Exécuter 100 requêtes pour stresser l'I/O
        start_time = time.time()
        results = []
        for _ in range(100):
            results.append(make_request())
        end_time = time.time()
        
        # Vérifier que la plupart des requêtes ont réussi
        success_rate = sum(results) / len(results)
        assert success_rate >= 0.9  # 90% de succès minimum
        
        # Vérifier que le temps total est raisonnable
        total_time = end_time - start_time
        assert total_time < 180  # Moins de 3 minutes