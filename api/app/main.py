from fastapi import FastAPI
from app.services.database.connection import connect_to_mongo, close_mongo_connection
import logging

# Import routers
from app.routes.dashboard.getAllPrompts import router as prompts_router
# from app.routes.dashboard.getAllAttacks import router as allAttacks_router
# from app.routes.dashboard.getAllCleanPrompts import router as allCleanPrompts_router
# from app.routes.dashboard.getAttackByType import router as attackByType_router
# from app.routes.chat import router as chat_router

# Configure logging
logging.basicConfig(
    #level=logging.DEBUG,
    #format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    level=logging.INFO,
    format='%(levelname)s:%(name)s:%(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI()

# Add startup event handler for overall app
@app.on_event("startup")
async def app_startup():
    """Log when the application starts"""
    logger.debug("FastAPI application starting up")
    
# Add shutdown event handler for overall app
@app.on_event("shutdown")
async def app_shutdown():
    """Log when the application shuts down"""
    logger.debug("FastAPI application shutting down")

# Include routers
# app.include_router(root_router)
# app.include_router(items_router)
app.include_router(prompts_router)
# app.include_router(allAttacks_router)
# app.include_router(allCleanPrompts_router)
# app.include_router(attackByType_router)
# app.include_router(chat_router)

@app.on_event("startup")
async def startup_db_client():
    """Initialize database connection when the app starts"""
    logger.debug("Starting database connection process")
    try:
        logger.debug("Attempting to connect to MongoDB...")
        await connect_to_mongo()
        logger.info("Successfully connected to MongoDB")
        logger.debug("Database connection established and ready for operations")
    except Exception as e:
        error_class = e.__class__.__name__
        detail = str(e)
        logger.error(f"Failed to connect to MongoDB: {error_class} - {detail}")
        logger.exception("Stack trace for database connection failure:")
        raise
    logger.debug("Database startup process completed")

@app.on_event("shutdown")
async def shutdown_db_client():
    """Close database connection when the app shuts down"""
    logger.debug("Starting database shutdown process")
    try:
        logger.debug("Attempting to close MongoDB connection...")
        await close_mongo_connection()
        logger.info("Successfully closed MongoDB connection")
    except Exception as e:
        error_class = e.__class__.__name__
        detail = str(e)
        logger.error(f"Error during database shutdown: {error_class} - {detail}")
        logger.exception("Stack trace for database shutdown failure:")
    logger.debug("Database shutdown process completed")
