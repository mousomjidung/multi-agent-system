"""
FastAPI endpoints.
POST /chat     — AI conversation
POST /execute  — Multi-step workflow
GET  /tasks    — Direct Firestore read
GET  /schedule — Direct Firestore read
GET  /notes    — Direct Firestore read
GET  /health   — Health check
"""
import os, traceback
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from google.genai import types
from agents.agent_definition import runner, session_service
from database.firestore_client import list_tasks, list_events, list_notes

router = APIRouter()

class ChatReq(BaseModel):
    message: str
    session_id: str = ""

class ChatRes(BaseModel):
    response: str
    session_id: str

class ExecReq(BaseModel):
    instruction: str

class ExecRes(BaseModel):
    response: str
    session_id: str

@router.get("/health")
async def health():
    return {"status": "healthy", "project": os.environ.get("GOOGLE_CLOUD_PROJECT", "")}

@router.post("/chat", response_model=ChatRes)
async def chat(req: ChatReq):
    try:
        sid = req.session_id or f"s_{os.urandom(4).hex()}"
        if not await session_service.get_session(app_name="multi_agent_system", user_id="user", session_id=sid):
            await session_service.create_session(app_name="multi_agent_system", user_id="user", session_id=sid)
        msg = types.Content(role="user", parts=[types.Part.from_text(text=req.message)])
        text = ""
        async for event in runner.run_async(user_id="user", session_id=sid, new_message=msg):
            if event.is_final_response() and event.content and event.content.parts:
                for p in event.content.parts:
                    if p.text:
                        text += p.text
        return ChatRes(response=text or "Done.", session_id=sid)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, detail=str(e))

@router.post("/execute", response_model=ExecRes)
async def execute(req: ExecReq):
    try:
        sid = f"w_{os.urandom(4).hex()}"
        await session_service.create_session(app_name="multi_agent_system", user_id="user", session_id=sid)
        msg = types.Content(role="user", parts=[types.Part.from_text(text=req.instruction)])
        text = ""
        async for event in runner.run_async(user_id="user", session_id=sid, new_message=msg):
            if event.is_final_response() and event.content and event.content.parts:
                for p in event.content.parts:
                    if p.text:
                        text += p.text
        return ExecRes(response=text or "Workflow done.", session_id=sid)
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(500, detail=str(e))

@router.get("/tasks")
async def get_tasks(status: str = ""):
    return {"tasks": list_tasks(status=status)}

@router.get("/schedule")
async def get_schedule(date: str = ""):
    return {"events": list_events(date=date)}

@router.get("/notes")
async def get_notes(tag: str = ""):
    return {"notes": list_notes(tag=tag)}
