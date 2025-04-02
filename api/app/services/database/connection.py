import motor.motor_asyncio
import logging
import asyncio
from typing import Optional, Dict, Any, AsyncGenerator
from contextlib import asynccontextmanager

from app.services.database.config import DatabaseConfig
from app.services.database.exceptions import DatabaseConnectionError, ConfigurationError

# Configure logging
logger = logging.getLogger(__name__)

class DatabaseConnection:
    """
    DatabaseConnection manages MongoDB connections with motor driver.
    
    Features:
    - Connection pooling with configurable pool size
    - Async context manager support for clean connection management
    - Lazy connection initialization
    - Connection health monitoring
    - Proper error handling with custom exceptions
    - Thread-safe client access
    
    Usage:
    ```python
    # As a context manager (recommended):
    async with DatabaseConnection() as db:
        collection = db["collection_name"]
        await collection.find_one({"key": "value"})
    
    # Manual connection management:
    db_conn = DatabaseConnection()
    await db_conn.connect()
    db = db_conn.get_database()
    # ... use db ...
    await db_conn.disconnect()
    ```
    """
    
    _instances: Dict[str, 'DatabaseConnection'] = {}
    _lock = asyncio.Lock()
    
    def __init__(
        self,
        config: Optional[DatabaseConfig] = None,
    ):
        """
        Initialize a new DatabaseConnection with the given configuration.
        Args:
            config: Optional DatabaseConfig instance. If None, a new one is created.
            max_pool_size: Maximum number of connections in the connection pool
            min_pool_size: Minimum number of connections in the connection pool
            max_idle_time_ms: Maximum time a connection can remain idle before being closed
            connect_timeout_ms: Timeout for connection attempts in milliseconds
        """
        self._config = config or DatabaseConfig()
        self._client: Optional[motor.motor_asyncio.AsyncIOMotorClient] = None
        self._db: Optional[motor.motor_asyncio.AsyncIOMotorDatabase] = None
        self._connected = False
    
    @classmethod
    async def get_instance(
        cls, 
        database_name: Optional[str] = None
    ) -> 'DatabaseConnection':
        """
        Get or create a DatabaseConnection instance (singleton per database).
        Args:
            database_name: Optional database name. If None, uses the one from config.
            **kwargs: Additional arguments to pass to the constructor if creating a new instance.
        Returns:
            A DatabaseConnection instance for the specified database
        """
        config = DatabaseConfig()
        db_name = database_name or config.db_name
        
        async with cls._lock:
            if db_name not in cls._instances:
                cls._instances[db_name] = DatabaseConnection(config=config)
                await cls._instances[db_name].connect()
                
            return cls._instances[db_name]
    
    async def connect(self) -> None:
        """
        Establish connection to MongoDB.
        Raises:
            DatabaseConnectionError: If connection fails
            ConfigurationError: If configuration is invalid
        """
        if self._connected:
            return
            
        try:
            # Configure MongoDB client with connection pooling settings from config
            connection_options = self._config.get_connection_options()
            self._client = motor.motor_asyncio.AsyncIOMotorClient(
                self._config.uri,
                **connection_options,
                serverSelectionTimeoutMS=self._config.connection_timeout_ms
            )
            
            # Verify connection by pinging the server
            await self._client.admin.command('ping')
            
            self._db = self._client[self._config.db_name]
            self._connected = True
            
            logger.info(f"Successfully connected to MongoDB database: {self._config.db_name}")
        except ConfigurationError as ce:
            # Re-raise configuration errors directly
            logger.error(f"Configuration error: {str(ce)}")
            raise
        except Exception as e:
            # Wrap other errors in our custom exception
            logger.error(f"Failed to connect to MongoDB: {str(e)}")
            raise DatabaseConnectionError(f"Failed to connect to MongoDB: {str(e)}", original_error=e)
    
    async def disconnect(self) -> None:
        """
        Close the MongoDB connection and release resources.
        """
        if self._client is not None:
            self._client.close()
            self._client = None
            self._db = None
            self._connected = False
            logger.info("Disconnected from MongoDB")
    
    async def reconnect(self) -> None:
        """
        Reconnect to the database by closing the current connection and creating a new one.
        Raises: DatabaseConnectionError: If reconnection fails
        """
        await self.disconnect()
        await self.connect()
    
    def get_database(self) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        """
        Get the database instance.
        Returns: AsyncIOMotorDatabase: The connected database instance
        Raises: DatabaseConnectionError: If not connected
        """
        if not self._connected:
            raise DatabaseConnectionError("Not connected to MongoDB. Call connect() first.")
            
        if self._db is None:
            raise DatabaseConnectionError("Database connection is None. There may be an issue with the connection.")
            
        return self._db
    
    def __getitem__(self, collection_name: str) -> motor.motor_asyncio.AsyncIOMotorCollection:
        """
        Get a collection by name using dictionary-like syntax.
        Args: collection_name: Name of the collection to retrieve
        Returns: AsyncIOMotorCollection: The requested collection
        Raises: DatabaseConnectionError: If not connected
            
        Example:
            db_conn = DatabaseConnection()
            await db_conn.connect()
            users = db_conn["users"]  # Get the 'users' collection
        """
        db = self.get_database()
        return db[collection_name]
    
    async def check_connection_health(self) -> bool:
        """
        Check if the database connection is healthy.
        Returns: bool: True if connection is healthy, False otherwise
        """
        if self._client is None:
            return False
            
        try:
            await self._client.admin.command('ping')
            return True
        except Exception as e:
            logger.warning(f"Connection health check failed: {str(e)}")
            return False
    
    @asynccontextmanager
    async def session(self) -> AsyncGenerator[motor.motor_asyncio.AsyncIOMotorClientSession, None]:
        """
        Create a MongoDB session for use with transactions.
        Yields: AsyncIOMotorClientSession: A MongoDB session
        Raises: DatabaseConnectionError: If not connected
        """
        if self._client is None:
            raise DatabaseConnectionError("Not connected to MongoDB. Call connect() first.")
            
        session = await self._client.start_session()
        try:
            yield session
        finally:
            await session.end_session()
    
    async def __aenter__(self) -> motor.motor_asyncio.AsyncIOMotorDatabase:
        """
        Enter the async context manager, ensuring connection is established.
        Returns: AsyncIOMotorDatabase: The connected database instance  
        Raises: DatabaseConnectionError: If connection fails
        """
        await self.connect()
        return self.get_database()
    
    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        """
        Exit the async context manager, closing the connection.
        """
        # We don't disconnect to preserve the connection pool
        # Only close on application shutdown
        pass

