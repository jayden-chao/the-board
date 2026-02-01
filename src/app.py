from crew import TheBoard, load_prompts
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from uuid import uuid4
from datetime import datetime
from fastapi import HTTPException
from pydantic import BaseModel
from db import init_db, get_db, create_sessions, session_exists, delete_session

perspective_prompts = load_prompts('perspectives')

def get_perspective_prompt(perspective):
    return perspective_prompts['perspectives'][perspective]

board = TheBoard(get_perspective_prompt("contrarian"))

app = FastAPI()
init_db()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class MessageInput(BaseModel):
    content: str

class Perspective(BaseModel):
    value: str


@app.post("/perspective")
def updatePerspective(perspective: Perspective):
    global board
    board = TheBoard(get_perspective_prompt(perspective.value))


@app.post("/sessions", status_code=201)
def createSession():
    session_id = str(uuid4())
    created_at = datetime.utcnow().isoformat()

    create_sessions(session_id, created_at)

    return {
        "id": session_id,
        "created_at": created_at
    }


@app.get("/sessions/{session_id}")
def sessionInfo(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found!")
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, created_at FROM sessions WHERE id = ?",
        (session_id,)
    )
    session_row = cursor.fetchone()

    if not session_row:
        raise HTTPException(status_code=404, detail="Session not found!")

    cursor.execute(
        "SELECT COUNT(*) FROM messages WHERE session_id = ?",
        (session_id,)
    )
    message_count = cursor.fetchone()[0]

    conn.close()

    return {
        "id": session_row[0],
        "created_at": session_row[1],
        "message_count": message_count
    }


@app.post("/sessions/{session_id}/messages", status_code=201)
def boardResponse(session_id: str, input_message: MessageInput):
    if not session_exists(session_id):
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

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO messages (id, role, session_id, content, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_message["id"], user_message["role"], user_message["session_id"],
         user_message["content"], user_message["created_at"])
    )
    conn.commit()

    response = board.run_pipeline(content)

    board_message = {
        "id": str(uuid4()),
        "role": "board",
        "session_id": session_id,
        "content": str(response),
        "created_at": datetime.utcnow().isoformat()
    }

    cursor.execute(
        """
        INSERT INTO messages (id, role, session_id, content, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (board_message["id"], board_message["role"], board_message["session_id"], 
         board_message["content"], board_message["created_at"])
    )

    conn.commit()
    conn.close()

    return board_message


@app.get("/sessions/{session_id}/messages", status_code=200)
def getChatHistory(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found!")
    
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, role, session_id, content, created_at
        FROM messages
        WHERE session_id = ?
        ORDER BY created_at ASC
        """,
        (session_id,)
    )
    rows = cursor.fetchall()

    messages = []
    for row in rows:
        messages.append({
            "id": row[0],
            "role": row[1],
            "session_id": row[2],
            "content": row[3],
            "created_at": row[4],
        })
    
    conn.close()

    return messages

    
@app.delete("/sessions/{session_id}", status_code=204)
def deleteSession(session_id: str):
    if not session_exists(session_id):
        raise HTTPException(status_code=404, detail="Session not found!")
    
    delete_session(session_id)
