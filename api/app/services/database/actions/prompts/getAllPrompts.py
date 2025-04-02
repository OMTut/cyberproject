from typing import List, Dict, Any, Optional
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.database.connection import get_database
from app.services.database.exceptions import DatabaseOperationError

logger = logging.getLogger(__name__)

async def get_all_prompts(
    limit: Optional[int] = None,
    skip: Optional[int] = None,
    sort_by: Optional[str] = "created_at",
    sort_order: int = -1  # -1 for descending, 1 for ascending
) -> List[Dict[str, Any]]:
    """
    Fetches prompts from the MongoDB collection, with optional
    pagination and sorting capabilities.
    Args:
        limit (Optional[int]): Maximum number of prompts to return (pagination)
        skip (Optional[int]): Number of prompts to skip (pagination)
        sort_by (Optional[str]): Field to sort by, defaults to "created_at"
        sort_order (int): Sort direction, 1 for ascending, -1 for descending
    Returns:
        List[Dict[str, Any]]: A list of prompt documents
    Raises:
        DatabaseOperationError: If there's an error retrieving prompts from the database
    """
    try:
        # Get database connection
        db: AsyncIOMotorDatabase = await get_database()
        
        # Set up the query pipeline
        pipeline = []
        
        # Add sorting
        if sort_by:
            pipeline.append({"$sort": {sort_by: sort_order}})
        
        # Add pagination
        if skip:
            pipeline.append({"$skip": skip})
        if limit:
            pipeline.append({"$limit": limit})
            
        # Execute the query
        cursor = db.prompts.aggregate(pipeline)
        prompts = await cursor.to_list(length=limit if limit else 1000)
        
        logger.info(f"Retrieved {len(prompts)} prompts from database")
        return prompts
        
    except Exception as e:
        error_msg = f"Error retrieving prompts: {str(e)}"
        logger.error(error_msg)
        raise DatabaseOperationError(error_msg) from e