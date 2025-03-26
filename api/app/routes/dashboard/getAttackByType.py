from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Query
import logging
from app.services.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/prompts/attacks/type", response_model=List[Dict[str, Any]])
async def get_attack_by_type(
   type: str = Query(..., description='The type of attack to filter by'),
   db=Depends(get_db)):
   """
   Fetch all prompts that are attacks where attackType is 'prompt-injection'
     from the database.
   Returns a list of prompts as JSON.
   """
   try:
      # Connect to the prompts collection
      prompts_collection = db.prompts

      # filter by query
      filter_criteria = { "attackType": type }
        
      # Fetch all prompts matching criteria from the database
      cursor = prompts_collection.find(filter_criteria)
        
      # Convert MongoDB documents to Python dictionaries
      prompts = await cursor.to_list(length=None)
      if not prompts:
          raise HTTPException(status_code=404, detail=f'No Pompts found with attack type: {type}')
        
      # Convert ObjectId to string for JSON serialization
      for prompt in prompts:
         if "_id" in prompt:
            prompt["_id"] = str(prompt["_id"])
        
      return prompts
   except Exception as e:
         logger.error(f"Database error in getAttackByType endpoint: {str(e)}")
         raise HTTPException(status_code=500, detail=f"Error accessing database: {str(e)}")