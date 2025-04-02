import logging
from typing import List, Dict, Any
from app.services.database.connection import get_database
from bson.objectid import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase

logger = logging.getLogger(__name__)

async def get_attack_by_type(attack_type: str) -> List[Dict[str, Any]]:
    """
    Retrieves attack prompts of a specific type from the database.
    Params:
        attack_type: The type of attack to filter by
    Returns:
        List of attack prompts matching the type
    Raises:
        Exception: If there's an error querying the database
    """
    try:
        db: AsyncIOMotorDatabase = await get_database()
        
        # Create filter query for both isAttack:true and the specified type
        filter_query = {
            "isAttack": True,
            "attackType": attack_type
        }
        
        cursor = db.prompts.find(filter_query)
        attack_prompts = await cursor.to_list(length=None)
        
        # Convert ObjectId to string for JSON serialization
        for prompt in attack_prompts:
            if "_id" in prompt:
                prompt["_id"] = str(prompt["_id"])
                
        return attack_prompts
    except Exception as e:
        logger.error(f"Error retrieving attack prompts of type {attack_type}: {str(e)}")
        raise Exception(f"Failed to retrieve attack prompts of type {attack_type}: {str(e)}")