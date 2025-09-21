"""
Tests unitaires pour les services
"""
import pytest
from unittest.mock import Mock, patch
from app.services.ocr_service import OCRService
from app.services.speech_service import SpeechService
from app.services.tts_service import TTSService
from app.services.summary_service import SummaryService

class TestOCRService:
    """Tests pour le service OCR"""
    
    def test_clean_text(self):
        """Test nettoyage du texte"""
        service = OCRService()
        dirty_text = "  Test   text  \n\n  with  \t  spaces  "
        clean_text = service._clean_text(dirty_text)
        assert clean_text == "Test text with spaces"
    
    def test_segment_paragraphs(self):
        """Test segmentation en paragraphes"""
        service = OCRService()
        text = "Premier paragraphe.\n\nDeuxième paragraphe.\n\nTroisième paragraphe."
        paragraphs = service._segment_paragraphs(text)
        assert len(paragraphs) == 3
        assert paragraphs[0] == "Premier paragraphe."
        assert paragraphs[1] == "Deuxième paragraphe."
        assert paragraphs[2] == "Troisième paragraphe."
    
    def test_detect_language(self):
        """Test détection de langue"""
        service = OCRService()
        french_text = "Ceci est un texte en français avec des accents à é è"
        english_text = "This is an English text without accents"
        
        assert service._detect_language(french_text) == "fr"
        assert service._detect_language(english_text) == "en"

class TestTTSService:
    """Tests pour le service TTS"""
    
    def test_validate_text(self):
        """Test validation du texte"""
        service = TTSService()
        assert service._validate_text("Valid text") is True
        assert service._validate_text("") is False
        assert service._validate_text("   ") is False
        assert service._validate_text("x" * 6000) is False
    
    def test_get_supported_languages(self):
        """Test langues supportées"""
        service = TTSService()
        languages = service._get_supported_languages()
        assert "fr" in languages
        assert "en" in languages
        assert languages["fr"] == "Français"

class TestSummaryService:
    """Tests pour le service de résumé"""
    
    def test_extract_keywords(self):
        """Test extraction de mots-clés"""
        service = SummaryService()
        text = "Ceci est un texte de test avec des mots importants et des mots vides"
        keywords = service._extract_keywords(text)
        assert "texte" in keywords
        assert "test" in keywords
        assert "mots" in keywords
        assert "ceci" not in keywords  # Mot vide
    
    def test_analyze_structure(self):
        """Test analyse de structure"""
        service = SummaryService()
        good_summary = "Ceci est un bon résumé. Il contient plusieurs phrases. Et des connecteurs."
        bad_summary = "Résumé sans ponctuation"
        
        good_score = service._analyze_structure(good_summary)
        bad_score = service._analyze_structure(bad_summary)
        
        assert good_score > bad_score
        assert 0 <= good_score <= 1
        assert 0 <= bad_score <= 1
    
    def test_analyze_fluency(self):
        """Test analyse de fluidité"""
        service = SummaryService()
        good_summary = "Ceci est un résumé bien structuré avec des phrases de longueur appropriée."
        bad_summary = "Très court."
        
        good_score = service._analyze_fluency(good_summary)
        bad_score = service._analyze_fluency(bad_summary)
        
        assert good_score > bad_score
        assert 0 <= good_score <= 1
        assert 0 <= bad_score <= 1
