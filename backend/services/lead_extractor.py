import os
import json
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def extract_lead(text):
    prompt = f"""
Extract the following fields from user input:

Fields:
- budget
- bhk
- location
- intent (low/medium/high)

Return JSON only mapping field names to extracted values.

Text:
{text}
"""
    try:
        model = genai.GenerativeModel('gemini-2.0-flash', generation_config={"response_mime_type": "application/json"})
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception as e:
        print(f"Error extracting lead with Gemini: {e}")
        return {}
