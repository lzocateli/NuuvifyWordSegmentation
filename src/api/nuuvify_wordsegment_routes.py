from fastapi import APIRouter, HTTPException

from src.core.models import WordSegmentationRequest, WordSegmentationResponse
from src.services.nuuvify_wordsegment_service import nuuvify_wordsegment_service

router = APIRouter(prefix="/segment", tags=["Word Segmentation"])


@router.post("/", response_model=WordSegmentationResponse)
async def segment_text(input_data: WordSegmentationRequest):
    """Segmenta e formata texto usando NLP"""
    try:
        result = nuuvify_wordsegment_service.segment_and_format(
            input_data.text, input_data.language
        )
        return WordSegmentationResponse(original=input_data.text, formatted=result)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Erro ao processar texto: {str(e)}"
        )
