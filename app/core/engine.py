import uuid
from app.core.analyzer import PIIHandler
from app.core.vault import SecureVault

class ShieldEngine:
    def __init__(self):
        self.handler=PIIHandler()
        self.vault=SecureVault()

    def protect_prompt(self,session_id:str,prompt:str)->str:
        #get list of PII from analyzer
        analysis_result=self.handler.analyze_text(prompt)

        #sort by start index in descending order
        result=sorted(analysis_result,key=lambda x:x.start,reverse=True)

        masked_prompt=prompt
        for res in result:
            original_val=prompt[res.start:res.end]
            # Store in vault and get a consistent placeholder 
            placeholder = self.vault.store_secret(session_id, original_val, res.entity_type)
            # Replace the PII with the placeholder
            masked_prompt = masked_prompt[:res.start] + placeholder + masked_prompt[res.end:]
            
        return masked_prompt
    
    def reconstruct_response(self,session_id:str,llm_response:str)->str:
        """Retrieves original PII from vault and fixes the LLM response."""
        return self.vault.retrieve_secret(session_id, llm_response)
    

    