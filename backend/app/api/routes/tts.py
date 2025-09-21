"""
Routes de synthèse vocale
"""
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.services.tts_service import TTSService
from app.models.tts import TTSRequest, TTSResponse
import logging
import os

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/read", response_model=TTSResponse)
async def generate_speech(request: TTSRequest):
    """
    Génère un fichier audio à partir d'un texte
    """
    try:
        tts_service = TTSService()
        audio_file = await tts_service.generate_speech(
            text=request.text,
            language=request.language,
            slow=request.slow
        )
        
        return TTSResponse(
            success=True,
            audio_url=f"/static/{os.path.basename(audio_file)}",
            duration=request.duration,
            language=request.language
        )
        
    except Exception as e:
        logger.error(f"Erreur TTS: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération audio: {str(e)}"
        )

@router.get("/audio/{filename}")
async def get_audio_file(filename: str):
    """
    Récupère un fichier audio généré
    """
    try:
        file_path = os.path.join("static", filename)
        if not os.path.exists(file_path):
            raise HTTPException(
                status_code=404,
                detail="Fichier audio non trouvé"
            )
        
        return FileResponse(
            path=file_path,
            media_type="audio/mpeg",
            filename=filename
        )
        
    except Exception as e:
        logger.error(f"Erreur récupération audio: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la récupération du fichier audio: {str(e)}"
        )
