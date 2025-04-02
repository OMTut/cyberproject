"""
Custom exceptions for database operations.
This module contains custom exception classes used throughout the database service layer
to provide more specific error handling for database-related issues.
"""

class DatabaseConnectionError(Exception):
    """
    Exception raised for database connection failures.
    
    This exception is raised when the application fails to establish 
    a connection to the database, such as connection timeouts, 
    authentication failures, or network issues.
    
    Attributes:
        message (str): Explanation of the error
        original_error (Exception, optional): The original exception that caused this error
    """
    
    def __init__(self, message, original_error=None):
        self.message = message
        self.original_error = original_error
        super().__init__(self.message)


class ConfigurationError(Exception):
    """
    Exception raised for database configuration issues.
    
    This exception is raised when there are problems with the database
    configuration, such as missing or invalid environment variables,
    malformed connection strings, or invalid configuration parameters.
    
    Attributes:
        message (str): Explanation of the error
        param (str, optional): Name of the configuration parameter causing the issue
    """
    
    def __init__(self, message, param=None):
        self.message = message
        self.param = param
        if param:
            self.message = f"{message} (parameter: {param})"
        super().__init__(self.message)


class DatabaseOperationError(Exception):
    """
    Exception raised for general database operation failures.
    
    This exception is raised when a database operation fails, such as
    failed queries, write operations, transactions, or other database
    interactions that don't succeed.
    
    Attributes:
        message (str): Explanation of the error
        operation (str, optional): The database operation that failed
        original_error (Exception, optional): The original exception that caused this error
    """
    
    def __init__(self, message, operation=None, original_error=None):
        self.message = message
        self.operation = operation
        self.original_error = original_error
        
        if operation:
            self.message = f"{message} (operation: {operation})"
            
        super().__init__(self.message)