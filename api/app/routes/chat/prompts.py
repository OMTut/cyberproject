from fastapi import APIRouter, HTTPException, status, Body
from typing import Dict, Any
import logging
from app.services.PromptDetectorService import PromptDetectorService
from app.services.llm_service import LLMService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.post("/chat/prompt", response_description="Analyze prompt for potential attacks", tags=["chat"])
async def analyze_prompt(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """
    Analyze a text prompt for potential attacks.
    Request body should contain a JSON object with a "text" field containing the prompt to analyze.
    Returns analysis results including whether the prompt is detected as an attack,
    the attack type if applicable, and a confidence score.
    """
    try:
        # Extract the text from the request body
        if "text" not in payload:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Request must include 'text' field"
            )
            
        prompt_text = payload["text"]
        
        # Analyze the prompt using the PromptDetectorService
        detector = PromptDetectorService()
        analysis_result = detector.analyze_prompt(prompt_text)
        
        logger.info(f"Prompt analyzed: {'ATTACK' if analysis_result['isAttack'] else 'CLEAN'}")

        # If it's an attack
        if analysis_result["isAttack"]:
            return {
                "status": "rejected",
                "reason": "Potential attack detected",
                "analysis": analysis_result
            }
        
        # If it's safe
        llm_service = LLMService()
        llm_response = await llm_service.generate_response(prompt_text)
        
        return llm_response
        
    except HTTPException:
        # Re-raise HTTP exceptions as they already have appropriate status codes
        raise
    except Exception as e:
        logger.error(f"Error analyzing prompt: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze prompt: {str(e)}"
        )