import motor.motor_asyncio
import logging
import os
import urllib.parse
from dotenv import load_dotenv
from app.database.utils.uri_formatter import format_mongodb_uri

# Configure logging
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get MongoDB connection string from environment variables
MONGODB_URI_RAW = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB_NAME")
if not DB_NAME:
    logger.error("MONGODB_DB_NAME not found")
    raise ValueError("MONGODB_DB_NAME variable is required")



# Format the MongoDB connection string with encoded credentials
MONGODB_URI = format_mongodb_uri(MONGODB_URI_RAW)

# Create MongoDB client
client = None

async def connect_to_mongodb():
    """Establishes connection to MongoDB and logs status."""
    global client
    try:
        # Create client connection with encoded URI
        client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URI)
        # Trigger actual connection attempt
        await client.admin.command('ping')
        logger.info("Successfully connected to MongoDB")
        return client
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {str(e)}")
        raise

async def get_database():
    """Returns database instance. Connects first if not connected."""
    global client
    if client is None:
        await connect_to_mongodb()
    return client[DB_NAME]

