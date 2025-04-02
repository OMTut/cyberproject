import logging
import urllib.parse
from typing import Tuple, Optional, Dict, Any

logger = logging.getLogger(__name__)

def format_mongodb_uri(uri: str) -> str:
    """
    Format MongoDB URI with proper URL encoding for username and password.
    
    This enhanced version includes:
    - Better debug logging for troubleshooting
    - Improved handling of edge cases (multiple @ characters, special chars)
    - Compatible with DatabaseConfig expectations
    - Fixed value unpacking issues
    
    Args:
        uri: The MongoDB connection URI string
        
    Returns:
        Properly formatted MongoDB URI with encoded credentials
        
    Raises:
        ValueError: If URI is empty or malformed
    """
    if not uri:
        logger.error("MONGODB_URI not found")
        raise ValueError("MONGODB_URI variable is required")
    
    # Log masked URI for debugging (hide credentials)
    masked_uri = _get_masked_uri_for_logging(uri)
    logger.debug(f"Processing MongoDB URI: {masked_uri}")
    
    try:
        # Check if the URI has the mongodb+srv:// or mongodb:// protocol
        if not uri.startswith(('mongodb+srv://', 'mongodb://')):
            logger.warning("URI doesn't start with mongodb:// or mongodb+srv://")
            return uri
            
        # Extract protocol
        protocol_separator = uri.find('://')
        if protocol_separator == -1:
            logger.error("Invalid URI format: protocol separator '://' not found")
            return uri
            
        protocol = uri[:protocol_separator]
        logger.debug(f"Protocol: {protocol}")
        
        # Find the position after the protocol://
        auth_start = protocol_separator + 3
        
        # Look for the @ that separates credentials from host
        # We need to find the last @ before the first / after the protocol
        rest_of_uri = uri[auth_start:]
        
        # Parse the URI components safely
        parsed_components = _parse_uri_components(protocol, rest_of_uri)
        if not parsed_components:
            logger.debug("No credentials found or no changes needed to URI")
            return uri
            
        credentials, host_and_options = parsed_components
        logger.debug(f"Found credentials and host components (host: {host_and_options[:10]}...)")
        
        # Parse and encode credentials
        result_uri = _encode_credentials(protocol, credentials, host_and_options)
        
        # Log success (with masked credentials)
        masked_result = _get_masked_uri_for_logging(result_uri)
        logger.debug(f"Successfully formatted URI: {masked_result}")
        return result_uri
        
    except Exception as e:
        logger.error(f"Error formatting MongoDB URI: {str(e)}", exc_info=True)
        raise ValueError(f"Failed to format MongoDB URI: {str(e)}")

def _get_masked_uri_for_logging(uri: str) -> str:
    """Create a safe version of the URI for logging by hiding credentials."""
    try:
        parsed = urllib.parse.urlparse(uri)
        netloc = parsed.netloc
        
        if '@' in netloc:
            # Split at the last @ character
            parts = netloc.rsplit('@', 1)
            if len(parts) == 2:
                # Replace credentials with ***:***
                masked_netloc = f"***:***@{parts[1]}"
                masked_parts = list(parsed)
                masked_parts[1] = masked_netloc
                return urllib.parse.urlunparse(tuple(masked_parts))
        
        return uri
    except Exception as e:
        logger.warning(f"Could not mask URI for logging: {str(e)}")
        return "***[uri]***"

def _parse_uri_components(protocol: str, rest_of_uri: str) -> Optional[Tuple[str, str]]:
    """
    Parse URI into credentials and host components.
    
    Args:
        protocol: The MongoDB protocol (mongodb:// or mongodb+srv://)
        rest_of_uri: The part of the URI after the protocol
        
    Returns:
        A tuple of (credentials, host_and_options) or None if no credentials
    """
    # Find the path part (first / after credentials and host)
    path_pos = rest_of_uri.find('/')
    
    # Determine search scope (where to look for the @ character)
    if path_pos == -1:
        search_scope = rest_of_uri
    else:
        search_scope = rest_of_uri[:path_pos]
        
    # Find the correct @ separator (the last @ in the search scope)
    at_pos = search_scope.rfind('@')
    logger.debug(f"@ position in URI: {at_pos}")
    
    if at_pos == -1:
        # No credentials in URI
        logger.debug("No credentials found in URI")
        return None
        
    # We have credentials
    credentials = rest_of_uri[:at_pos]
    host_and_options = rest_of_uri[at_pos+1:]
    logger.debug(f"Credentials length: {len(credentials)}, Host options length: {len(host_and_options)}")
    
    return credentials, host_and_options

def _encode_credentials(protocol: str, credentials: str, host_and_options: str) -> str:
    """
    Encode credentials and rebuild the URI.
    
    Args:
        protocol: The MongoDB protocol (mongodb:// or mongodb+srv://)
        credentials: The credentials part (username:password)
        host_and_options: Everything after the @ in the URI
        
    Returns:
        The rebuilt URI with properly encoded credentials
    """
    # Find the username/password separator (first colon)
    # Use split with maxsplit=1 to handle passwords containing colons
    parts = credentials.split(':', 1)
    
    if len(parts) == 2:
        # We have both username and password
        username, password = parts
        logger.debug(f"Username length: {len(username)}, Password length: {len(password)}")
        
        # URL encode the username and password
        encoded_username = urllib.parse.quote_plus(username)
        encoded_password = urllib.parse.quote_plus(password)
        
        # Rebuild the URI with encoded credentials
        return f"{protocol}://{encoded_username}:{encoded_password}@{host_and_options}"
    else:
        # Only username, no password
        username = credentials
        logger.debug(f"Only username found (length: {len(username)}), no password")
        encoded_username = urllib.parse.quote_plus(username)
        return f"{protocol}://{encoded_username}@{host_and_options}"

def format_uri_for_config(uri: str) -> str:
    """
    Format a URI specifically for use with DatabaseConfig.
    Compatible wrapper for format_mongodb_uri.
    
    Args:
        uri: The MongoDB connection URI string
        
    Returns:
        Properly formatted MongoDB URI with encoded credentials
    """
    return format_mongodb_uri(uri)
