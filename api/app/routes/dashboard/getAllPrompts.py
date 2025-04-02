from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.database.connection import get_database
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prompts", response_description="List all prompts", tags=["prompts"])
async def get_all_prompts() -> List[Dict[str, Any]]:
    """
    Retrieves all prompts from the database.
    Returns:
        List[Dict[str, Any]]: A list of prompts as dictionaries.
        FastAPI converts this to json
    Raises:
        HTTPException: If database operation fails
    """
    try:
        db = await get_database()
        prompts_collection = db.prompts
        
        # Convert cursor to list of dictionaries
        prompts = await prompts_collection.find().to_list(length=None)
        
        # Convert ObjectId to string for JSON serialization
        for prompt in prompts:
            prompt["_id"] = str(prompt["_id"])
        
        return prompts
    
    except Exception as e:
        logger.error(f"Error retrieving prompts: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve prompts"
        )