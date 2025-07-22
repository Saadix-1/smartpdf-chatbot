import json
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
import faiss
import numpy as np
from llm_interface.query_ollama import query_ollama

FAISS_INDEX_PATH = "db/faiss_index/index.faiss"
CHUNKS_MAPPING_PATH = "db/faiss_index/chunks.json"
TOP_K = 5  # Nombre de passages les plus proches à récupérer

def load_faiss_index(index_path=FAISS_INDEX_PATH):
    if not os.path.exists(index_path):
        raise FileNotFoundError(f"FAISS index not found at {index_path}")
    return faiss.read_index(index_path)

def load_chunks(mapping_path=CHUNKS_MAPPING_PATH):
    if not os.path.exists(mapping_path):
        raise FileNotFoundError(f"Chunks mapping file not found at {mapping_path}")
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f)

def embed_query(query, model):
    # On utilise la même méthode d'embedding que dans embed_text.py
    # Pour simplifier, on utilise ici sentence-transformers aussi
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode([query], convert_to_tensor=False)[0]

def main():
    print("Chargement de l'index FAISS et des chunks...")
    index = load_faiss_index()
    chunks = load_chunks()

    print("Modèle d'embedding chargé (all-MiniLM-L6-v2)")

    while True:
        query = input("\n💬 Pose ta question (exit pour quitter) :\n> ")
        if query.strip().lower() == "exit":
            print("Au revoir 👋")
            break

        # Embedding de la question
        query_embedding = embed_query(query, None)

        # Recherche des TOP_K voisins les plus proches
        D, I = index.search(np.array([query_embedding]).astype("float32"), TOP_K)

        # Récupération des chunks correspondants
        matched_chunks = [chunks[i] for i in I[0] if i < len(chunks)]

        # Construction du prompt à envoyer à Ollama
        prompt = (
            "Voici des extraits de documents pour t'aider à répondre à la question suivante :\n\n"
            + "\n\n---\n\n".join(matched_chunks)
            + f"\n\nQuestion : {query}\nRéponse :"
        )

        print("\n🧠 Envoi au modèle Ollama...\n")
        try:
            response = query_ollama(prompt)
            print(f"🧠 Réponse :\n\n{response}")
        except Exception as e:
            print(f"Erreur LLM: {e}")

if __name__ == "__main__":
    main()
