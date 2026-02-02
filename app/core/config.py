# app/core/config.py

# Score threshold to prevent over-redaction (like masking "today")
CONFIDENCE_THRESHOLD = 0.45 

# The entities we want to detect based on our initial goal [cite: 7]
SUPPORTED_ENTITIES = [
    "PERSON", 
    "EMAIL_ADDRESS", 
    "PHONE_NUMBER", 
    "LOCATION", 
    "URL",
    "DATE_TIME"
]

# Standard ID patterns for the "Tech Gap" task 
CUSTOM_PATTERNS = [
    {"name": "INTERNAL_ID", "regex": r"PROJ-[0-9]{3,6}", "score": 0.5}
]