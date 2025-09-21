"""
Service de synthèse vocale
"""
from gtts import gTTS
import tempfile
import os
import logging
from typing import Optional
import uuid

logger = logging.getLogger(__name__)

class TTSService:
    """Service de synthèse vocale"""
    
    def __init__(self):
        self.static_dir = "static"
        os.makedirs(self.static_dir, exist_ok=True)
    
    async def generate_speech(
        self, 
        text: str, 
        language: str = "fr", 
        slow: bool = False
    ) -> str:
        """
        Génère un fichier audio à partir d'un texte
        """
        try:
            # Génération du nom de fichier unique
            filename = f"tts_{uuid.uuid4().hex}.mp3"
            filepath = os.path.join(self.static_dir, filename)
            
            # Génération de la parole avec gTTS
            tts = gTTS(
                text=text,
                lang=language,
                slow=slow
            )
            
            # Sauvegarde du fichier
            tts.save(filepath)
            
            logger.info(f"Fichier audio généré: {filepath}")
            return filepath
            
        except Exception as e:
            logger.error(f"Erreur génération TTS: {str(e)}")
            raise
    
    async def generate_speech_with_ssml(
        self, 
        text: str, 
        language: str = "fr",
        ssml: Optional[str] = None
    ) -> str:
        """
        Génère un fichier audio avec SSML pour un contrôle avancé
        """
        try:
            # Pour l'instant, utilise la méthode standard
            # L'implémentation SSML nécessiterait un service plus avancé
            return await self.generate_speech(text, language)
            
        except Exception as e:
            logger.error(f"Erreur génération TTS SSML: {str(e)}")
            raise
    
    async def get_audio_duration(self, filepath: str) -> float:
        """
        Calcule la durée d'un fichier audio
        """
        try:
            import librosa
            y, sr = librosa.load(filepath)
            duration = len(y) / sr
            return duration
        except Exception as e:
            logger.error(f"Erreur calcul durée: {str(e)}")
            return 0.0
    
    async def cleanup_old_files(self, max_age_hours: int = 24):
        """
        Nettoie les anciens fichiers audio
        """
        try:
            import time
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for filename in os.listdir(self.static_dir):
                if filename.startswith("tts_"):
                    filepath = os.path.join(self.static_dir, filename)
                    file_age = current_time - os.path.getmtime(filepath)
                    
                    if file_age > max_age_seconds:
                        os.remove(filepath)
                        logger.info(f"Fichier supprimé: {filename}")
                        
        except Exception as e:
            logger.error(f"Erreur nettoyage fichiers: {str(e)}")
    
    def _validate_text(self, text: str) -> bool:
        """Valide le texte avant génération"""
        if not text or not text.strip():
            return False
        
        # Vérification de la longueur
        if len(text) > 5000:
            return False
        
        return True
    
    def _get_supported_languages(self) -> dict:
        """Retourne les langues supportées"""
        return {
            "fr": "Français",
            "en": "Anglais",
            "es": "Espagnol",
            "de": "Allemand",
            "it": "Italien",
            "pt": "Portugais"
        }
