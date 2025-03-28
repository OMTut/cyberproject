import os
import requests
import time
from typing import Dict, Any
import logging
import asyncio

class LLMService:
    def __init__(self):
        self.api_token = os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_token:
            raise ValueError("HUGGINGFACE_API_KEY not found in environment variables")
        
        self.api_url = "https://api-inference.huggingface.co/models/facebook/opt-125m"
        self.api_url = "https://api-inference.huggingface.co/models/gpt2"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        self.logger = logging.getLogger(__name__)

        # Retry configuration
        self.max_retries = 5
        self.initial_backoff = 1  # Initial backoff in seconds

    async def generate_response(self, prompt: str) -> Dict[str, Any]:
        """
        Generate a response using the Hugging Face Inference API.
        Args: prompt (str): The input prompt for the model
        Returns: Dict: Response containing generated text or error message
        """
        try:
            # Prepare the payload
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_length": 150,
                    "temperature": 0.7,
                    "top_p": 0.95,
                    "return_full_text": False
                }
            }

            # Make the API call using asyncio to run in an async context
            response = await asyncio.to_thread(
                lambda: requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30  # Add timeout to prevent hanging
                )
            )
            response.raise_for_status()  # Raise exception for bad status codes

            # Process the response
            result = response.json()
            
            # Handle the response format
            if isinstance(result, list) and len(result) > 0:
                return {"generated_text": result[0].get("generated_text", "")}
            
            return {"generated_text": "No response generated"}

        except requests.exceptions.RequestException as e:
            self.logger.error(f"API request failed: {str(e)}")
            return {"error": f"Failed to generate response: {str(e)}"}
        except Exception as e:
            self.logger.error(f"Error generating response: {str(e)}")
            return {"error": f"An unexpected error occurred: {str(e)}"}
    
    async def health_check(self) -> Dict[str, str]:
        """
        Check if the API is accessible.
        Returns: Dict: Status message
        """
        try:
            # Simple request with minimal content to check API connectivity
            payload = {"inputs": "Hello"}
            
            response = await asyncio.to_thread(
                lambda: requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=10
                )
            )
            
            if response.status_code == 200:
                return {"status": "ok", "message": "LLM service is connected"}
            else:
                return {
                    "status": "error", 
                    "message": f"LLM service returned status code: {response.status_code}"
                }
                
        except Exception as e:
            return {"status": "error", "message": f"LLM service connection failed: {str(e)}"}