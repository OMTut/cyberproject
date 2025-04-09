import os
import urllib.parse
import logging
from typing import Optional
from dotenv import load_dotenv
from app.services.utils.uri_formatter import format_uri_for_config

logger = logging.getLogger(__name__)


class DatabaseConfig:
    """
    Configuration class for database connection settings.
    Handles loading environment variables, URI formatting, and connection pool settings.
    """

    def __init__(self):
        """Initialize the database configuration by loading environment variables."""
        # Load environment variables from .env file
        load_dotenv()
        
        # Database connection settings
        try:
            self.uri = self._get_formatted_uri()
        except Exception as e:
            logger.error(f"Failed to configure database URI: {str(e)}", exc_info=True)
            raise ValueError(f"Database configuration error: {str(e)}") from e
        self.db_name = self._get_required_env("MONGODB_DB_NAME")
        
        # Connection pool settings with reasonable defaults
        self.max_pool_size = int(os.getenv("MONGODB_MAX_POOL_SIZE", "10"))
        self.min_pool_size = int(os.getenv("MONGODB_MIN_POOL_SIZE", "1"))
        self.max_idle_time_ms = int(os.getenv("MONGODB_MAX_IDLE_TIME_MS", "50000"))
        self.connection_timeout_ms = int(os.getenv("MONGODB_CONNECTION_TIMEOUT_MS", "20000"))
        
        # SSL/TLS configuration
        self.tls_enabled = os.getenv("MONGODB_TLS_ENABLED", "true").lower() == "true"
        self.tls_allow_invalid_certs = os.getenv("MONGODB_TLS_ALLOW_INVALID_CERTS", "false").lower() == "true"
        self.tls_ca_file = os.getenv("MONGODB_TLS_CA_FILE", None)

        logger.info(f"Database configuration loaded for {self.db_name}")

    def _get_required_env(self, var_name: str) -> str:
        """
        Get a required environment variable.
        Args: var_name: Name of the environment variable
        Returns: The value of the environment variable
        Raises: ValueError: If the environment variable is not set
        """
        value = os.getenv(var_name)
        if not value:
            logger.error(f"{var_name} environment variable is required but not set")
            raise ValueError(f"{var_name} environment variable is required")
        return value

    def _get_formatted_uri(self) -> str:
        """
        Format the MongoDB URI with properly encoded credentials.
        Returns: Properly formatted MongoDB URI with encoded credentials
        Raises: ValueError: If the MongoDB URI is invalid or cannot be formatted
        """
        # Get the raw URI from environment variables
        mongo_uri = self._get_required_env("MONGODB_URI")
        return format_uri_for_config(mongo_uri)
        
    def get_connection_options(self) -> dict:
        """
        Get all connection options as a dictionary for the MongoDB client.
        Returns: Dictionary of connection options
        """
        options = {
            "maxPoolSize": self.max_pool_size,
            "minPoolSize": self.min_pool_size,
            "maxIdleTimeMS": self.max_idle_time_ms,
            "connectTimeoutMS": self.connection_timeout_ms,
        }

        # Add TLS options if TLS is enabled (for MongoDB Atlas this is always enabled)
        if self.tls_enabled:
            options.update({
                "tls": True,
                "tlsAllowInvalidCertificates": self.tls_allow_invalid_certs,
            })
            
            # Add CA certificates file path if provided
            if self.tls_ca_file:
                options["tlsCAFile"] = self.tls_ca_file

        return options
    
    def __str__(self) -> str:
        """Return a string representation of the configuration (without sensitive data)."""
        # Create a safe URI for logging (hide credentials)
        parsed = urllib.parse.urlparse(self.uri)
        if '@' in parsed.netloc:
            auth, host = parsed.netloc.split('@')
            safe_netloc = f"***:***@{host}"
            parsed = parsed._replace(netloc=safe_netloc)
            safe_uri = urllib.parse.urlunparse(parsed)
        else:
            safe_uri = self.uri
            
        return (
            f"DatabaseConfig(uri={safe_uri}, "
            f"db_name={self.db_name}, "
            f"max_pool_size={self.max_pool_size}, "
            f"min_pool_size={self.min_pool_size}, "
            f"tls_enabled={self.tls_enabled})"
        )


# Create a singleton instance
_config_instance = None


def get_database_config() -> DatabaseConfig:
    """
    Get the singleton instance of DatabaseConfig.
    Returns: DatabaseConfig instance
    """
    global _config_instance
    if _config_instance is None:
        _config_instance = DatabaseConfig()
    return _config_instance

