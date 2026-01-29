from pydantic import BaseModel,Field
from typing import Annotated

class MaskRequest(BaseModel):
    prompt:str=Field(...,example="My name is John Doe and my phone number is 123-456-7890")
    session_id:str=Field(None,example="session_12345")

class MaskResponse(BaseModel):
    masked_text:str
    session_id:str

class RehydrateRequest(BaseModel):
    session_id:str
    llm_response:str=Field(None)
