import json
import os
import google.generativeai as genai
import faiss
import numpy as np

# Change path relative to backend root or main.py execution directory
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "project_data.json")

try:
    with open(data_path) as f:
        project_data = f.read()

    def retrieve_context(query):
        # For this small dataset, providing the entire JSON is more reliable 
        # than a failing RAG service and fits easily in Gemini's context.
        return project_data

except Exception as e:
    print(f"Warning: Project data load failed: {e}")
    def retrieve_context(query):
        return "Seabreeze by Godrej Bayview is located in Vashi. 2 BHK starts at 3.20 Cr, 3 BHK starts at 4.75 Cr. It has sea views and 52+ amenities."
