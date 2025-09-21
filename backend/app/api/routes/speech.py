"""
Routes de traitement de la parole
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.speech_service import SpeechService
from app.models.speech import SpeechAnalysisResponse, SpeechAnalysisRequest
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/analyze", response_model=SpeechAnalysisResponse)
async def analyze_speech(
    audio_file: UploadFile = File(...),
    expected_text: str = None
):
    """
    Analyse un enregistrement vocal et le compare au texte attendu
    """
    try:
        # Vérification du type de fichier
        if not audio_file.content_type.startswith('audio/'):
            raise HTTPException(
                status_code=400,
                detail="Le fichier doit être un fichier audio"
            )
        
        # Lecture du contenu du fichier
        content = await audio_file.read()
        
        # Traitement de la parole
        speech_service = SpeechService()
        result = await speech_service.analyze_speech(content, expected_text)
        
        return SpeechAnalysisResponse(
            success=True,
            transcription=result["transcription"],
            alignment=result["alignment"],
            errors=result["errors"],
            prosody=result["prosody"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        logger.error(f"Erreur analyse vocale: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse vocale: {str(e)}"
        )

@router.post("/prosody", response_model=SpeechAnalysisResponse)
async def analyze_prosody(request: SpeechAnalysisRequest):
    """
    Analyse uniquement la prosodie (intonation, rythme) d'un enregistrement
    """
    try:
        speech_service = SpeechService()
        result = await speech_service.analyze_prosody(request.audio_file, request.expected_text)
        
        return SpeechAnalysisResponse(
            success=True,
            transcription=result["transcription"],
            alignment=result["alignment"],
            errors=result["errors"],
            prosody=result["prosody"],
            confidence=result["confidence"]
        )
        
    except Exception as e:
        logger.error(f"Erreur analyse prosodie: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse prosodique: {str(e)}"
        )
