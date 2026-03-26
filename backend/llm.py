import os
import google.generativeai as genai

api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)

def call_llm(prompt, system=None):
    if not os.getenv("GEMINI_API_KEY"):
        return "⚠️ [SYSTEM ERROR]: GEMINI_API_KEY is not set. Please set the environment variable to enable the AI Chatbot."
        
    try:
        model = genai.GenerativeModel('gemini-2.0-flash', system_instruction=system)
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Gemini LLM Call Error: {e}")
        return f"I am unable to process that right now. Could you rephrase? (Error: {e})"
