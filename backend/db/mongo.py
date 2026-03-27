import json
import os

# Zero-config file-based storage for leads
LEADS_FILE = "leads.json"

def save_lead(session_id, lead):
    try:
        leads = {}
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r") as f:
                leads = json.load(f)
        
        # Update or create lead entry
        if session_id not in leads:
            leads[session_id] = {}
        
        current_lead = leads[session_id]
        if isinstance(current_lead, dict):
            current_lead.update(lead)
        
        with open(LEADS_FILE, "w") as f:
            json.dump(leads, f, indent=2)
            
        print(f"Lead Saved Locally: {session_id} -> {lead}")
    except Exception as e:
        print(f"Failed to save lead: {e}")

def get_lead(session_id):
    try:
        if os.path.exists(LEADS_FILE):
            with open(LEADS_FILE, "r") as f:
                leads = json.load(f)
                return leads.get(session_id, {})
    except Exception as e:
        print(f"Failed to get lead: {e}")
    return {}
