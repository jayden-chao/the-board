from crew import TheBoard, load_prompts

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

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

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message")

    if not message:
        return { "reply": "No message provided." }

    result = board.run_pipeline(message)

    try:
        reply = result["tasks_output"][-1]["raw"]
    except (KeyError, TypeError, IndexError):
        reply = str(result)

    return { "reply": reply }