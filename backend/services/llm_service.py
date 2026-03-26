import os
import google.generativeai as genai

# Setup Gemini API key
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

SYSTEM_PROMPT = """
You are a professional real estate assistant for Seabreeze by Godrej Bayview.

Goals:
- Answer user queries
- Highlight USPs (sea view, amenities, connectivity)
- Capture requirements naturally
- Push toward site visit

Tone:
Professional, helpful, slightly persuasive
"""

def generate_response(user_input, context):
    prompt = f"""
Context:
{context}

User:
{user_input}
"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=SYSTEM_PROMPT)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Hello! I am having trouble connecting to my Gemini brain ({e}). But I can still answer basic questions about Seabreeze by Godrej Bayview!"
