import logging
import re
from typing import Dict, Any, Tuple, List

logger = logging.getLogger(__name__)

class PromptDetectorService:
    """
    A service for detecting potentially malicious prompts.
    This is a simple implementation that will be replaced with a more sophisticated ML model later.
    """
    
    def __init__(self):
        # Basic dictionary of attack types and their associated keywords
        self.attack_patterns = {
            "prompt injection": [
                "ignore previous instructions", 
                "disregard", 
                "instead",
                "system prompt",
                "system message",
                "you are now",
                "new role"
            ],
            "jailbreak": [
                "DAN", 
                "developer mode", 
                "ignore ethics",
                "no moral",
                "bypass",
                "restrictions"
            ],
            "data exfiltration": [
                "reveal source code", 
                "show system", 
                "what is your training data",
                "how were you trained",
                "display internal"
            ],
            "malicious code": [
                "eval(", 
                "exec(", 
                "system(",
                "subprocess",
                "os.system",
                "</script>"
            ]
        }
    
    def analyze_prompt(self, prompt_text: str) -> Dict[str, Any]:
        """
        Analyzes a prompt for potential attacks.
        Args:
            prompt_text: The text of the prompt to analyze
        Returns:
            Dict containing analysis results:
            {
                "isAttack": bool,
                "type": str or None,
                "confidence": float (0-1),
                "matches": List of detected patterns
            }
        """
        prompt_lower = prompt_text.lower()
        
        # Check for attack patterns
        detected_attacks = []
        matched_patterns = []
        
        for attack_type, patterns in self.attack_patterns.items():
            for pattern in patterns:
                if pattern.lower() in prompt_lower:
                    detected_attacks.append(attack_type)
                    matched_patterns.append(pattern)
                    logger.warning(f"Potential {attack_type} attack detected: '{pattern}' found in prompt")
                    print(f"ALERT: Potential {attack_type} attack detected: '{pattern}' found in prompt")
        
        # Calculate results
        if detected_attacks:
            # Get the most frequent attack type
            attack_type = max(set(detected_attacks), key=detected_attacks.count)
            
            # Simple confidence calculation based on number of matches
            # In a real system, this would use ML model confidence scores
            confidence = min(0.5 + (len(matched_patterns) * 0.1), 0.95)
            
            return {
                "isAttack": True,
                "attackType": attack_type,
                "confidence": confidence,
                "matches": matched_patterns
            }
        else:
            return {
                "isAttack": False,
                "attackType": None,
                "confidence": 0.0,
                "matches": []
            }
    
    # TODO: Add more sophisticated detection using ML models
    def _analyze_with_ml(self, prompt_text: str) -> Dict[str, Any]:
        """
        Future implementation placeholder for ML-based analysis.
        This would integrate with a trained model to perform more accurate detection.
        Args:
            prompt_text: The text of the prompt to analyze
        Returns:
            Dict containing ML analysis results
        """
        # This is where ML model integration would happen
        # For example:
        # - Tokenize the input
        # - Run it through the model
        # - Interpret confidence scores
        # - Return structured results
        pass