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
    try:
        data = request.json
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "Question vide"}), 400

        print(f"[LOG] Question reçue : {question}")

        # Embed la question
        question_embedding = model.encode([question]).astype("float32")

        # Recherche dans FAISS (top 5)
        D, I = index.search(question_embedding, 5)
        print(f"[LOG] Indices retournés : {I[0]}")
        print(f"[LOG] Distances : {D[0]}")

        # Récupérer les chunks correspondants
        context_chunks = [chunks[i] for i in I[0] if 0 <= i < len(chunks)]
        if not context_chunks:
            return jsonify({"error": "Aucun chunk pertinent trouvé"}), 404

        print(f"[LOG] Nombre de chunks retrouvés : {len(context_chunks)}")

        # Préparer prompt à envoyer à Ollama
        context_text = "\n\n".join(context_chunks)
        prompt = f"Voici le contexte :\n{context_text}\n\nQuestion: {question}\nRéponse :"

        print(f"[LOG] Prompt envoyé à Ollama :\n{prompt[:500]}...")  # Affiche seulement les 500 premiers caractères

        # Appel Ollama (ta fonction)
        response = query_ollama(prompt)

        print(f"[LOG] Réponse reçue d'Ollama : {response}")

        return jsonify({"answer": response})

    except Exception as e:
        print(f"[ERREUR] Une erreur s'est produite : {str(e)}")
        return jsonify({"error": "Erreur interne du serveur"}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
