from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.database.actions.prompts.getAllPrompts import get_all_prompts
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prompts", response_description="List all prompts", tags=["prompts"])
async def list_all_prompts() -> List[Dict[str, Any]]:
    """
    Retrieves all prompts from the database.
    Returns:
        List[Dict[str, Any]]: A list of prompts as dictionaries.
        FastAPI converts this to json
    Raises:
        HTTPException: If database operation fails
    """
    try:
      return await get_all_prompts()
    except Exception as e:
        logger.error(f"Error retrieving prompts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prompts"
        )