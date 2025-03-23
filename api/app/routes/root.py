from fastapi import APIRouter, Depends
import logging
from app.services.database import get_db

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/")
async def root(db=Depends(get_db)):
    """Root endpoint with database connection test"""
    try:
        logger.info("This is an info message")
        logger.error("this is an error message")
        logger.warning("This is a warning message")
        logger.debug("This is a debug message")
        
        # Verify connection with a simple command
        await db.command('ping')
        
        return {"message": "Connected to MongoDB"}
    except Exception as e:
        logger.error(f"Database error in root endpoint: {str(e)}")
        return {"message": "Error connecting to MongoDB", "error": str(e)}

