from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import faiss
import numpy as np
import json
import sys

from sentence_transformers import SentenceTransformer
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from llm_interface.query_ollama import query_ollama
from scripts.extract_pdf import extract_text_from_pdf

#  Initialisation Flask
app = Flask(__name__)
CORS(app)  # autorise toutes les origines pour React

UPLOAD_FOLDER = "data"
ALLOWED_EXTENSIONS = {"pdf"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ✅ Utilitaires
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Charger le modèle une seule fois
model = SentenceTransformer("all-MiniLM-L6-v2")

# 
# Route 1 — Upload PDF
@app.route("/upload", methods=["POST"])
def upload_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "Aucun fichier fourni"}), 400
        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "Nom de fichier vide"}), 400
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(filepath)

            print(f"[LOG] Fichier enregistré sous : {filepath}")

            # Extraction
            text = extract_text_from_pdf(filepath)
            with open("data/extracted_text.json", "w", encoding="utf-8") as f:
                json.dump({"text": text}, f)

            # Chunk + embeddings + save FAISS
            chunks = [text[i:i+500] for i in range(0, len(text), 500)]
            embeddings = model.encode(chunks).astype("float32")
            dim = embeddings.shape[1]
            index = faiss.IndexFlatL2(dim)
            index.add(embeddings)
            os.makedirs("db/faiss_index", exist_ok=True)
            faiss.write_index(index, "db/faiss_index/index.faiss")

            with open("db/faiss_index/chunks.json", "w", encoding="utf-8") as f:
                json.dump(chunks, f)

            return jsonify({"message": "PDF traité avec succès"}), 200
        else:
            return jsonify({"error": "Fichier non supporté"}), 400
    except Exception as e:
        print("Erreur upload_pdf :", e)
        return jsonify({"error": str(e)}), 500

#  Route 2 — Poser une question
@app.route("/ask", methods=["POST"])
def ask():
    try:
        data = request.get_json()
        question = data.get("question", "")
        if not question:
            return jsonify({"error": "Question vide"}), 400

        # Vérifier si FAISS et chunks existent
        if not os.path.exists("db/faiss_index/index.faiss") or not os.path.exists("db/faiss_index/chunks.json"):
            return jsonify({"error": "FAISS index ou chunks manquants. Veuillez uploader un PDF d'abord."}), 400

        # Charger FAISS + chunks
        index = faiss.read_index("db/faiss_index/index.faiss")
        with open("db/faiss_index/chunks.json", "r", encoding="utf-8") as f:
            chunks = json.load(f)

        question_embedding = model.encode([question]).astype("float32")
        D, I = index.search(question_embedding, 5)
        context_chunks = [chunks[i] for i in I[0] if 0 <= i < len(chunks)]

        context_text = "\n\n".join(context_chunks)
        prompt = f"Voici le contexte :\n{context_text}\n\nQuestion: {question}\nRéponse :"

        response = query_ollama(prompt)

        return jsonify({"response": response})
    except Exception as e:
        print("Erreur ask :", e)
        return jsonify({"error": str(e)}), 500

#  Lancer le serveur Flask
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
