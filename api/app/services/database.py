import logging
from app.database.connection import get_database

logger = logging.getLogger(__name__)

async def get_db():
    """
    Dependency function to get database connection for routes
    Returns a database connection that can be used in route handlers
    """
    try:
        db = await get_database()
        return db
    except Exception as e:
        logger.error(f"Error getting database connection: {str(e)}")
        raise

