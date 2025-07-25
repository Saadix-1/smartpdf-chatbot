import os
import uuid
import fitz  # PyMuPDF
import psycopg2
import json
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from llm_interface.query_ollama import ask_llm  # <-- tu as déjà ce fichier
import numpy as np

load_dotenv()

# ==== CONFIG ====
UPLOAD_FOLDER = 'uploads'
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST", "localhost"),
    "port": os.getenv("DB_PORT", "5432")
}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

model = SentenceTransformer("all-MiniLM-L6-v2")

# ==== UTILS ====

def extract_text_from_pdf(filepath):
    doc = fitz.open(filepath)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def chunk_text(text, max_tokens=300):
    sentences = text.split(". ")
    chunks = []
    chunk = ""
    for sentence in sentences:
        if len((chunk + sentence).split()) > max_tokens:
            chunks.append(chunk.strip())
            chunk = sentence
        else:
            chunk += " " + sentence
    if chunk:
        chunks.append(chunk.strip())
    return chunks

def store_embeddings_pg(chunks, embeddings):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    for chunk, emb in zip(chunks, embeddings):
        cur.execute("""
            INSERT INTO embeddings (id, chunk, embedding)
            VALUES (%s, %s, %s)
        """, (str(uuid.uuid4()), chunk, json.dumps(emb.tolist())))
    conn.commit()
    cur.close()
    conn.close()

def retrieve_most_similar_chunks_pg(question_embedding, top_k=3):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute("SELECT chunk, embedding FROM embeddings")
    rows = cur.fetchall()
    cur.close()
    conn.close()

    scores = []
    for chunk, embedding in rows:
        emb_array = np.array(json.loads(embedding))
        similarity = np.dot(question_embedding, emb_array)
        scores.append((chunk, similarity))
    
    scores.sort(key=lambda x: x[1], reverse=True)
    return [chunk for chunk, _ in scores[:top_k]]

# ==== ROUTES ====

@app.route("/upload", methods=["POST"])
def upload_pdf():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "No file provided"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    text = extract_text_from_pdf(filepath)
    chunks = chunk_text(text)
    embeddings = model.encode(chunks)

    store_embeddings_pg(chunks, embeddings)

    return jsonify({"message": f"{len(chunks)} chunks embeddés et stockés"}), 200

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question")
    if not question:
        return jsonify({"error": "Pas de question fournie"}), 400

    question_embedding = model.encode([question])[0]
    context_chunks = retrieve_most_similar_chunks_pg(question_embedding)

    prompt = f"Voici des extraits du document :\n\n" + "\n\n".join(context_chunks)
    prompt += f"\n\nQuestion : {question}"

    response = ask_llm(prompt)
    return jsonify({"response": response})

# ==== LANCEMENT ====
if __name__ == "__main__":
    app.run(debug=True)
