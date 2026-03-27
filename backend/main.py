from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from services.rag_service import retrieve_context
from agents.graph import app_graph
from db.mongo import save_lead, get_lead

# Simple in-memory session storage for history (for Zero-Config simplicity)
sessions = {}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: str
    
@app.post("/chat")
async def chat(req: ChatRequest):
    # Initialize session if not exists
    if req.session_id not in sessions:
        sessions[req.session_id] = []
    
    chat_history = sessions[req.session_id]
    existing_lead = get_lead(req.session_id)

    # LangGraph agentic approach
    state = {
        "user_input": req.message,
        "history": chat_history,
        "context": "",
        "response": "",
        "lead": {},
        "lead_data": existing_lead,
        "intent": ""
    }
    
    # Run the graph
    result = app_graph.invoke(state)
    
    # Update memory (keep last 10 turns)
    chat_history.append({"role": "user", "content": req.message})
    chat_history.append({"role": "assistant", "content": result["response"]})
    sessions[req.session_id] = chat_history[-10:]

    # If the lead extractor or closer agents populated the lead info:
    if result.get("lead") and any(result["lead"].values()):
        save_lead(req.session_id, result["lead"])

    return {
        "response": result["response"],
        "lead": result["lead"]
    }

from routes.voice import router as voice_router
app.include_router(voice_router)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
