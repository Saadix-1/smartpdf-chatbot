# main.py
import fitz  # PyMuPDF
print("PDF package OK ✅")

import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

def search(query, k=3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_embedding = model.encode([query])

    index = faiss.read_index("db/faiss_index/index.faiss")
    D, I = index.search(np.array(query_embedding).astype("float32"), k)

    with open("db/faiss_index/chunks.json", "r", encoding="utf-8") as f:
        chunks = json.load(f)

    results = [chunks[i] for i in I[0]]
    return results
