from typing import List, Dict, Any, Optional
import logging
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.services.database.connection import get_database
from app.services.database.exceptions import DatabaseOperationError

logger = logging.getLogger(__name__)


async def get_all_attacks() -> List[Dict[str, Any]]:
    """
    Retrieve all prompts where isAttack is True from the database.
    Returns:
        List[Dict[str, Any]]: A list of attack prompts
    Raises:
        Exception: If there's an error retrieving the prompts
    """
    try:
        db: AsyncIOMotorDatabase = await get_database()
        prompts_collection = db["prompts"]
        
        # Query for prompts where isAttack is True
        cursor = prompts_collection.find({"isAttack": True})
        
        # Convert the cursor to a list
        attacks = await cursor.to_list(length=None)
        
        # Convert ObjectId to string for JSON serialization
        for attack in attacks:
            if "_id" in attack:
                attack["_id"] = str(attack["_id"])
        
        logger.info(f"Retrieved {len(attacks)} attack prompts")
        return attacks
    except Exception as e:
        logger.error(f"Failed to retrieve attack prompts: {str(e)}")
        raise Exception(f"Failed to retrieve attack prompts: {str(e)}")