# Global instance for backward compatibility
_default_connection: Optional[DatabaseConnection] = None

async def get_database():
    """
    Returns database instance. Connects first if not connected.
    This is the main entry point for getting a database connection.
    Returns: AsyncIOMotorDatabase: The MongoDB database instance
    Raises: DatabaseConnectionError: If connection fails
    """
    global _default_connection
    
    # Initialize connection if needed
    if _default_connection is None:
        _default_connection = DatabaseConnection()
    
    # Connect if not already connected
    if not _default_connection._connected:
        await _default_connection.connect()
    
    # Return the database
    return _default_connection.get_database()

async def close_mongo_connection():
    """
    Close the MongoDB connection and shutdown application
    """
    global _default_connection
    
    if _default_connection is not None and _default_connection._connected:
        await _default_connection.disconnect()
        logger.info("MongoDB connection closed")

# Backwards compatibility functions
async def connect_to_mongodb():
    """
    Establishes connection to MongoDB and returns the client.
    Returns: AsyncIOMotorClient: The MongoDB client instance
    Raises: DatabaseConnectionError: If connection fails
    """
    global _default_connection
    
    if _default_connection is None:
        _default_connection = DatabaseConnection()
    
    await _default_connection.connect()
    return _default_connection._client

async def connect_to_mongo():
    """
    Establish connection to MongoDB.
    Returns: The MongoDB database instance
    Raises: DatabaseConnectionError: If connection fails
    """
    return await get_database()

