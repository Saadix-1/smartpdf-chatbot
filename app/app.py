from flask import Flask, request, jsonify
import os
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from llm_interface.query_ollama import query_ollama

app = Flask(__name__)

# Charger l'index FAISS
index_path = "db/faiss_index/index.faiss"
mapping_path = "db/faiss_index/chunks.json"

print("Chargement de l'index FAISS...")
index = faiss.read_index(index_path)

print("Chargement des chunks...")
with open(mapping_path, "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Charger modèle de SentenceTransformer (même que pour embed)
model = SentenceTransformer("all-MiniLM-L6-v2")

@app.route("/api/query", methods=["POST"])
def query():
    data = request.json
    question = data.get("question", "")
    if not question:
        return jsonify({"error": "Question vide"}), 400

    # Embed la question
    question_embedding = model.encode([question]).astype("float32")

    # Recherche dans FAISS (top 5)
    D, I = index.search(question_embedding, 5)

    # Récupérer les chunks correspondants
    context_chunks = [chunks[i] for i in I[0]]

    # Préparer prompt à envoyer à Ollama
    context_text = "\n\n".join(context_chunks)
    prompt = f"Voici le contexte :\n{context_text}\n\nQuestion: {question}\nRéponse :"

    # Appel Ollama (ta fonction)
    response = query_ollama(prompt)

    return jsonify({"answer": response})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
