"""
Service de traitement de la parole
"""
import logging
import tempfile
import os
from typing import Dict, List, Any

logger = logging.getLogger(__name__)

class SpeechService:
    """Service de traitement de la parole"""
    
    def __init__(self):
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Charge le modèle Whisper"""
        try:
            # Pour l'instant, on simule le chargement
            logger.info("Modèle Whisper simulé chargé")
            self.whisper_model = "simulated"
        except Exception as e:
            logger.error(f"Erreur chargement Whisper: {str(e)}")
            self.whisper_model = None
    
    async def analyze_speech(self, audio_content: bytes, expected_text: str = None) -> Dict:
        """
        Analyse un enregistrement vocal
        """
        try:
            # Sauvegarde temporaire du fichier audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name
            
            try:
                # Transcription avec Whisper
                transcription = await self._transcribe_audio(temp_path)
                
                # Alignement avec le texte attendu
                alignment = await self._align_text(transcription, expected_text)
                
                # Analyse prosodique
                prosody = await self._analyze_prosody(temp_path)
                
                # Détection des erreurs
                errors = await self._detect_errors(transcription, expected_text, alignment)
                
                # Calcul de la confiance
                confidence = await self._calculate_confidence(transcription, expected_text)
                
                return {
                    "transcription": transcription,
                    "alignment": alignment,
                    "errors": errors,
                    "prosody": prosody,
                    "confidence": confidence
                }
                
            finally:
                # Nettoyage du fichier temporaire
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Erreur analyse vocale: {str(e)}")
            raise
    
    async def analyze_prosody(self, audio_content: bytes, expected_text: str = None) -> Dict:
        """
        Analyse uniquement la prosodie
        """
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name
            
            try:
                # Transcription
                transcription = await self._transcribe_audio(temp_path)
                
                # Analyse prosodique
                prosody = await self._analyze_prosody(temp_path)
                
                return {
                    "transcription": transcription,
                    "alignment": {},
                    "errors": [],
                    "prosody": prosody,
                    "confidence": 0.0
                }
                
            finally:
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Erreur analyse prosodie: {str(e)}")
            raise
    
    async def _transcribe_audio(self, audio_path: str) -> str:
        """Transcrit un fichier audio avec Whisper"""
        if not self.whisper_model:
            raise Exception("Modèle Whisper non chargé")
        
        try:
            # Simulation de la transcription
            return "Transcription simulée du fichier audio"
        except Exception as e:
            logger.error(f"Erreur transcription: {str(e)}")
            raise
    
    async def _align_text(self, transcription: str, expected_text: str) -> Dict:
        """Aligne la transcription avec le texte attendu"""
        if not expected_text:
            return {}
        
        # Alignement simple basé sur les mots
        trans_words = transcription.lower().split()
        expected_words = expected_text.lower().split()
        
        alignment = {
            "transcribed_words": trans_words,
            "expected_words": expected_words,
            "matches": [],
            "insertions": [],
            "deletions": []
        }
        
        # Alignement simple
        i, j = 0, 0
        while i < len(trans_words) and j < len(expected_words):
            if trans_words[i] == expected_words[j]:
                alignment["matches"].append((i, j))
                i += 1
                j += 1
            elif trans_words[i] in expected_words[j:j+3]:
                # Insertion dans le texte attendu
                alignment["insertions"].append((i, j))
                i += 1
            else:
                # Suppression dans la transcription
                alignment["deletions"].append((i, j))
                j += 1
        
        return alignment
    
    async def _analyze_prosody(self, audio_path: str) -> Dict:
        """Analyse la prosodie (intonation, rythme, pauses)"""
        try:
            # Simulation de l'analyse prosodique
            return {
                "pitch": [100, 120, 110, 130, 115],
                "tempo": 120.0,
                "pauses": [{"start": 0.5, "duration": 0.2, "end": 0.7}],
                "intonation": {"monotone": False, "variation": 15.0, "mean_pitch": 115.0},
                "rhythm": {"tempo": 120.0, "regularity": 0.8, "beat_count": 10}
            }
            
        except Exception as e:
            logger.error(f"Erreur analyse prosodie: {str(e)}")
            return {}
    
    def _detect_pauses(self, y, sr: int) -> List[Dict]:
        """Détecte les pauses dans l'audio"""
        # Simulation de la détection de pauses
        return [{"start": 0.5, "duration": 0.2, "end": 0.7}]
    
    def _analyze_intonation(self, pitch) -> Dict:
        """Analyse l'intonation"""
        # Simulation de l'analyse d'intonation
        return {"monotone": False, "variation": 15.0, "mean_pitch": 115.0}
    
    def _analyze_rhythm(self, tempo: float, beats, sr: int) -> Dict:
        """Analyse le rythme"""
        # Simulation de l'analyse du rythme
        return {
            "tempo": float(tempo),
            "regularity": 0.8,
            "beat_count": 10
        }
    
    async def _detect_errors(self, transcription: str, expected_text: str, alignment: Dict) -> List[Dict]:
        """Détecte les erreurs de prononciation"""
        errors = []
        
        if not expected_text:
            return errors
        
        # Erreurs basées sur l'alignement
        for i, j in alignment.get("deletions", []):
            errors.append({
                "type": "deletion",
                "word": expected_text.split()[j],
                "position": j,
                "severity": "high"
            })
        
        for i, j in alignment.get("insertions", []):
            errors.append({
                "type": "insertion",
                "word": transcription.split()[i],
                "position": i,
                "severity": "medium"
            })
        
        return errors
    
    async def _calculate_confidence(self, transcription: str, expected_text: str) -> float:
        """Calcule la confiance de la transcription"""
        if not expected_text:
            return 0.0
        
        # Calcul simple basé sur la similarité
        trans_words = set(transcription.lower().split())
        expected_words = set(expected_text.lower().split())
        
        if not expected_words:
            return 0.0
        
        intersection = len(trans_words.intersection(expected_words))
        union = len(trans_words.union(expected_words))
        
        return intersection / union if union > 0 else 0.0
