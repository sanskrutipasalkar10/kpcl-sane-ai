from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "admin"

class ChatResponse(BaseModel):
    answer: str
    confidence: Optional[str] = None
    reasoning_path: Optional[str] = None
    error: Optional[str] = None
    
    # 🚀 THE FIX: Tell FastAPI to allow the JSON graph to pass through to React
    graph_json: Optional[str] = None
    
    # We can leave this here just in case any old code still references it
    graph_base64: Optional[str] = None