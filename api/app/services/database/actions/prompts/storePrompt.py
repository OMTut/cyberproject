from typing import List, Dict, Any
from datetime import datetime
import logging
from app.services.database.connection import get_database

logger = logging.getLogger(__name__)

async def store_prompt_analysis(
    prompt: str,
    is_attack: bool,
    attack_type: str | None,
    confidence: float,
    matches: List[str]
) -> Dict[str, Any]:
    """
    Store a prompt and its analysis results in the database.
    Args:
        prompt: The original prompt text
        is_attack: Whether the prompt was identified as an attack
        attack_type: The type of attack if identified, None otherwise
        confidence: Confidence score of the analysis
        matches: List of matched patterns that triggered attack detection
    Returns:
        Dict containing the inserted document's ID
    """
    try:
        db = await get_database()
        collection = db.prompts

        document = {
            "prompt": prompt,
            "isAttack": is_attack,
            "attackType": attack_type,
            "confidence": confidence,
            "matches": matches,
            "created_at": datetime.utcnow()
        }

        result = await collection.insert_one(document)
        
        logger.info(f"Stored prompt analysis with ID: {result.inserted_id}")
        
        return {"id": str(result.inserted_id)}
        
    except Exception as e:
        logger.error(f"Error storing prompt analysis: {str(e)}")
        raise Exception(f"Failed to store prompt analysis: {str(e)}")
