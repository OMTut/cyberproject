import logging
import urllib.parse

logger = logging.getLogger(__name__)

def format_mongodb_uri(uri: str) -> str:
    """Format MongoDB URI with proper URL encoding for username and password."""
    if not uri:
        logger.error("MONGODB_URI not found")
        raise ValueError("MONGODB_URI variable is required")
    
    try:
        # Check if the URI has the mongodb+srv:// or mongodb:// protocol
        if uri.startswith(('mongodb+srv://', 'mongodb://')):
            # Parse the URI more carefully to handle @ in passwords
            protocol_separator = uri.find('://')
            protocol = uri[:protocol_separator]
            
            # Find the position after the protocol://
            auth_start = protocol_separator + 3
            
            # Look for the @ that separates credentials from host
            # We need to find the last @ before the first / after the protocol
            rest_of_uri = uri[auth_start:]
            path_pos = rest_of_uri.find('/')
            if path_pos == -1:
                search_scope = rest_of_uri
            else:
                search_scope = rest_of_uri[:path_pos]
                
            # Find the correct @ separator (the last @ in the search scope)
            at_pos = search_scope.rfind('@')
            
            if at_pos != -1:
                # We have credentials
                credentials = rest_of_uri[:at_pos]
                host_and_options = rest_of_uri[at_pos+1:]
                
                # Find the username/password separator
                colon_pos = credentials.find(':')
                
                if colon_pos != -1:
                    # We have both username and password
                    username = credentials[:colon_pos]
                    password = credentials[colon_pos+1:]
                    
                    # URL encode the username and password
                    encoded_username = urllib.parse.quote_plus(username)
                    encoded_password = urllib.parse.quote_plus(password)
                    
                    # Rebuild the URI with encoded credentials
                    return f"{protocol}://{encoded_username}:{encoded_password}@{host_and_options}"
                else:
                    # Only username, no password
                    encoded_username = urllib.parse.quote_plus(credentials)
                    return f"{protocol}://{encoded_username}@{host_and_options}"
            else:
                # No credentials in URI
                return uri
        else:
            logger.warning("URI doesn't start with mongodb:// or mongodb+srv://")
            return uri
    except Exception as e:
        logger.error(f"Error formatting MongoDB URI: {str(e)}")
        raise ValueError(f"Failed to format MongoDB URI: {str(e)}")