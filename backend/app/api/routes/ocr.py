"""
Routes OCR pour l'extraction de texte à partir d'images
"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.ocr_service import OCRService
from app.models.ocr import OCRResponse, OCRRequest
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/upload", response_model=OCRResponse)
async def extract_text_from_image(file: UploadFile = File(...)):
    """
    Extrait le texte d'une image uploadée
    """
    try:
        # Vérification du type de fichier
        if not file.content_type.startswith('image/'):
            raise HTTPException(
                status_code=400,
                detail="Le fichier doit être une image"
            )
        
        # Lecture du contenu du fichier
        content = await file.read()
        
        # Traitement OCR
        ocr_service = OCRService()
        result = await ocr_service.extract_text(content)
        
        return OCRResponse(
            success=True,
            text=result["text"],
            paragraphs=result["paragraphs"],
            confidence=result["confidence"],
            language=result["language"]
        )
        
    except Exception as e:
        logger.error(f"Erreur OCR: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'extraction du texte: {str(e)}"
        )

@router.post("/analyze", response_model=OCRResponse)
async def analyze_text(request: OCRRequest):
    """
    Analyse un texte déjà extrait pour le structurer
    """
    try:
        ocr_service = OCRService()
        result = await ocr_service.analyze_text(request.text)
        
        return OCRResponse(
            success=True,
            text=result["text"],
            paragraphs=result["paragraphs"],
            confidence=result["confidence"],
            language=result["language"]
        )
        
    except Exception as e:
        logger.error(f"Erreur analyse texte: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'analyse du texte: {str(e)}"
        )
