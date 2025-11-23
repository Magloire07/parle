"""
Routes d'évaluation des résumés
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from app.services.summary_service import SummaryService
from app.core.config import settings
from app.models.summary import SummaryEvaluationResponse, SummaryEvaluationRequest, LLMEvaluationRequest
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/evaluate", response_model=SummaryEvaluationResponse)
async def evaluate_summary(
    audio_file: UploadFile = File(...),
    source_text: str = Form(None)
):
    """
    Évalue un résumé oral par rapport au texte source
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
        
        # Évaluation du résumé
        summary_service = SummaryService()
        result = await summary_service.evaluate_summary(content, source_text or "")
        
        return SummaryEvaluationResponse(
            success=True,
            transcription=result["transcription"],
            relevance_score=result["relevance_score"],
            quality_score=result["quality_score"],
            suggestions=result["suggestions"],
            errors=result["errors"],
            transitions=result["transitions"]
        )
        
    except Exception as e:
        logger.error(f"Erreur évaluation résumé: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de l'évaluation du résumé: {str(e)}"
        )

@router.post("/generate", response_model=SummaryEvaluationResponse)
async def generate_summary(request: SummaryEvaluationRequest):
    """
    Génère des suggestions de résumé à partir du texte source
    """
    try:
        summary_service = SummaryService()
        result = await summary_service.generate_summary_suggestions(request.source_text)
        return SummaryEvaluationResponse(
            success=True,
            transcription="",
            relevance_score=0.0,
            quality_score=0.0,
            suggestions=result["suggestions"],
            errors=[],
            transitions=result["transitions"]
        )
    except Exception as e:
        logger.error(f"Erreur génération résumé: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Erreur lors de la génération du résumé: {str(e)}"
        )

@router.post("/llm/evaluate", response_model=SummaryEvaluationResponse)
async def llm_evaluate_summary(request: SummaryEvaluationRequest):
    """Évalue un texte de résumé (déjà transcrit) via un LLM externe (OpenAI) avec fallback heuristique."""
    try:
        summary_service = SummaryService()
        result = await summary_service.llm_evaluate_summary(
            summary_text=request.source_text,
            source_text=request.source_text,  # rétro compat: même champ utilisé deux fois
            api_key=settings.GPT_API_KEY
        )
        return SummaryEvaluationResponse(
            success=True,
            transcription=result["transcription"],
            relevance_score=result["relevance_score"],
            quality_score=result["quality_score"],
            suggestions=result["suggestions"],
            errors=result["errors"],
            transitions=result["transitions"]
        )
    except Exception as e:
        logger.error(f"Erreur LLM évaluation résumé: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erreur LLM: {e}")

@router.post("/llm/full", response_model=SummaryEvaluationResponse)
async def llm_full_evaluate(request: LLMEvaluationRequest):
    """Nouvelle route LLM utilisant un résumé distinct du texte source."""
    try:
        summary_service = SummaryService()
        result = await summary_service.llm_evaluate_summary(
            summary_text=request.summary_text,
            source_text=request.source_text,
            api_key=settings.GPT_API_KEY
        )
        return SummaryEvaluationResponse(
            success=True,
            transcription=result["transcription"],
            relevance_score=result["relevance_score"],
            quality_score=result["quality_score"],
            suggestions=result["suggestions"],
            errors=result["errors"],
            transitions=result["transitions"]
        )
    except Exception as e:
        logger.error(f"Erreur LLM full: {e}")
        raise HTTPException(status_code=500, detail=f"Erreur LLM: {e}")
