from llm import call_llm
from services.rag_service import retrieve_context
import json

def router(state):
    intent = call_llm(f"Classify intent (is it high, medium, low intent for real estate buying): {state['user_input']}")

    return {
        **state,
        "intent": intent
    }

def rag_agent(state):
    context = retrieve_context(state["user_input"])
    return {**state, "context": context}

SYSTEM_PROMPT = """
You are Shardul, an elite, professional lead relationship manager and real estate sales consultant for Seabreeze by Godrej Bayview.

Your instructions:
1.  **Professional Tone**: Maintain a luxury, helpful, and sophisticated tone. Use polite greetings and professional closings.
2.  **Project Knowledge**: Use the provided context to answer questions with precision. Highlight unique USPs like "stunning sea views", "private decks", and "52+ amenities across 3 retreat levels".
3.  **Lead Capture**: To move towards a site visit, you MUST capture the user's:
    *   Requirement (2 or 3 BHK)
    *   Budget Range
    *   Preferred Location (if they are already in Vashi or moving from elsewhere)
4.  **Natural Progression**: If the user hasn't provided their budget or BHK preference, ask for it naturally as part of your answer.
5.  **Conversion**: Once you have the basic details, invite them for a physical site visit to experience the views from the actual private decks.
"""

def sales_agent(state: dict):
    prompt = f"""
Context:
{state.get('context', '')}

User:
{state.get('user_input', '')}
"""

    response = call_llm(prompt, system=SYSTEM_PROMPT)

    return {**state, "response": response}

def lead_agent(state):
    prompt = f"""
    Analyze the following message from a potential real estate lead and extract the following information in a structured JSON format:
    - budget: Their mentioned budget (e.g., "3-4 Cr")
    - bhk: Their preferred configuration (e.g., "2 BHK")
    - location: Their current or preferred location
    - intent: Their buying intent level (Low, Medium, High)

    If a field is not mentioned, return null for that field.

    Text to analyze:
    {state['user_input']}
    """

    result = call_llm(prompt)

    try:
        if result.startswith("```json"):
            result = result.split("```json")[1].split("```")[0].strip()
        lead = json.loads(result)
    except:
        lead = {}

    return {**state, "lead": lead}

def closer_agent(state):
    prompt = f"""
    The user is showing high interest. Take the following professional response and enhance it with a specific, warm invitation for a site visit at Seabreeze or a call with our Relationship Manager, Shardul. 
    Ensure you maintain the expert sales consultant tone and mention Shardul by name.

    Original Response:
    {state['response']}
    """

    closing = call_llm(prompt)

    return {**state, "response": closing}
