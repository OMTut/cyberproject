from typing import List, Dict, Any
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.database.connection import get_database
from app.services.database.exceptions import DatabaseOperationError

logger = logging.getLogger(__name__)

async def get_all_prompts() -> List[Dict[str, Any]]:
    """
    Returns:
        List[Dict[str, Any]]: A list of prompt documents
    Raises:
        DatabaseOperationError: If there's an error retrieving prompts from the database
    """
    try:
        db: AsyncIOMotorDatabase = await get_database()
        prompts_collection = db["prompts"]
        cursor = prompts_collection.find()
        prompts = await cursor.to_list(length=None)
            
        # Convert ObjectId to string for JSON serialization
        for prompt in prompts:
            if "_id" in prompt:
                prompt["_id"] = str(prompt["_id"])
                    
        return prompts
    except Exception as e:
        logger.error(f"Error retrieving prompts: {str(e)}")
        raise Exception(f"Failed to retrieve prompts: {str(e)}")