import os
from dotenv import load_dotenv
import requests
import time
from typing import Dict, Any
import logging
import asyncio
from pathlib import Path

# Get the directory containing this file
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Load environment variables from .env file in the api directory
load_dotenv(BASE_DIR / '.env')

class LLMService:
    def __init__(self, model="gpt-3.5-turbo-instruct"):  # Changed to instruct model
        # Use OpenAI API key
        self.api_token = os.getenv("OPENAI_API_KEY")
        if not self.api_token:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        # OpenAI API endpoint for completions (not chat completions)
        self.api_url = "https://api.openai.com/v1/completions"  # Changed to completions endpoint
        
        # Default model
        self.model = model
        
        # OpenAI authentication headers
        self.headers = {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json"
        }
        self.logger = logging.getLogger(__name__)

        # Retry configuration
        self.max_retries = 3  # Reduced from 5
        self.initial_backoff = 2  # Increased initial backoff

    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response using OpenAI's completions API.
        Args: prompt (str): The input prompt for the model
        Returns: Dict: Response containing generated text or error message
        """
        try:
            # Prepare the payload with minimal tokens
            payload = {
                "model": self.model,
                "prompt": prompt,  # Changed from messages format
                "max_tokens": 50,  # Reduced significantly from 150 to 50
                "temperature": 0.7,  # Controls randomness
                "top_p": 0.9      # Nucleus sampling parameter
            }
            
            # Make the API call using asyncio to run in an async context
            response = await asyncio.to_thread(
                lambda: requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30  # Reduced timeout to 30 seconds
                )
            )
            response.raise_for_status()  # Raise exception for bad status codes

            # Process the response
            result = response.json()
            
            # Handle the response format based on completions API format
            if isinstance(result, dict) and "choices" in result and len(result["choices"]) > 0:
                text = result["choices"][0].get("text", "").strip()
                self.logger.info(f"Generated response of length: {len(text)}")
                return {"generated_text": text}
            
            self.logger.warning(f"Unexpected response format: {result}")
            return {"generated_text": "No response generated"}

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else 'unknown'
            self.logger.error(f"HTTP error {status_code}: {str(e)}")
            
            # Handle specific OpenAI error codes
            if hasattr(e, 'response'):
                if e.response.status_code == 429:
                    return {"error": "Rate limit exceeded. Please verify your OpenAI account status and API key."}
                elif e.response.status_code == 400:
                    error_message = "Invalid request"
                    try:
                        error_data = e.response.json()
                        if "error" in error_data and "message" in error_data["error"]:
                            error_message = error_data["error"]["message"]
                    except:
                        pass
                    return {"error": f"OpenAI API error: {error_message}"}
            
            return {"error": f"API request failed with status {status_code}: {str(e)}"}
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error: {str(e)}")
            return {"error": "Failed to connect to the OpenAI API. Please check your internet connection."}
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Request timed out: {str(e)}")
            return {"error": "Request to OpenAI API timed out. The service might be experiencing high demand."}
        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return {"error": f"Failed to generate response: {str(e)}"}
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}"}
    
    async def health_check(self) -> Dict[str, str]:
        """
        Check if the OpenAI API is accessible.
        Returns: Dict: Status message
        """
        try:
            # Simple request with minimal content to check API connectivity
            payload = {
                "model": self.model,
                "prompt": "Hello",  # Changed from messages format
                "max_tokens": 5
            }
            
            response = await asyncio.to_thread(
                lambda: requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=10
                )
            )
            
            if response.status_code == 200:
                return {"status": "ok", "message": "OpenAI API is connected and accessible"}
            else:
                return {
                    "status": "error", 
                    "message": f"OpenAI API returned status code: {response.status_code}"
                }
                
        except Exception as e:
            return {"status": "error", "message": f"Connection to OpenAI API failed: {str(e)}"}
