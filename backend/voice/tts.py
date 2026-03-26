import os
from elevenlabs.client import ElevenLabs

# ElevenLabs v1.0.0+ requires standard client format
try:
    client = ElevenLabs(api_key=os.environ.get("ELEVENLABS_API_KEY", ""))
except:
    client = None

def speak(text):
    if not client or not os.environ.get("ELEVENLABS_API_KEY"):
        return None
        
    try:
        audio = client.generate(
            text=text,
            voice="Rachel",
            model="eleven_monolingual_v1"
        )
        return b''.join(audio)    
    except Exception as e:
        print(f"TTS Error: {e}")
        return None
