import uuid
from app.core.anonymizer import PIIAnonymizer
from app.core.analyzer import PIIHandler
from app.core.vault import SecureVault
from app.core.logger import AuditLogger

class ShieldEngine:
    def __init__(self):
        self.handler = PIIHandler()
        self.anonymizer = PIIAnonymizer()
        self.vault = SecureVault()
        self.audit = AuditLogger()
    
    def _remove_overlaps(self, analysis_result):
        sorted_results = sorted(analysis_result, key=lambda x: x.end - x.start, reverse=True)
        filtered_results = []
        for result in sorted_results:
            is_overlapping = False
            for filtered in filtered_results:
                if result.start >= filtered.start and result.end <= filtered.end:
                    is_overlapping = True
                    break
            if not is_overlapping:
                filtered_results.append(result)
        return filtered_results

    def protect_prompt(self, session_id: str, prompt: str, mode: str = "replace") -> str:
        try:
            # 1. Analyze text for PII
            analysis_result = self.handler.analyze_text(prompt)

            if not analysis_result:
                return prompt 
            
            # 2. Log violations
            for res in analysis_result:
                self.audit.log_violation(session_id, res.entity_type)

            cleaned_results = self._remove_overlaps(analysis_result)

            # 3. Apply Privacy Logic
            if mode == "replace":
                result = sorted(cleaned_results, key=lambda x: x.start, reverse=True)
                masked_prompt = prompt
                for res in result:
                    original_val = prompt[res.start:res.end]
                    placeholder = self.vault.store_secret(session_id, original_val, res.entity_type)
                    masked_prompt = masked_prompt[:res.start] + placeholder + masked_prompt[res.end:]
                return masked_prompt
            
            else:
                return self.anonymizer.anonymize(prompt, cleaned_results, mode=mode)

        except Exception as e:
            # --- FAIL-CLOSED LOGIC STARTS HERE ---
            # Log the actual error for the developer to see
            self.audit.logger.error(f"CRITICAL SYSTEM FAILURE: {str(e)}")
            
            # Return a blocked message. 
            # NEVER return the original 'prompt' here.
            return "[SECURITY BLOCK: The privacy engine encountered an error. Request halted to prevent data leakage.]"
        
    def reconstruct_response(self, session_id: str, llm_response: str) -> str:
        return self.vault.retrieve_secret(session_id, llm_response)