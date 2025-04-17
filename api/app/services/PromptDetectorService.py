import logging
import json
import os
import torch
import traceback
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification, DebertaV2ForSequenceClassification
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)

class PromptDetectorService:
    """
    Service for detecting potentially harmful prompts using a fine-tuned model.
    Uses a DeBERTa-v2 model hosted on Hugging Face.
    """
    
    def __init__(self):
        """Initialize the PromptDetectorService with model from Hugging Face"""
        try:
            # --- determine base paths ---
            this_file = Path(__file__).resolve()
            app_dir = this_file.parent.parent  # api/app directory
            
            # Default path for mapping file
            default_mapping_file = app_dir / "artifacts" / "id2label.json"
            
            # Allow override via env var
            mapping_file = Path(os.getenv("ID2LABEL_PATH", default_mapping_file))
            
            # Hugging Face model ID
            model_id = os.getenv("HF_MODEL_ID", "jonastuttle/NobleGuardClassifier")
            
            logger.info(f"Using model from Hugging Face: {model_id}")
            logger.info(f"Using mapping file: {mapping_file}")
            
            # --- Step 1: Load tokenizer from Hugging Face ---
            logger.info(f"Loading tokenizer from Hugging Face: {model_id}...")
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(
                    model_id,
                    subfolder="checkpoint-2320",
                    trust_remote_code=True
                )
                logger.info("Tokenizer loaded successfully")
            except Exception as e:
                logger.error(f"Error loading tokenizer: {str(e)}")
                logger.error(traceback.format_exc())
                raise RuntimeError(f"Failed to load tokenizer: {str(e)}")
            
            # --- Step 2: Load model from Hugging Face ---
            logger.info("Loading model from Hugging Face as DeBERTa-v2...")
            try:
                # Try explicit DeBERTa-v2 model class
                self.model = DebertaV2ForSequenceClassification.from_pretrained(
                    model_id,
                    subfolder="checkpoint-2320",
                    trust_remote_code=True
                )
                logger.info("Successfully loaded model as DeBERTa-v2")
            except Exception as e:
                logger.warning(f"Failed to load with explicit DeBERTa-v2: {str(e)}")
                # Fall back to AutoModel as a backup
                logger.info("Falling back to AutoModelForSequenceClassification...")
                try:
                    self.model = AutoModelForSequenceClassification.from_pretrained(
                        model_id,
                        subfolder="checkpoint-2320",
                        trust_remote_code=True,
                        ignore_mismatched_sizes=True
                    )
                    logger.info("Model loaded successfully with AutoModelForSequenceClassification")
                except Exception as e2:
                    logger.error(f"Error loading model with AutoModelForSequenceClassification: {str(e2)}")
                    logger.error(traceback.format_exc())
                    raise RuntimeError(f"Failed to load model: {str(e2)}")
            
            # --- Step 3: Load label mapping ---
            logger.info(f"Loading label mapping from {mapping_file}...")
            try:
                with open(mapping_file, "r") as f:
                    raw = json.load(f)
                self.id2label = {int(k): v for k, v in raw.items()}
                logger.info(f"Loaded {len(self.id2label)} labels from mapping file")
            except Exception as e:
                logger.error(f"Error loading label mapping: {str(e)}")
                # Use default mapping from model config as fallback
                self.id2label = self.model.config.id2label if hasattr(self.model.config, 'id2label') else {
                    0: "Adversarial Example",
                    1: "Harmful Request",
                    2: "Indirect Manipulation",
                    3: "Instruction Override",
                    4: "Jailbreak Attempt",
                    5: "Other",
                    6: "Prompt Leaking",
                    7: "Role Impersonation",
                    8: "benign"
                }
                logger.warning(f"Using default label mapping with {len(self.id2label)} labels")
            
            # --- Step 4: Move model to GPU if available ---
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            logger.info(f"Using device: {self.device}")
            self.model.to(self.device)
            
            logger.info("PromptDetectorService initialization complete")
            
        except Exception as e:
            logger.error(f"Error initializing PromptDetectorService: {str(e)}")
            logger.error(traceback.format_exc())
            raise RuntimeError(f"Failed to initialize PromptDetectorService: {str(e)}")
    
    def analyze_prompt(self, prompt_text: str) -> Dict[str, Any]:
        """
        Analyze a prompt text for potential attacks
        
        Args:
            prompt_text: The text prompt to analyze
            
        Returns:
            Dict containing analysis results (isAttack, attackType, confidence, matches)
        """
        if not prompt_text:
            logger.warning("Empty prompt text provided for analysis")
            return {"isAttack": False, "attackType": None, "confidence": 0.0, "matches": []}
            
        return self._analyze_with_ml(prompt_text)
    
    def _analyze_with_ml(self, prompt_text: str) -> Dict[str, Any]:
        """
        Analyze prompt text using the ML model
        
        Args:
            prompt_text: The text prompt to analyze
            
        Returns:
            Dict containing analysis results
        """
        try:
            # Tokenize input
            inputs = self.tokenizer(
                prompt_text,
                return_tensors="pt",
                truncation=True,
                padding="max_length",
                max_length=512
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get model prediction
            self.model.eval()
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Process outputs
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
            idx = int(torch.argmax(probs, dim=1).item())
            confidence = float(probs[0, idx].item())
            label = self.id2label.get(idx)
            
            logger.info(f"Predicted label: {label}, confidence: {confidence:.4f}")
            
            # Format the result
            if label and label.lower() == "benign":
                logger.info("Prompt classified as benign")
                return {"isAttack": False, "attackType": None, "confidence": confidence, "matches": []}
            else:
                # Map model's attack type to standardized categories
                attack_type = self._normalize_attack_type(label)
                logger.info(f"Prompt classified as attack: {attack_type}")
                return {
                    "isAttack": True, 
                    "attackType": attack_type, 
                    "confidence": confidence, 
                    "matches": []
                }
        except Exception as e:
            logger.error(f"Error analyzing prompt: {str(e)}")
            logger.error(traceback.format_exc())
            # Return conservative result on error (not an attack)
            return {"isAttack": False, "attackType": None, "confidence": 0.0, "matches": []}
    
    def _normalize_attack_type(self, attack_type: Optional[str]) -> str:
        """
        Normalize attack types to standardized categories
        
        Args:
            attack_type: The raw attack type label from the model
            
        Returns:
            Standardized attack type category
        """
        if not attack_type:
            return "other"
            
        # Mapping from model's attack types to standardized categories
        mappings = {
            "adversarial example": "prompt_injection",
            "harmful request": "prompt_injection", 
            "indirect manipulation": "jailbreak",
            "instruction override": "jailbreak",
            "jailbreak attempt": "jailbreak",
            "prompt leaking": "data_exfiltration",
            "role impersonation": "unauthorized_access",
            "other": "other"
        }
        
        # Normalize to lowercase for matching
        normalized = attack_type.lower()
        
        # Return mapped category or "other" if not found
        return mappings.get(normalized, "other")
