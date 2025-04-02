from fastapi import APIRouter, HTTPException, status, Body
from typing import Dict, Any
import logging
from app.services.PromptDetectorService import PromptDetectorService
from app.services.llm_service import LLMService
from app.services.database.actions.prompts.storePrompt import store_prompt_analysis

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

        try:
            await store_prompt_analysis(
                prompt=prompt_text,
                is_attack=analysis_result["isAttack"],
                attack_type=analysis_result["attackType"],
                confidence=analysis_result["confidence"],
                matches=analysis_result["matches"]
            )
        except Exception as db_error:
            logger.error(f"Failed to store prompt: {str(db_error)}")
            # Continue processing even if storage fails
        
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