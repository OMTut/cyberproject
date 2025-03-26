from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
import logging
from app.services.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prompts/clean", response_model=List[Dict[str, Any]])
async def get_all_prompts(db=Depends(get_db)):
   """
   Fetch all prompts that are not attacks from the database.
   Returns a list of prompts as JSON.
   """
   try:
      # Connect to the prompts collection
      prompts_collection = db.prompts
        
      # Fetch all prompts from the database
      cursor = prompts_collection.find({"isAttack": False})
        
      # Convert MongoDB documents to Python dictionaries
      prompts = await cursor.to_list(length=None)
        
      # Convert ObjectId to string for JSON serialization
      for prompt in prompts:
         if "_id" in prompt:
            prompt["_id"] = str(prompt["_id"])
        
      return prompts
   except Exception as e:
         logger.error(f"Database error in getAllCleanPrompts endpoint: {str(e)}")
         raise HTTPException(status_code=500, detail=f"Error accessing database: {str(e)}")