import os
import sys
import secrets
from datetime import datetime
import uvicorn
from fastapi import FastAPI, HTTPException, status, Depends, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import Response
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import COMPANY, MOCK_USERS, ROLE_ACCESS
from agents.orchestrator import KaranAgenticRAG
from tools.mcp_server import load_drafts, generate_ics_content, MAIL_SENDER

app = FastAPI(title=f"{COMPANY} API Backend")

# CORS middleware for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate the Agent
agent = KaranAgenticRAG()

# Simple token storage (in-memory for mock auth)
# Maps token -> user_data
ACTIVE_SESSIONS: Dict[str, Dict[str, Any]] = {}

CHATS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tools", "chats.json")

def load_chats() -> Dict[str, Any]:
    if os.path.exists(CHATS_FILE):
        try:
            with open(CHATS_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_chats(chats: Dict[str, Any]):
    os.makedirs(os.path.dirname(CHATS_FILE), exist_ok=True)
    with open(CHATS_FILE, "w") as f:
        json.dump(chats, f, indent=4)

import json

class LoginRequest(BaseModel):
    email: str
    password: str

class ChatMessageRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

# Auth Helper
def get_current_user(authorization: Optional[str] = Header(None)) -> Dict[str, Any]:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authentication header"
        )
    token = authorization.split(" ")[1]
    if token not in ACTIVE_SESSIONS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid token"
        )
    return ACTIVE_SESSIONS[token]

@app.post("/api/login")
def login(req: LoginRequest):
    email = req.email.strip()
    record = MOCK_USERS.get(email)
    if record and record["password"] == req.password:
        token = secrets.token_hex(16)
        user_data = {
            "name": record["name"],
            "role": record["role"],
            "user_id": record["user_id"],
            "email": email
        }
        ACTIVE_SESSIONS[token] = user_data
        return {"success": True, "token": token, "user": user_data}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication failed."
        )

@app.post("/api/logout")
def logout(authorization: Optional[str] = Header(None)):
    if authorization and authorization.startswith("Bearer "):
        token = authorization.split(" ")[1]
        if token in ACTIVE_SESSIONS:
            del ACTIVE_SESSIONS[token]
    return {"success": True}

@app.get("/api/chats")
def get_chats(user: Dict[str, Any] = Depends(get_current_user)):
    chats = load_chats()
    user_chats = [c for c in chats.values() if c.get("user_email") == user["email"]]
    user_chats.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return user_chats

@app.get("/api/chats/{session_id}")
def get_chat_session(session_id: str, user: Dict[str, Any] = Depends(get_current_user)):
    chats = load_chats()
    if session_id not in chats:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    session = chats[session_id]
    if session.get("user_email") != user["email"]:
        raise HTTPException(status_code=403, detail="Access denied to this chat session")
        
    return session

@app.delete("/api/chats/{session_id}")
def delete_chat_session(session_id: str, user: Dict[str, Any] = Depends(get_current_user)):
    chats = load_chats()
    if session_id not in chats:
        raise HTTPException(status_code=404, detail="Chat session not found")
        
    session = chats[session_id]
    if session.get("user_email") != user["email"]:
        raise HTTPException(status_code=403, detail="Access denied to this chat session")
        
    del chats[session_id]
    save_chats(chats)
    return {"success": True}

@app.post("/api/chats/message")
def chat_message(req: ChatMessageRequest, user: Dict[str, Any] = Depends(get_current_user)):
    chats = load_chats()
    session_id = req.session_id

    if not session_id or session_id not in chats:
        session_id = secrets.token_hex(8)
        title = req.message[:25] + ("..." if len(req.message) > 25 else "")
        chats[session_id] = {
            "id": session_id,
            "user_email": user["email"],
            "title": title.upper(),
            "messages": [],
            "timestamp": datetime.now().isoformat()
        }

    session = chats[session_id]
    if session.get("user_email") != user["email"]:
        raise HTTPException(status_code=403, detail="Access denied to this chat session")

    # Append user message
    session["messages"].append({
        "role": "user",
        "content": req.message
    })

    try:
        # Run agent query
        response = agent.query(
            user_query=req.message,
            chat_history=session["messages"][:-1],
            role=user["role"]
        )
    except Exception as e:
        response = f"An error occurred while reasoning: {str(e)}"

    # Append assistant message
    session["messages"].append({
        "role": "assistant",
        "content": response
    })
    
    session["timestamp"] = datetime.now().isoformat()
    save_chats(chats)

    return {"session_id": session_id, "response": response}

@app.get("/api/meetings")
def get_meetings(user: Dict[str, Any] = Depends(get_current_user)):
    try:
        drafts = load_drafts()
        return list(drafts.values())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load meetings: {str(e)}")

@app.get("/api/meetings/{meeting_id}/ics")
def download_ics(meeting_id: str):
    try:
        drafts = load_drafts()
        if meeting_id not in drafts:
            raise HTTPException(status_code=404, detail="Meeting draft not found")
        
        meeting = drafts[meeting_id]
        ics_content = generate_ics_content(meeting, MAIL_SENDER)
        
        return Response(
            content=ics_content,
            media_type="text/calendar",
            headers={
                "Content-Disposition": f"attachment; filename=invite-{meeting_id}.ics"
            }
        )
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate calendar file: {str(e)}")

# Mount UI static folder
ui_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ui")
if os.path.exists(ui_path):
    app.mount("/", StaticFiles(directory=ui_path, html=True), name="ui")

if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    host = os.getenv("HOST", "0.0.0.0")
    uvicorn.run("server:app", host=host, port=port, reload=False)
