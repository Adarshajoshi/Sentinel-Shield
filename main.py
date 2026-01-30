import uuid
from fastapi import FastAPI, HTTPException,Request
from app.api import MaskRequest, MaskResponse, RehydrateRequest
from app.core.engine import ShieldEngine
import time

app = FastAPI(
    title="sentinel-shield",
    description="A PII protection layer for LLM applications"
)

engine=ShieldEngine()

@app.get("/")
def root():
    return {"message":"sentinel-shield is up and running!"}

@app.post( "/mask",response_model=MaskResponse)
async def mask_pii(request:MaskRequest):
    try:
        session_id=request.session_id or str(uuid.uuid4())
        masked_text=engine.protect_prompt(session_id,request.prompt)
        return MaskResponse(masked_text=masked_text,
                            session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.post("/rehydrate")
async def rehydrate_text(request:RehydrateRequest):
    try:
        final_text=engine.reconstruct_response(request.session_id,request.llm_response)
        return {"rehydrated_text":final_text}
    except Exception as e:
        raise HTTPException(status_code=500,detail=str(e))
    
@app.middleware("http")
async def add_process_time_header(request:Request,call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    # Add the time it took to the response headers
    response.headers["X-Process-Time"] = f"{process_time:.4f} sec"
    return response