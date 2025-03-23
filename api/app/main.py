from typing import Union
from fastapi import FastAPI
from app.database.connection import connect_to_mongodb, get_database
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection when the app starts"""
    try:
        await connect_to_mongodb()
        logger.info("Connected to MongoDB")
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection when the app shuts down"""
    try:
        client = await get_database()
        if client:
            client.close()
            logger.info("MongoDB connection closed")
    except Exception as e:
        logger.error(f"Error during database shutdown: {str(e)}")

@app.get("/")
async def root():
    """Root endpoint with database connection test"""
    try:
        logger.info("This is an info message")
        logger.error("this is an error message")
        logger.warning("This is a warning message")
        logger.debug("This is a debug message")
        
        # Use await with async database function
        db = await get_database()
        # Verify connection with a simple command
        await db.command('ping')
        
        return {"message": "Connected to MongoDB"}
    except Exception as e:
        logger.error(f"Database error in root endpoint: {str(e)}")
        return {"message": "Error connecting to MongoDB", "error": str(e)}


@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None):
    """Example endpoint with database access"""
    try:
        # Get database connection asynchronously
        db = await get_database()
        
        # Example of how you might use the database (commented out until collections exist)
        # result = await db.items.find_one({"_id": item_id})
        # if result:
        #     return {**result, "q": q}
        
        return {"item_id": item_id, "q": q}
    except Exception as e:
        logger.error(f"Database error in read_item endpoint: {str(e)}")
        return {"message": "Error accessing database", "error": str(e)}
