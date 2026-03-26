from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

from services.rag_service import retrieve_context
from agents.graph import app_graph
from db.mongo import save_lead

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
    # LangGraph agentic approach
    state = {
        "user_input": req.message,
        "context": "",
        "response": "",
        "lead": {},
        "intent": ""
    }
    
    # We can use the simple code or the graph code. The graph incorporates everything.
    result = app_graph.invoke(state)
    
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
