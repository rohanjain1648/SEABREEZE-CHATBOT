import json
import os
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Change path relative to backend root or main.py execution directory
data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "project_data.json")

try:
    with open(data_path) as f:
        data = json.load(f)

    def flatten_data(data, prefix=""):
        items = []
        if isinstance(data, dict):
            for k, v in data.items():
                items.extend(flatten_data(v, f"{prefix}{k}: "))
        elif isinstance(data, list):
            for i, v in enumerate(data):
                items.extend(flatten_data(v, f"{prefix}"))
        else:
            items.append(f"{prefix}{data}")
        return items

    documents = flatten_data(data)

    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(documents)
    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(np.array(embeddings))
    
    def retrieve_context(query):
        q_embedding = model.encode([query])
        D, I = index.search(np.array(q_embedding), k=5)
        results = [documents[i] for i in I[0]]
        return "\n".join(results)

except Exception as e:
    # Fallback/Dummy logic if model or data fail to load quickly
    print(f"Warning: RAG initialization failed: {e}")
    def retrieve_context(query):
        return "Seabreeze by Godrej Bayview is located in Vashi. 2 BHK starts at 3.20 Cr, 3 BHK starts at 4.75 Cr. It has sea views and 52+ amenities."
