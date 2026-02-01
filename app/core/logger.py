import logging
import os
from datetime import datetime

os.makedirs('logs', exist_ok=True)

class AuditLogger:
    def __init__(self):
        self.logger=logging.getLogger("SentinelAudit")
        self.logger.setLevel(logging.INFO)

        handler=logging.FileHandler(f"logs/audit_{datetime.now().strftime('%Y%m%d')}.log")
        formatter=logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    def log_violation(self,session_id:str,entity_type:str):
        """Logs that PII was detected without logging the PII itself."""
        self.logger.info(f"PRIVACY_VIOLATION_PREVENTED | Session: {session_id} | Type: {entity_type}")