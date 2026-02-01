import uuid
from app.core.anonymizer import PIIAnonymizer
from app.core.analyzer import PIIHandler
from app.core.vault import SecureVault
from app.core.logger import AuditLogger

class ShieldEngine:
    def __init__(self,mode="replace"):
        self.handler=PIIHandler()
        self.anonymizer = PIIAnonymizer(mode=mode)
        self.vault=SecureVault()
        self.audit = AuditLogger()
    
    def _remove_overlaps(self,analysis_result):
        #Filters out entities that overlap, keeping the longest match
        #sort out by length
        sorted_results = sorted(analysis_result, key=lambda x: x.end - x.start, reverse=True)
        filtered_results=[]

        for result in sorted_results:
            is_overlapping=False
            for filtered in filtered_results:
                if result.start >=filtered.start and result.end<=filtered.end:
                    is_overlapping=True
                    break
            
            if not is_overlapping:
                filtered_results.append(result)
        return filtered_results

    def protect_prompt(self,session_id:str,prompt:str)->str:
        #get list of PII from analyzer
        analysis_result=self.handler.analyze_text(prompt)

        if not analysis_result:
            return prompt 
        
        #log each detected entity
        for res in analysis_result:
            self.audit.log_violation(session_id, res.entity_type)

        #cleaned results
        cleaned_results=self._remove_overlaps(analysis_result)

        #sort by start index in descending order
        result=sorted(cleaned_results,key=lambda x:x.start,reverse=True)

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
    

    