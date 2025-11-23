"""
Service d'évaluation des résumés
"""
import logging
from typing import Dict, List, Any, Optional
import tempfile
import os
import re
import json
import asyncio

try:
    from openai import OpenAI
except ImportError:  # openai lib peut ne pas être installé encore
    OpenAI = None  # type: ignore

logger = logging.getLogger(__name__)

from app.core.config import settings


class SummaryService:
    """Service d'évaluation des résumés"""
    
    def __init__(self):
        self.whisper_model = None
        self.summarizer = None
        self._load_models()
    
    def _load_models(self):
        """Charge les modèles nécessaires (réel ou simulation)."""
        if settings.USE_SIMULATED_SUMMARY:
            self.whisper_model = "simulated"
            self.summarizer = "simulated"
            logger.info("[Summary] Mode simulation activé")
            return
        try:
            impl = settings.SUMMARY_TRANSCRIBE_IMPL.lower()
            if impl == "faster-whisper":
                from faster_whisper import WhisperModel  # type: ignore
                self.whisper_model = WhisperModel(settings.WHISPER_MODEL, device=settings.WHISPER_DEVICE)
                logger.info(f"[Summary] faster-whisper modèle '{settings.WHISPER_MODEL}' chargé")
            else:
                import whisper  # type: ignore
                self.whisper_model = whisper.load_model(settings.WHISPER_MODEL)
                logger.info(f"[Summary] openai-whisper modèle '{settings.WHISPER_MODEL}' chargé")
            self.summarizer = None  # Placeholder si un modèle de résumé distinct est ajouté plus tard
        except Exception as e:
            logger.error(f"Erreur chargement modèles (fallback simulation): {e}")
            self.whisper_model = "simulated"
            self.summarizer = "simulated"
    
    async def evaluate_summary(self, audio_content: bytes, source_text: str) -> Dict:
        """
        Évalue un résumé oral par rapport au texte source
        """
        try:
            # Sauvegarde temporaire du fichier audio
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as temp_file:
                temp_file.write(audio_content)
                temp_path = temp_file.name
            working_path = temp_path
            # Conversion si non simulation & ffmpeg disponible
            if self.whisper_model != "simulated":
                try:
                    import shutil, subprocess
                    ffmpeg_bin = shutil.which("ffmpeg")
                    if ffmpeg_bin:
                        wav_path = temp_path + ".wav"
                        cmd = [ffmpeg_bin, "-y", "-i", temp_path, "-ar", "16000", "-ac", "1", wav_path]
                        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                        working_path = wav_path
                except Exception as ce:
                    logger.warning(f"Conversion ffmpeg échouée (fallback fichier brut): {ce}")
            
            try:
                # Transcription du résumé
                transcription = await self._transcribe_summary(working_path)
                
                # Analyse de la pertinence
                relevance_score = await self._analyze_relevance(transcription, source_text)
                
                # Analyse de la qualité
                quality_score = await self._analyze_quality(transcription)
                
                # Génération de suggestions
                suggestions = await self._generate_suggestions(transcription, source_text)
                
                # Détection des erreurs
                errors = await self._detect_summary_errors(transcription)
                
                # Analyse des transitions
                transitions = await self._analyze_transitions(transcription)
                
                return {
                    "transcription": transcription,
                    "relevance_score": relevance_score,
                    "quality_score": quality_score,
                    "suggestions": suggestions,
                    "errors": errors,
                    "transitions": transitions
                }
                
            finally:
                for p in {temp_path, working_path}:
                    if p and os.path.exists(p):
                        try:
                            os.unlink(p)
                        except OSError:
                            pass
                    
        except Exception as e:
            logger.error(f"Erreur évaluation résumé: {str(e)}")
            raise
    
    async def generate_summary_suggestions(self, source_text: str) -> Dict:
        """
        Génère des suggestions de résumé à partir du texte source
        """
        try:
            if not self.summarizer:
                return {
                    "suggestions": ["Modèle de résumé non disponible"],
                    "transitions": ["Cependant", "De plus", "En conclusion"]
                }
            
            # Simulation de la génération de résumés
            suggestions = [
                "Résumé court simulé du texte source",
                "Résumé moyen simulé avec plus de détails",
                "Résumé long simulé avec tous les éléments importants"
            ]
            
            # Génération de transitions
            transitions = await self._generate_transitions(source_text)
            
            return {
                "suggestions": suggestions,
                "transitions": transitions
            }
            
        except Exception as e:
            logger.error(f"Erreur génération suggestions: {str(e)}")
            return {
                "suggestions": ["Erreur lors de la génération des suggestions"],
                "transitions": ["Cependant", "De plus", "En conclusion"]
            }
    
    async def _transcribe_summary(self, audio_path: str) -> str:
        """Transcrit le résumé audio (réel si modèle chargé, sinon simulation)."""
        if self.whisper_model == "simulated":
            return "Résumé simulé du texte audio"
        try:
            if settings.SUMMARY_TRANSCRIBE_IMPL.lower() == "faster-whisper":
                # streaming segments
                segments, info = self.whisper_model.transcribe(audio_path, beam_size=1)
                text_parts = []
                for seg in segments:
                    text_parts.append(seg.text.strip())
                transcript = " ".join(text_parts).strip()
                return transcript or "(Transcription vide)"
            else:
                # openai-whisper
                result = self.whisper_model.transcribe(audio_path)
                return result.get("text", "").strip() or "(Transcription vide)"
        except Exception as e:
            logger.error(f"Erreur transcription résumé: {e}")
            return "(Erreur transcription)"
    
    async def _analyze_relevance(self, summary: str, source_text: str) -> float:
        """Analyse la pertinence du résumé"""
        try:
            # Extraction des mots-clés du texte source
            source_keywords = self._extract_keywords(source_text)
            summary_keywords = self._extract_keywords(summary)
            
            # Calcul de la similarité des mots-clés
            common_keywords = set(source_keywords) & set(summary_keywords)
            total_keywords = set(source_keywords) | set(summary_keywords)
            
            if not total_keywords:
                return 0.0
            
            relevance = len(common_keywords) / len(total_keywords)
            return min(relevance, 1.0)
            
        except Exception as e:
            logger.error(f"Erreur analyse pertinence: {str(e)}")
            return 0.0
    
    async def _analyze_quality(self, summary: str) -> float:
        """Analyse la qualité du résumé"""
        try:
            # Vérification de la longueur
            word_count = len(summary.split())
            if word_count < 10:
                length_score = 0.3
            elif word_count < 50:
                length_score = 0.7
            else:
                length_score = 1.0
            
            # Vérification de la structure
            structure_score = self._analyze_structure(summary)
            
            # Vérification de la fluidité
            fluency_score = self._analyze_fluency(summary)
            
            # Score global
            quality = (length_score + structure_score + fluency_score) / 3
            return min(quality, 1.0)
            
        except Exception as e:
            logger.error(f"Erreur analyse qualité: {str(e)}")
            return 0.0
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrait les mots-clés d'un texte"""
        # Nettoyage et tokenisation
        words = re.findall(r'\b\w+\b', text.lower())
        
        # Filtrage des mots vides
        stop_words = {
            'le', 'la', 'les', 'un', 'une', 'des', 'du', 'de', 'et', 'ou', 'mais',
            'donc', 'or', 'ni', 'car', 'que', 'qui', 'quoi', 'dont', 'où', 'ce',
            'cette', 'ces', 'son', 'sa', 'ses', 'mon', 'ma', 'mes', 'ton', 'ta',
            'tes', 'notre', 'nos', 'votre', 'vos', 'leur', 'leurs', 'je', 'tu',
            'il', 'elle', 'nous', 'vous', 'ils', 'elles', 'me', 'te', 'se', 'nous',
            'vous', 'se', 'y', 'en', 'lui', 'leur', 'soi', 'même', 'autre', 'tout',
            'tous', 'toute', 'toutes', 'aucun', 'aucune', 'plusieurs', 'certains',
            'certaines', 'chaque', 'plus', 'moins', 'très', 'bien', 'mal', 'beaucoup',
            'peu', 'assez', 'trop', 'si', 'aussi', 'encore', 'déjà', 'jamais',
            'toujours', 'souvent', 'parfois', 'quelquefois', 'ne', 'pas', 'plus',
            'jamais', 'rien', 'personne', 'aucun', 'nulle', 'part', 'ici', 'là',
            'où', 'quand', 'comment', 'pourquoi', 'parce', 'que', 'afin', 'de',
            'pour', 'sans', 'avec', 'sous', 'sur', 'dans', 'entre', 'parmi',
            'devant', 'derrière', 'après', 'avant', 'pendant', 'depuis', 'jusqu',
            'à', 'vers', 'contre', 'selon', 'malgré', 'grâce', 'à', 'cause', 'de'
        }
        
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Retour des mots les plus fréquents
        from collections import Counter
        word_freq = Counter(keywords)
        return [word for word, freq in word_freq.most_common(20)]
    
    def _analyze_structure(self, summary: str) -> float:
        """Analyse la structure du résumé"""
        # Vérification de la présence de phrases complètes
        sentences = re.split(r'[.!?]+', summary)
        complete_sentences = [s.strip() for s in sentences if s.strip()]
        
        if not complete_sentences:
            return 0.0
        
        # Vérification de la cohérence
        coherence_score = 0.5  # Score de base
        
        # Vérification de la présence de connecteurs
        connectors = ['mais', 'donc', 'cependant', 'de plus', 'en outre', 'par ailleurs']
        connector_count = sum(1 for connector in connectors if connector in summary.lower())
        
        if connector_count > 0:
            coherence_score += 0.3
        
        return min(coherence_score, 1.0)
    
    def _analyze_fluency(self, summary: str) -> float:
        """Analyse la fluidité du résumé"""
        # Vérification de la longueur des phrases
        sentences = re.split(r'[.!?]+', summary)
        sentence_lengths = [len(s.split()) for s in sentences if s.strip()]
        
        if not sentence_lengths:
            return 0.0
        
        avg_length = sum(sentence_lengths) / len(sentence_lengths)
        
        # Score basé sur la longueur moyenne des phrases
        if 8 <= avg_length <= 20:
            fluency_score = 1.0
        elif 5 <= avg_length < 8 or 20 < avg_length <= 30:
            fluency_score = 0.7
        else:
            fluency_score = 0.4
        
        return fluency_score
    
    async def _generate_suggestions(self, summary: str, source_text: str) -> List[str]:
        """Génère des suggestions d'amélioration"""
        suggestions = []
        
        # Suggestion basée sur la longueur
        word_count = len(summary.split())
        if word_count < 20:
            suggestions.append("Votre résumé est trop court. Essayez d'inclure plus de détails.")
        elif word_count > 100:
            suggestions.append("Votre résumé est trop long. Concentrez-vous sur les points essentiels.")
        
        # Suggestion basée sur la structure
        if not re.search(r'[.!?]', summary):
            suggestions.append("Ajoutez de la ponctuation pour structurer votre résumé.")
        
        # Suggestion basée sur les connecteurs
        connectors = ['mais', 'donc', 'cependant', 'de plus', 'en outre']
        if not any(connector in summary.lower() for connector in connectors):
            suggestions.append("Utilisez des mots de liaison pour améliorer la fluidité.")
        
        return suggestions
    
    async def _detect_summary_errors(self, summary: str) -> List[Dict[str, Any]]:
        """Détecte les erreurs dans le résumé"""
        errors = []
        
        # Détection des répétitions
        words = summary.lower().split()
        word_freq = {}
        for word in words:
            word_freq[word] = word_freq.get(word, 0) + 1
        
        for word, freq in word_freq.items():
            if freq > 3 and len(word) > 3:
                errors.append({
                    "type": "repetition",
                    "word": word,
                    "count": freq,
                    "severity": "medium"
                })
        
        # Détection des phrases incomplètes
        sentences = re.split(r'[.!?]+', summary)
        for i, sentence in enumerate(sentences):
            if sentence.strip() and not sentence.strip().endswith(('.', '!', '?')):
                errors.append({
                    "type": "incomplete_sentence",
                    "sentence": sentence.strip(),
                    "position": i,
                    "severity": "low"
                })
        
        return errors
    
    async def _analyze_transitions(self, summary: str) -> List[str]:
        """Analyse les transitions utilisées"""
        transitions = []
        
        # Détection des connecteurs de transition
        transition_words = {
            'mais': 'opposition',
            'donc': 'conséquence',
            'cependant': 'opposition',
            'de plus': 'addition',
            'en outre': 'addition',
            'par ailleurs': 'addition',
            'en conclusion': 'conclusion',
            'finalement': 'conclusion',
            'd\'abord': 'ordre',
            'ensuite': 'ordre',
            'enfin': 'ordre'
        }
        
        for word, type_transition in transition_words.items():
            if word in summary.lower():
                transitions.append(f"{word} ({type_transition})")
        
        return transitions
    
    async def _generate_transitions(self, source_text: str) -> List[str]:
        """Génère des suggestions de transitions"""
        # Transitions basées sur le contenu
        transitions = [
            "Cependant",
            "De plus",
            "En outre",
            "Par ailleurs",
            "En conclusion",
            "Finalement",
            "D'abord",
            "Ensuite",
            "Enfin"
        ]
        
        return transitions

    # ====== LLM (GPT/OpenAI) Évaluation Avancée ======
    async def llm_evaluate_summary(self, summary_text: str, source_text: str, api_key: Optional[str]) -> Dict[str, Any]:
        """Évalue un résumé texte avec un LLM (OpenAI) si disponible, sinon heuristique fallback.

        Retourne un dict aligné avec SummaryEvaluationResponse.
        """
        # Fallback heuristique si pas de clé ou lib absente
        if not api_key or OpenAI is None:
            relevance = await self._analyze_relevance(summary_text, source_text)
            quality = await self._analyze_quality(summary_text)
            suggestions = await self._generate_suggestions(summary_text, source_text)
            errors = await self._detect_summary_errors(summary_text)
            transitions = await self._analyze_transitions(summary_text)
            return {
                "transcription": summary_text,
                "relevance_score": relevance,
                "quality_score": quality,
                "suggestions": suggestions,
                "errors": errors,
                "transitions": transitions,
                "_llm": False
            }

        prompt_system = (
            "Tu es un évaluateur pédagogique francophone. Tu reçois un TEXTE SOURCE et un RESUME (résumé oral transcrit). "
            "Tu dois retourner UNE SEULE STRUCTURE JSON STRICTE avec les champs: \n"
            "relevance_score (float 0-1), quality_score (float 0-1), suggestions (liste de chaînes), transitions (liste de chaînes), "
            "errors (liste d'objets {type, word, severity}), transcription (copie exacte du résumé). "
            "Relevance: couverture des points clés sans ajout erroné. Quality: clarté, structure (intro, développement, conclusion), fluidité, utilisation de connecteurs. "
            "Donne 3-6 suggestions actionnables. transitions: connecteurs utiles supplémentaires (max 8). errors: détecte répétitions excessives, prononciation potentielle (type=prononciation), phrases incomplètes (type=incomplete_sentence). severity in [low, medium, high]. "
            "Répond UNIQUEMENT par du JSON valide."
        )
        user_payload = {
            "source_text": source_text[:8000],  # limiter taille
            "summary": summary_text[:4000]
        }
        prompt_user = (
            "TEXTE SOURCE:\n" + user_payload["source_text"] + "\n\nRESUME:\n" + user_payload["summary"] + "\n\nProduis le JSON maintenant."
        )

        client = OpenAI(api_key=api_key)
        # Utilise un thread pour ne pas bloquer l'event loop si le SDK n'est pas async
        try:
            response = await asyncio.to_thread(
                lambda: client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": prompt_system},
                        {"role": "user", "content": prompt_user}
                    ],
                    temperature=0.2,
                    max_tokens=800
                )
            )
            content = response.choices[0].message.content if response and response.choices else ""
        except Exception as e:
            logger.error(f"Erreur appel OpenAI: {e}")
            # Fallback heuristique
            relevance = await self._analyze_relevance(summary_text, source_text)
            quality = await self._analyze_quality(summary_text)
            suggestions = await self._generate_suggestions(summary_text, source_text)
            errors = await self._detect_summary_errors(summary_text)
            transitions = await self._analyze_transitions(summary_text)
            return {
                "transcription": summary_text,
                "relevance_score": relevance,
                "quality_score": quality,
                "suggestions": suggestions + ["(Fallback LLM)"] if suggestions else ["(Fallback LLM)"] ,
                "errors": errors,
                "transitions": transitions,
                "_llm": False,
                "_error": str(e)
            }

        parsed = None
        if content:
            # Extraction robuste du JSON
            try:
                json_str = content.strip()
                # Supprime markdown fences si présents
                if json_str.startswith("```"):
                    json_str = re.sub(r'^```(json)?', '', json_str).strip()
                    if json_str.endswith('```'):
                        json_str = json_str[:-3].strip()
                parsed = json.loads(json_str)
            except Exception as e:
                logger.error(f"Parsing JSON LLM échoué: {e} | content tronqué: {content[:120]}")

        # Heuristiques + fusion
        relevance = self._safe_float(parsed, 'relevance_score') if parsed else None
        quality = self._safe_float(parsed, 'quality_score') if parsed else None
        suggestions = self._safe_list(parsed, 'suggestions') if parsed else []
        transitions = self._safe_list(parsed, 'transitions') if parsed else []
        errors = self._safe_list(parsed, 'errors') if parsed else []

        # Compléter avec heuristique si valeurs manquantes
        if relevance is None:
            relevance = await self._analyze_relevance(summary_text, source_text)
        if quality is None:
            quality = await self._analyze_quality(summary_text)
        if not transitions:
            transitions = await self._analyze_transitions(summary_text)
        if not errors:
            errors = await self._detect_summary_errors(summary_text)
        if not suggestions:
            suggestions = await self._generate_suggestions(summary_text, source_text)

        return {
            "transcription": summary_text,
            "relevance_score": max(0.0, min(1.0, relevance)),
            "quality_score": max(0.0, min(1.0, quality)),
            "suggestions": suggestions,
            "errors": errors,
            "transitions": transitions,
            "_llm": True,
            "_raw": content[:5000] if content else None
        }

    # Utils parsing JSON LLM
    def _safe_float(self, obj: Optional[dict], key: str) -> Optional[float]:
        try:
            if obj is None or key not in obj:
                return None
            return float(obj[key])
        except Exception:
            return None

    def _safe_list(self, obj: Optional[dict], key: str) -> List[Any]:
        if not obj or key not in obj:
            return []
        val = obj.get(key)
        return val if isinstance(val, list) else []
