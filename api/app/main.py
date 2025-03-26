from fastapi import FastAPI
from app.database.connection import connect_to_mongodb, get_database
import logging

# Import routers
from app.routes.root import router as root_router
from app.routes.items import router as items_router
from app.routes.getAllPrompts import router as prompts_router
from app.routes.getAllAttacks import router as allAttacks_router
from app.routes.chat import router as chat_router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Include routers
app.include_router(root_router)
app.include_router(items_router)
app.include_router(prompts_router)
app.include_router(allAttacks_router)
app.include_router(chat_router)

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
