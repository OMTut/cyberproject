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
        
        #self.api_url = "https://api-inference.huggingface.co/models/google/gemma-2b-it"
        self.api_url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"
        #self.api_url = "https://api-inference.huggingface.co/models/gpt2"
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
            # Prepare the payload according to the Hugging Face Inference API documentation
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 150,  # Number of new tokens to generate
                    "temperature": 0.7,  # Controls randomness: higher values mean more random completions
                    "top_p": 0.9,  # Nucleus sampling parameter
                    "top_k": 50,  # Only sample from the top_k most likely tokens
                    "repetition_penalty": 1.2,  # Penalize repetitions
                    "do_sample": True,  # Enable sampling (set to False for deterministic output)
                    "return_full_text": False,  # Only return the newly generated text, not the prompt
                    "num_return_sequences": 1  # Number of independently computed returned sequences
                }
            }
            # Make the API call using asyncio to run in an async context
            response = await asyncio.to_thread(
                lambda: requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=60  # Add timeout to prevent hanging
                )
            )
            response.raise_for_status()  # Raise exception for bad status codes

            # Process the response
            result = response.json()
            
            # Handle the response format based on Hugging Face Inference API documentation
            if isinstance(result, list) and len(result) > 0:
                generated_text = result[0].get("generated_text", "")
                self.logger.info(f"Generated response of length: {len(generated_text)}")
                return {"generated_text": generated_text}
            elif isinstance(result, dict) and "generated_text" in result:
                # Some models return a single dict instead of a list
                self.logger.info(f"Generated response of length: {len(result['generated_text'])}")
                return {"generated_text": result["generated_text"]}
            
            self.logger.warning(f"Unexpected response format: {result}")
            return {"generated_text": "No response generated"}

        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if hasattr(e, 'response') else 'unknown'
            self.logger.error(f"HTTP error {status_code}: {str(e)}")
            
            # Handle 503 Service Unavailable (model loading) error
            if hasattr(e, 'response') and e.response.status_code == 503:
                return {"error": "The model is currently loading. Please try again in a few moments."}
            
            return {"error": f"API request failed with status {status_code}: {str(e)}"}
        except requests.exceptions.ConnectionError as e:
            self.logger.error(f"Connection error: {str(e)}")
            return {"error": "Failed to connect to the Hugging Face API. Please check your internet connection."}
        except requests.exceptions.Timeout as e:
            self.logger.error(f"Request timed out: {str(e)}")
            return {"error": "Request to Hugging Face API timed out. The service might be experiencing high demand."}
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
            # Using smallest possible request for health check
            payload = {
                "inputs": "Hello",
                "parameters": {
                    "max_new_tokens": 5,
                    "return_full_text": False
                }
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
                return {"status": "ok", "message": "LLM service is connected"}
            else:
                return {
                    "status": "error", 
                    "message": f"LLM service returned status code: {response.status_code}"
                }
                
        except Exception as e:
            return {"status": "error", "message": f"LLM service connection failed: {str(e)}"}