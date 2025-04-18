from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.database.actions.prompts.getAllCleanPrompts import get_all_clean_prompts
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prompts/clean", response_description="List all prompts", tags=["prompts"])
async def list_all_clean_prompts() -> List[Dict[str, Any]]:
   """
   Fetch all prompts that are not attacks from the database.
   Returns a list of prompts as JSON.
   """
   try:
      return await get_all_clean_prompts()
   except Exception as e:
        logger.error(f"Error retrieving prompts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prompts"
        )