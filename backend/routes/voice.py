import os
import tempfile
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import Response
from voice.stt import transcribe
from voice.tts import speak
from agents.graph import app_graph

router = APIRouter()

@router.post("/voice-chat")
async def voice_chat(file: UploadFile = File(...)):
    # Create temp directory instead of hardcoded temp/
    temp_dir = tempfile.gettempdir()
    audio_path = os.path.join(temp_dir, file.filename if file.filename else "temp.wav")

    with open(audio_path, "wb") as f:
        f.write(await file.read())

    text = transcribe(audio_path)

    state = {
        "user_input": text,
        "context": "",
        "response": "",
        "lead": {},
        "intent": ""
    }

    result = app_graph.invoke(state)
    audio = speak(result["response"])

    # Clean up temp file
    if os.path.exists(audio_path):
        os.remove(audio_path)

    if audio:
        return Response(content=audio, media_type="audio/mpeg")
    else:
        # Fallback if ElevenLabs is not configured
        return {"text": result["response"], "message": "TTS audio not completely generated due to config"}
