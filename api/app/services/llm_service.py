import os
import requests
import logging
from typing import Dict, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.api_token = os.getenv("HUGGINGFACE_API_TOKEN")
        if not self.api_token:
            raise ValueError("HUGGINGFACE_API_TOKEN not found in environment variables")
        self.api_url = "https://api-inference.huggingface.co/models/"
        self.model_name = "gpt2"  # Default model, can be changed
        
    def _validate_input(self, text: str) -> bool:
        """
        Validate input text
        Returns True if input is valid, False otherwise
        """
        if not text or not isinstance(text, str):
            return False
        if len(text.strip()) == 0:
            return False
        # Add any other validation rules here
        return True

    def _sanitize_input(self, text: str) -> str:
        """
        Sanitize input text
        """
        # Basic sanitization
        text = text.strip()
        # Add any other sanitization rules here
        return text

    async def generate_response(self, text: str) -> Dict:
        """
        Generate response from the LLM model
        """
        try:
            if not self._validate_input(text):
                raise ValueError("Invalid input text")
            
            sanitized_text = self._sanitize_input(text)
            
            headers = {
                "Authorization": f"Bearer {self.api_token}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "inputs": sanitized_text,
                "parameters": {
                    "max_length": 100,
                    "temperature": 0.7,
                    "top_p": 0.9,
                }
            }
            
            response = requests.post(
                f"{self.api_url}{self.model_name}",
                headers=headers,
                json=payload
            )
            
            if response.status_code != 200:
                logger.error(f"API request failed: {response.text}")
                raise Exception("Failed to generate response from LLM")
            
            return response.json()
            
        except Exception as e:
            logger.error(f"Error in generate_response: {str(e)}")
            raise

    def set_model(self, model_name: str) -> None:
        """
        Change the model being used
        """
        self.model_name = model_name

