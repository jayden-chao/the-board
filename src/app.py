from crew import TheBoard, load_prompts
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel


perspective_prompts = load_prompts('perspectives')

def get_perspective_prompt(perspective):
    return perspective_prompts['perspectives'][perspective]

perspective = "contrarian"
board = TheBoard(get_perspective_prompt(perspective))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageInput(BaseModel):
    content: str

SESSIONS = {

}

@app.post("/sessions", status_code=201)
def createSession():
    session_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()


    SESSIONS[session_id] = {
        "id": session_id,
        "created_at": created_at,
        "messages": []
    }

    return {
        "id": session_id,
        "created_at": created_at
    }

@app.get("/sessions/{session_id}")
def sessionInfo(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found!")
    
    session = SESSIONS[session_id]

    return {
        "id": session["id"],
        "created_at": session["created_at"],
        "message_count": len(session["messages"])
    }

@app.post("/sessions/{session_id}/messages", status_code=201)
def boardResponse(session_id: str, input_message: MessageInput):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found!")
    
    content = input_message.content.strip()
    if not content:
        raise HTTPException(status_code=400, detail="No message content!")
    
    user_message = {
        "id": str(uuid4()),
        "role": "user",
        "session_id": session_id,
        "content": content,
        "created_at": datetime.utcnow().isoformat()
    }

    SESSIONS[session_id]["messages"].append(user_message)

    response = board.run_pipeline(content)

    board_message = {
        "id": str(uuid4()),
        "role": "board",
        "session_id": session_id,
        "content": response,
        "created_at": datetime.utcnow().isoformat()
    }

    SESSIONS[session_id]["messages"].append(board_message)


    return board_message

@app.get("/sessions/{session_id}/messages", status_code=200)
def getChatHistory(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found!")
    
    return SESSIONS[session_id]["messages"]

    
@app.delete("/sessions/{session_id}", status_code=204)
def deleteSession(session_id: str):
    if session_id not in SESSIONS:
        raise HTTPException(status_code=404, detail="Session not found!")
    
    del SESSIONS[session_id]