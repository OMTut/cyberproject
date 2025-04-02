from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any
from app.services.database.actions.prompts.getAttackByType import get_attack_by_type
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prompts/attacks/{attack_type}", response_description="Get attacks by type", tags=["prompts"])
async def list_attacks_by_type(attack_type: str) -> List[Dict[str, Any]]:
    """
    Fetch all attack prompts of a specific type from the database.
    Parameters:
    - attack_type: The type of attack to filter b
    Returns:
    - List of attack prompts of the specified type as JSON
    Raises:
    - 404: If no attacks of the specified type are found
    - 500: If there's a server error
    """
    try:
        attacks = await get_attack_by_type(attack_type)
        if not attacks:
            logger.info(f"No attacks found for type: {attack_type}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"No attacks found for type: {attack_type}"
            )
        return attacks
    except HTTPException:
        # Re-raise HTTP exceptions to preserve status code
        raise
    except Exception as e:
        logger.error(f"Error retrieving attacks by type '{attack_type}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve attacks by type: {str(e)}"
        )