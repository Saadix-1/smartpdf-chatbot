import json
import os
import faiss
import numpy as np
import sys
from sentence_transformers import SentenceTransformer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from llm_interface.query_ollama import query_ollama  

def load_text_chunks(json_path, chunk_size=500):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        text = data.get("text", "")

    # Découpage simple en morceaux de `chunk_size` caractères
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

def embed_chunks(chunks, model):
    return model.encode(chunks, convert_to_tensor=False)

def save_faiss_index(embeddings, path="db/faiss_index"):
    os.makedirs(path, exist_ok=True)
    dim = len(embeddings[0])
    index = faiss.IndexFlatL2(dim)
    index.add(np.array(embeddings).astype("float32"))
    faiss.write_index(index, f"{path}/index.faiss")

def save_mapping(chunks, path="db/faiss_index"):
    with open(f"{path}/chunks.json", "w", encoding="utf-8") as f:
        json.dump(chunks, f)

def main():
    model = SentenceTransformer("all-MiniLM-L6-v2")
    chunks = load_text_chunks("data/extracted_text.json")
    embeddings = embed_chunks(chunks, model)
    save_faiss_index(embeddings)
    save_mapping(chunks)

    texte_complet = " ".join(chunks)  # Concaténation des chunks
    print(" Envoi du texte extrait au modèle LLM (Ollama)...")
    reponse = query_ollama(texte_complet)
    print("📩 Réponse du LLM :\n")
    print(reponse)

if __name__ == "__main__":
    main()
