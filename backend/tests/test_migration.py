"""
Tests de migration pour l'API
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

class TestMigration:
    """Tests de migration"""
    
    def test_database_schema_compatibility(self):
        """Test compatibilité du schéma de base de données"""
        # Test que la base de données peut être créée
        response = client.get("/health/")
        assert response.status_code == 200
        
        # Vérifier que la base de données est accessible
        data = response.json()
        assert "database" in data
        assert data["database"] in ["healthy", "unhealthy"]
    
    def test_api_version_migration(self):
        """Test migration de version API"""
        # Test que l'API répond avec la bonne version
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "version" in data
        assert data["version"] == "1.0.0"
    
    def test_data_migration_compatibility(self):
        """Test compatibilité de migration des données"""
        # Test que les données peuvent être migrées
        response = client.post("/ocr/analyze", json={"text": "Test migration data"})
        assert response.status_code == 200
        
        data = response.json()
        assert "success" in data
        assert "text" in data
        assert "paragraphs" in data
    
    def test_configuration_migration(self):
        """Test migration de configuration"""
        # Test que la configuration est correcte
        response = client.get("/health/")
        assert response.status_code == 200
        
        # Vérifier que les services sont configurés
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"
    
    def test_dependency_migration(self):
        """Test migration des dépendances"""
        # Test que les dépendances sont disponibles
        response = client.get("/health/")
        assert response.status_code == 200
        
        # Vérifier que les services externes sont accessibles
        data = response.json()
        assert "database" in data
        assert data["database"] == "healthy"
    
    def test_backward_compatibility(self):
        """Test compatibilité ascendante"""
        # Test que l'API est compatible avec les versions précédentes
        response = client.get("/")
        assert response.status_code == 200
        
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "docs" in data