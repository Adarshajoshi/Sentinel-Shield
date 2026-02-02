import hashlib
from app.core.config import CONFIDENCE_THRESHOLD

class PIIAnonymizer:
    def __init__(self, mode="replace"):
        self.mode = mode  # Options: "replace", "redact", "hash" 

    def anonymize(self, text: str, entity_type: str, index: int) -> str:
        if self.mode == "redact":
            return "[REDACTED]"
        
        if self.mode == "hash":
            # Creates a unique, non-reversible ID for the same PII 
            hash_obj = hashlib.md5(text.encode())
            return f"[HASH_{hash_obj.hexdigest()[:8]}]"
            
        # Default: replace with placeholders
        return f"[{entity_type}_{index}]"