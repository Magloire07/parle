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
                # Heuristique: si la transcription contient des tokens hors chars lettres (ex "la la la"), forcer des erreurs vs texte attendu
                if expected_text:
                    import re
                    is_noise = len(re.findall(r"[a-zA-ZÀ-ÖØ-öø-ÿ]", transcription)) < 3
                    if is_noise:
                        # Marquer la plupart des mots attendus comme manqués
                        exp_tokens = re.findall(r"[\w'\-]+", expected_text)
                        errors = [
                            {
                                'type': 'deletion',
                                'word': w,
                                'expected': w,
                                'position': i,
                                'severity': 'high'
                            } for i, w in enumerate(exp_tokens[: min(5, len(exp_tokens))])
                        ]
                
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
        """Aligne la transcription avec le texte attendu avec appariement tolérant.

        - Normalisation insensible aux diacritiques (ex: garcon == garçon)
        - Retourne pour chaque opération un score de similarité `sim` (0..1)
        """
        if not expected_text:
            return {}
        
        import re, unicodedata

        def _strip_diacritics(text: str) -> str:
            nf = unicodedata.normalize('NFD', text)
            # supprimer les marques combinatoires
            no_marks = ''.join(ch for ch in nf if unicodedata.category(ch) != 'Mn')
            return no_marks

        def _normalize_token(tok: str) -> str:
            # minuscules + enlever diacritiques + garder lettres/chiffres/['-]
            tok = _strip_diacritics(tok.strip().lower())
            return re.sub(r"[^\w'\-]", '', tok)

        def normalize_words(s: str) -> List[str]:
            raw = re.findall(r"[\w'\-]+", s)
            return [_normalize_token(t) for t in raw if _normalize_token(t)]

        def char_similarity(a: str, b: str) -> float:
            """Levenshtein normalisé caractère (0..1)."""
            if a == b:
                return 1.0
            n, m = len(a), len(b)
            if n == 0 or m == 0:
                return 0.0
            dp = [[0]*(m+1) for _ in range(n+1)]
            for i in range(n+1):
                dp[i][0] = i
            for j in range(m+1):
                dp[0][j] = j
            for i in range(1, n+1):
                for j in range(1, m+1):
                    cost = 0 if a[i-1] == b[j-1] else 1
                    dp[i][j] = min(
                        dp[i-1][j] + 1,    # del
                        dp[i][j-1] + 1,    # ins
                        dp[i-1][j-1] + cost  # sub
                    )
            dist = dp[n][m]
            return max(0.0, 1.0 - dist / max(n, m))

        trans_words = normalize_words(transcription)
        expected_words = normalize_words(expected_text)

        # Levenshtein alignment with backtrace
        n, m = len(trans_words), len(expected_words)
        dp = [[0.0]*(m+1) for _ in range(n+1)]
        bt = [[None]*(m+1) for _ in range(n+1)]  # backtrace: 'M' approx/sub, 'I' insertion, 'D' deletion
        # Légère pénalisation des gaps et léger bonus pour match exact
        INS_COST = 1.0001
        DEL_COST = 1.0001
        EPS_MATCH_BONUS = 1e-6

        for i in range(n+1):
            dp[i][0] = i * DEL_COST
            if i>0: bt[i][0] = 'D'
        for j in range(m+1):
            dp[0][j] = j * INS_COST
            if j>0: bt[0][j] = 'I'

        for i in range(1, n+1):
            for j in range(1, m+1):
                # coût basé sur similarité caractère pour être tolérant
                sim = char_similarity(trans_words[i-1], expected_words[j-1])
                cost_sub = 1.0 - sim  # 0 si identique, proche de 0 si très similaire
                # bonus infinitésimal pour forcer un match exact le plus tôt possible
                if trans_words[i-1] == expected_words[j-1]:
                    cost_sub = max(0.0, cost_sub - EPS_MATCH_BONUS)
                # substitution/approx or match
                best = dp[i-1][j-1] + cost_sub
                op = 'M'
                # deletion (in transcription → missed expected word)
                if dp[i-1][j] + DEL_COST < best:
                    best = dp[i-1][j] + DEL_COST
                    op = 'D'
                # insertion (extra word in transcription)
                if dp[i][j-1] + INS_COST < best:
                    best = dp[i][j-1] + INS_COST
                    op = 'I'
                dp[i][j] = best
                bt[i][j] = op

        # backtrace to build operations
        i, j = n, m
        ops: List[Dict[str, Any]] = []
        while i>0 or j>0:
            op = bt[i][j]
            if op == 'M':
                sim = char_similarity(trans_words[i-1], expected_words[j-1])
                # on distingue match exact et substitution approximative mais on fournit toujours `sim`
                ops.append({
                    'op': 'match' if sim >= 0.9 else 'sub',
                    'i': i-1,
                    'j': j-1,
                    'trans': trans_words[i-1],
                    'exp': expected_words[j-1],
                    'sim': round(float(sim), 3)
                })
                i -= 1; j -= 1
            elif op == 'D':
                ops.append({
                    'op': 'del',
                    'i': i-1,
                    'j': None,
                    'trans': trans_words[i-1],
                    'exp': None,
                    'sim': 0.0
                })
                i -= 1
            elif op == 'I':
                ops.append({
                    'op': 'ins',
                    'i': None,
                    'j': j-1,
                    'trans': None,
                    'exp': expected_words[j-1],
                    'sim': 0.0
                })
                j -= 1
            else:
                break
        ops.reverse()

        # Post-traitement pour ré-ancrer les doublons sur leur première occurrence.
        # Cas observé: un mot répété (ex: "des") peut être apparié à une occurrence plus tardive
        # si la fin de la transcription diverge, ce qui rend le surlignage trompeur.
        # Stratégie minimale (non destructive pour le coût global):
        #  - repérer les 'ins' (mots attendus manqués)
        #  - si un 'match/sub' ultérieur a le même mot attendu et une position j plus grande,
        #    échanger les indices j pour que le match couvre la première occurrence.
        try:
            # Construire une map mot -> liste d'indices d'opérations 'ins' (dans l'ordre)
            insertion_positions = {}
            for idx, op in enumerate(ops):
                if op.get('op') == 'ins' and isinstance(op.get('exp'), str):
                    w = op['exp']
                    insertion_positions.setdefault(w, []).append(idx)
            # Parcourir les matches/substitutions et ré-ancrer si possible
            for idx, op in enumerate(ops):
                if op.get('op') in ('match', 'sub') and isinstance(op.get('exp'), str) and isinstance(op.get('j'), int):
                    w = op['exp']
                    ins_list = insertion_positions.get(w)
                    if not ins_list:
                        continue
                    # Chercher la première insertion antérieure avec j plus petit
                    for ins_idx in ins_list:
                        if ins_idx < idx:
                            ins_op = ops[ins_idx]
                            j_ins = ins_op.get('j')
                            j_match = op.get('j')
                            # Sécurité: les deux j doivent être des int et j_ins < j_match
                            if isinstance(j_ins, int) and isinstance(j_match, int) and j_ins < j_match:
                                # Échanger les indices j
                                ins_op['j'], op['j'] = j_match, j_ins
                                # Mise à jour: après échange on ne réutilise plus cette insertion
                                ins_list.remove(ins_idx)
                                break
        except Exception:
            # Ne jamais faire échouer l'alignement si post-process rate
            pass

        alignment: Dict[str, Any] = {
            'transcribed_words': trans_words,
            'expected_words': expected_words,
            'ops': ops,
            'edit_distance': dp[n][m],
            'max_len': max(n, m)
        }
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
        """Détecte les erreurs de prononciation en tenant compte de la similarité.

        - Les substitutions très proches (sim >= 0.8) ne sont pas considérées comme des erreurs
        - Les substitutions proches (0.6 <= sim < 0.8) sont des écarts mineurs (severity: low)
        - En-dessous, c'est une vraie erreur de prononciation (severity: medium)
        """
        errors = []
        
        if not expected_text:
            return errors
        
        ops = alignment.get('ops', [])
        for k, op in enumerate(ops):
            if op['op'] == 'del':
                errors.append({
                    'type': 'substitution_or_skip',
                    'word': op['trans'],
                    'expected': None,
                    'position': op['i'],
                    'severity': 'medium'
                })
            elif op['op'] == 'ins':
                errors.append({
                    'type': 'deletion',
                    'word': op['exp'],
                    'expected': op['exp'],
                    'position': op['j'],
                    'severity': 'high'
                })
            elif op['op'] == 'sub':
                sim = float(op.get('sim', 0.0))
                if sim >= 0.8:
                    # assez proche, ignorer
                    continue
                elif sim >= 0.6:
                    errors.append({
                        'type': 'near_miss',
                        'word': op['trans'],
                        'expected': op['exp'],
                        'position': op['i'],
                        'severity': 'low',
                        'similarity': round(sim, 3)
                    })
                else:
                    errors.append({
                        'type': 'mispronunciation',
                        'word': op['trans'],
                        'expected': op['exp'],
                        'position': op['i'],
                        'severity': 'medium',
                        'similarity': round(sim, 3)
                    })
        
        return errors
    
    async def _calculate_confidence(self, transcription: str, expected_text: str) -> float:
        """Calcule la confiance avec le même alignement tolérant que _align_text.

        Retourne un score 0..1 (1 = parfait)."""
        if not expected_text:
            return 0.0
        import re, unicodedata

        def _strip(text: str) -> str:
            nf = unicodedata.normalize('NFD', text)
            return ''.join(ch for ch in nf if unicodedata.category(ch) != 'Mn')

        def norm_tokens(s: str) -> List[str]:
            raw = re.findall(r"[\w'\-]+", s)
            toks = []
            for t in raw:
                t = _strip(t.lower())
                t = re.sub(r"[^\w'\-]", '', t)
                if t:
                    toks.append(t)
            return toks

        def sim(a: str, b: str) -> float:
            if a == b:
                return 1.0
            n, m = len(a), len(b)
            if n == 0 or m == 0:
                return 0.0
            dp = [[0]*(m+1) for _ in range(n+1)]
            for i in range(n+1): dp[i][0] = i
            for j in range(m+1): dp[0][j] = j
            for i in range(1, n+1):
                for j in range(1, m+1):
                    cost = 0 if a[i-1] == b[j-1] else 1
                    dp[i][j] = min(dp[i-1][j] + 1, dp[i][j-1] + 1, dp[i-1][j-1] + cost)
            dist = dp[n][m]
            return max(0.0, 1.0 - dist / max(n, m))

        a = norm_tokens(transcription)
        b = norm_tokens(expected_text)
        n, m = len(a), len(b)
        if max(n, m) == 0:
            return 0.0

        # dp tolérant: coût sub = 1 - sim(mot_a, mot_b)
        dp = [[0.0]*(m+1) for _ in range(n+1)]
        INS_COST = 1.0001
        DEL_COST = 1.0001
        EPS_MATCH_BONUS = 1e-6
        for i in range(n+1): dp[i][0] = float(i) * DEL_COST
        for j in range(m+1): dp[0][j] = float(j) * INS_COST
        for i in range(1, n+1):
            for j in range(1, m+1):
                cost_sub = 1.0 - sim(a[i-1], b[j-1])
                if a[i-1] == b[j-1]:
                    cost_sub = max(0.0, cost_sub - EPS_MATCH_BONUS)
                dp[i][j] = min(
                    dp[i-1][j] + DEL_COST,
                    dp[i][j-1] + INS_COST,
                    dp[i-1][j-1] + cost_sub
                )
        dist = dp[n][m]
        # normaliser par max(n, m)
        return max(0.0, min(1.0, 1.0 - (dist / max(n, m))))
