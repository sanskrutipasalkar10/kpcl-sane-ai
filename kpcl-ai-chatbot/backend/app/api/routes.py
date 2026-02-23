from fastapi import APIRouter, HTTPException
from app.models.request import ChatRequest
from app.models.response import ChatResponse
from app.agents.code_agent import run_data_agent 

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        response_data = await run_data_agent(request.message, request.user_id)
        return response_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))