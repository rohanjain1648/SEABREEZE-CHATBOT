import json
import os
import google.generativeai as genai
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

    # Use Gemini Text Embedding Model to save 500MB+ RAM vs local PyTorch models
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        genai.configure(api_key=api_key)
        
    def get_embeddings(texts):
        if not os.getenv("GEMINI_API_KEY"):
            return np.zeros((len(texts), 768), dtype=np.float32)
            
        result = genai.embed_content(
            model="models/text-embedding-004",
            content=texts,
            task_type="retrieval_document"
        )
        return np.array(result['embedding'], dtype=np.float32)

    print("Initializing Gemini Embeddings (Lightweight)...")
    raw_embeddings = get_embeddings(documents)
    
    # Gemini text-embedding-004 outputs 768 dimensions
    index = faiss.IndexFlatL2(768)
    if raw_embeddings.shape[0] > 0 and raw_embeddings.shape[1] == 768:
        index.add(raw_embeddings)
    
    def retrieve_context(query):
        if not os.getenv("GEMINI_API_KEY"):
            return "Seabreeze by Godrej Bayview is located in Vashi. 2 BHK starts at 3.20 Cr, 3 BHK starts at 4.75 Cr. It has sea views and 52+ amenities."
            
        q_result = genai.embed_content(
            model="models/text-embedding-004",
            content=query,
            task_type="retrieval_query"
        )
        q_embedding = np.array([q_result['embedding']], dtype=np.float32)
        D, I = index.search(q_embedding, k=5)
        results = [documents[i] for i in I[0] if i >= 0]
        return "\n".join(results)

except Exception as e:
    # Fallback/Dummy logic if model or data fail to load quickly
    print(f"Warning: RAG initialization failed: {e}")
    def retrieve_context(query):
        return "Seabreeze by Godrej Bayview is located in Vashi. 2 BHK starts at 3.20 Cr, 3 BHK starts at 4.75 Cr. It has sea views and 52+ amenities."
