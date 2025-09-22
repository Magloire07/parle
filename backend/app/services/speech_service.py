"""
Service de traitement de la parole
"""
import logging
import tempfile
import os
from typing import Dict, List, Any

logger = logging.getLogger(__name__)
from app.core.config import settings

class SpeechService:
    """Service de traitement de la parole"""
    
    def __init__(self):
        self.whisper_model = None
        self._load_whisper_model()
    
    def _load_whisper_model(self):
        """Charge le modèle de transcription (faster-whisper si dispo, sinon simulation)"""
        try:
            from faster_whisper import WhisperModel  # type: ignore
            # Choisir un modèle léger par défaut
            model_size = os.getenv("WHISPER_MODEL", "base")
            device = os.getenv("WHISPER_DEVICE", "cpu")
            compute_type = "int8" if device == "cpu" else "float16"
            self.whisper_model = WhisperModel(model_size, device=device, compute_type=compute_type)
            logger.info(f"Modèle faster-whisper chargé: {model_size} ({device}/{compute_type})")
        except Exception as e:
            logger.warning(f"faster-whisper indisponible ({e}); bascule en mode simulé")
            self.whisper_model = "simulated"
    
    async def analyze_speech(self, audio_content: bytes, expected_text: str = None) -> Dict:
        """
        Analyse un enregistrement vocal
        """
        try:
            import subprocess, os, wave, contextlib, re

            # Sauvegarde temporaire du fichier audio (tel que reçu, souvent webm/opus)
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_in:
                temp_in.write(audio_content)
                temp_in_path = temp_in.name

            # Convertir en WAV PCM pour analyses basiques (nécessite ffmpeg installé)
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_out:
                temp_wav_path = temp_out.name

            try:
                subprocess.run([
                    'ffmpeg', '-y', '-i', temp_in_path,
                    '-ac', '1', '-ar', '16000', '-f', 'wav', temp_wav_path
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except Exception as conv_err:
                logger.warning(f"Conversion ffmpeg échouée: {conv_err}")
                # En dernier recours, essayer d'interpréter brut (échouera souvent)
                temp_wav_path = temp_in_path

            try:
                # Transcription (simulée pour MVP)
                transcription = await self._transcribe_audio(temp_wav_path)
                
                # Alignement avec le texte attendu
                alignment = await self._align_text(transcription, expected_text)
                
                # Analyse prosodique (basée en partie sur la durée)
                duration_sec = 0.0
                try:
                    with contextlib.closing(wave.open(temp_wav_path, 'r')) as wf:
                        frames = wf.getnframes()
                        rate = wf.getframerate()
                        duration_sec = frames / float(rate) if rate else 0.0
                except Exception as e:
                    logger.debug(f"Lecture WAV échouée pour durée: {e}")

                prosody = await self._analyze_prosody(temp_wav_path)
                # Injecter le tempo basé sur le débit (si expected_text fourni)
                if expected_text:
                    words = re.findall(r"[\w'\-]+", expected_text)
                    wpm = (len(words) / duration_sec * 60.0) if duration_sec > 0 else 0.0
                    prosody['tempo'] = float(max(60.0, min(200.0, wpm)))
                
                # Détection des erreurs
                errors = await self._detect_errors(transcription, expected_text, alignment)
                
                # Calcul de la confiance
                conf_align = await self._calculate_confidence(transcription, expected_text)
                # pondérer par la durée (éviter audios trop courts)
                duration_factor = max(0.0, min(1.0, duration_sec / 3.0))  # 3s => 1.0
                confidence = float(round(0.3 * duration_factor + 0.7 * conf_align, 2))
                
                return {
                    "transcription": transcription,
                    "alignment": alignment,
                    "errors": errors,
                    "prosody": prosody,
                    "confidence": confidence
                }
                
            finally:
                # Nettoyage des fichiers temporaires
                for p in [locals().get('temp_in_path'), locals().get('temp_wav_path')]:
                    try:
                        if p and os.path.exists(p):
                            os.unlink(p)
                    except Exception:
                        pass
                    
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
        """Transcrit un fichier audio (faster-whisper si dispo, sinon simulation)"""
        if not self.whisper_model:
            raise Exception("Modèle de transcription non chargé")
        try:
            # Si on est en mode simulé
            if isinstance(self.whisper_model, str):
                return "Transcription simulée du fichier audio"

            # faster-whisper
            lang_hint = getattr(settings, 'TTS_LANG', 'fr') or 'fr'
            segments, info = self.whisper_model.transcribe(
                audio_path,
                language=lang_hint,
                task='transcribe',
                vad_filter=True,
                beam_size=1
            )
            text_parts = []
            for seg in segments:
                text_parts.append(seg.text)
            return (" ".join(text_parts)).strip()
        except Exception as e:
            logger.error(f"Erreur transcription: {str(e)}")
            # Fallback de sécurité
            return ""
    
    async def _align_text(self, transcription: str, expected_text: str) -> Dict:
        """Aligne la transcription avec le texte attendu"""
        if not expected_text:
            return {}
        
        import re
        normalize = lambda s: re.findall(r"[\w'\-]+", s.lower())
        trans_words = normalize(transcription)
        expected_words = normalize(expected_text)

        alignment: Dict[str, Any] = {
            "transcribed_words": trans_words,
            "expected_words": expected_words,
            "matches": [],
            "insertions": [],
            "deletions": []
        }

        # Index expected words for quick lookup of positions
        expected_positions: Dict[str, list] = {}
        for idx, w in enumerate(expected_words):
            expected_positions.setdefault(w, []).append(idx)

        trans_positions: Dict[str, list] = {}
        for idx, w in enumerate(trans_words):
            trans_positions.setdefault(w, []).append(idx)

        # Matches on exact words present in both
        common = set(trans_positions.keys()) & set(expected_positions.keys())
        for w in common:
            # Pair first occurrences as matches (simple heuristic)
            alignment["matches"].append((trans_positions[w][0], expected_positions[w][0]))

        # Deletions: expected words not present in transcription
        for idx, w in enumerate(expected_words):
            if w not in trans_positions:
                alignment["deletions"].append((None, idx))

        # Insertions: transcribed words not in expected
        for idx, w in enumerate(trans_words):
            if w not in expected_positions:
                alignment["insertions"].append((idx, None))

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
        
        import re
        norm = lambda s: re.findall(r"[\w'\-]+", s)
        expected_tokens = norm(expected_text)
        trans_tokens = norm(transcription)

        # Erreurs basées sur l'alignement
        for i, j in alignment.get("deletions", []):
            if j is not None and 0 <= j < len(expected_tokens):
                errors.append({
                    "type": "deletion",
                    "word": expected_tokens[j],
                    "position": j,
                    "severity": "high"
                })
        
        for i, j in alignment.get("insertions", []):
            if i is not None and 0 <= i < len(trans_tokens):
                errors.append({
                    "type": "insertion",
                    "word": trans_tokens[i],
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
