import uuid

class SecureVault:
    def __init__(self):
        self._storage = {}
    
    def store_secret(self,session_id:str,original_value:str,entity_type:str)->str:
        if session_id not in self._storage:
            self._storage[session_id] = {}
        
        count = len(self._storage[session_id]) + 1
        placeholder = f"[{entity_type}_{count}]"
        
        self._storage[session_id][placeholder] = original_value
        return placeholder
    
    def retrieve_secret(self,session_id:str,anonymized_text:str)->str:
        if session_id not in self._storage:
            return anonymized_text
        
        rehydrated_text= anonymized_text
        for placeholder, original_value in self._storage[session_id].items():
            rehydrated_text = rehydrated_text.replace(placeholder, original_value)

        return rehydrated_text
    
    def clear_session(self,session_id:str)->None:
        if session_id in self._storage:
            del self._storage[session_id]