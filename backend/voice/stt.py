import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def transcribe(audio_path):
    try:
        # Upload the file to Gemini API
        audio_file = genai.upload_file(path=audio_path)
        
        # Use Gemini model to extract speech to text
        model = genai.GenerativeModel('gemini-2.0-flash')
        response = model.generate_content([
            audio_file, 
            "Please transcribe this audio exactly as it was spoken. Output only the transcription text and nothing else."
        ])
        
        # Delete file after transcription
        genai.delete_file(audio_file.name)
        
        return response.text.strip()
    except Exception as e:
        print(f"Gemini STT Error: {e}")
        return "I couldn't hear you clearly."
