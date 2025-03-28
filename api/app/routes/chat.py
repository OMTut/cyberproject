from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm_service import LLMService
import logging

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

logger = logging.getLogger(__name__)
llm_service = LLMService()

class ChatRequest(BaseModel):
    text: str

class ChatResponse(BaseModel):
    response: str

class HealthCheckResponse(BaseModel):
    status: str
    message: str

@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """
    Check the health of the LLM service connection
    """
    try:
        result = await llm_service.health_check()
        return HealthCheckResponse(**result)
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=500, detail="Health check failed")

@router.post("/prompt", response_model=ChatResponse)
async def process_chat(request: ChatRequest):
    """
    Process a chat prompt and return the LLM response
    """
    try:
        # The prompt injection check would go here
        # For now, we'll pass directly to the LLM
        
        # Get response from LLM service
        result = await llm_service.generate_response(request.text)
        
        # Handle different response formats
        if isinstance(result, dict):
            # Handle direct dictionary response
            response_text = result.get('generated_text', '')
        elif isinstance(result, list) and len(result) > 0:
            # Handle list of responses (take the first one)
            if isinstance(result[0], dict):
                response_text = result[0].get('generated_text', '')
            else:
                response_text = str(result[0])
        else:
            # If we get an unexpected format, convert to string
            response_text = str(result) if result else "No response generated"
        
        # Ensure we have some content to return
        if not response_text:
            response_text = "The model didn't generate a response. Please try again."
        
        logger.info(f"Generated response for prompt: {request.text[:30]}...")
        return ChatResponse(response=response_text)
        
    except ValueError as ve:
        logger.error(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except ConnectionError as ce:
        logger.error(f"Connection error with LLM service: {str(ce)}")
        raise HTTPException(status_code=503, detail="Unable to connect to LLM service")
    except TimeoutError as te:
        logger.error(f"Timeout error with LLM service: {str(te)}")
        raise HTTPException(status_code=504, detail="LLM service request timed out")
    except Exception as e:
        logger.error(f"Error processing chat: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to process chat prompt")

