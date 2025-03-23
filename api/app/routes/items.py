from typing import Union
from fastapi import APIRouter, Depends
import logging
from app.services.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None, db=Depends(get_db)):
    """Example endpoint with database access"""
    try:
        # Example of how you might use the database (commented out until collections exist)
        # result = await db.items.find_one({"_id": item_id})
        # if result:
        #     return {**result, "q": q}
        
        return {"item_id": item_id, "q": q}
    except Exception as e:
        logger.error(f"Database error in read_item endpoint: {str(e)}")
        return {"message": "Error accessing database", "error": str(e)}

