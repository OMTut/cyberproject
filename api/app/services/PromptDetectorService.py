import logging
import json
import os
import torch
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForSequenceClassification
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class PromptDetectorService:
    def __init__(self):
        # --- determine base paths ---
        this_file = Path(__file__).resolve()
        repo_root = this_file.parents[3]  

        # allow overrides via env vars
        model_dir = Path(os.getenv("MODEL_PATH", repo_root / "model"))
        mapping_file = Path(os.getenv("ID2LABEL_PATH",
                                      repo_root / "artifacts" / "id2label.json"))

        # --- load tokenizer & model from that directory ---
        self.tokenizer = AutoTokenizer.from_pretrained(str(model_dir))
        self.model     = AutoModelForSequenceClassification.from_pretrained(str(model_dir))

        # --- load id2label mapping ---
        with open(mapping_file, "r") as f:
            raw = json.load(f)
        self.id2label = {int(k): v for k, v in raw.items()}

        # move model to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    def analyze_prompt(self, prompt_text: str) -> Dict[str, Any]:
        return self._analyze_with_ml(prompt_text)

    def _analyze_with_ml(self, prompt_text: str) -> Dict[str, Any]:
        # same inference logic as before
        inputs = self.tokenizer(
            prompt_text,
            return_tensors="pt",
            truncation=True,
            padding="max_length",
            max_length=512
        )
        inputs = {k: v.to(self.device) for k, v in inputs.items()}

        self.model.eval()
        with torch.no_grad():
            outputs = self.model(**inputs)

        probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        idx = int(torch.argmax(probs, dim=1).item())
        confidence = float(probs[0, idx].item())
        label = self.id2label.get(idx)

        if label and label.lower() == "benign":
            return {"isAttack": False, "attackType": None, "confidence": confidence, "matches": []}
        return {"isAttack": True, "attackType": label, "confidence": confidence, "matches": []}