import psycopg2
import numpy as np
import pickle

# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="smartpdf",
    user="saadmehamdi", 
    password="",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Créer une table pour stocker embeddings
cursor.execute("""
CREATE TABLE IF NOT EXISTS pdf_chunks (
    id SERIAL PRIMARY KEY,
    chunk_text TEXT,
    embedding BYTEA
);
""")
conn.commit()

# Exemple de données : à adapter selon ton embed_text.py
chunks = ["exemple de texte 1", "exemple de texte 2"]
embeddings = [np.random.rand(768).tolist(), np.random.rand(768).tolist()]

for text, embed in zip(chunks, embeddings):
    # Encodage de l'embedding en binaire pour PostgreSQL
    embed_bytes = pickle.dumps(embed)
    cursor.execute(
        "INSERT INTO pdf_chunks (chunk_text, embedding) VALUES (%s, %s)",
        (text, psycopg2.Binary(embed_bytes))
    )

conn.commit()
cursor.close()
conn.close()
print("✅ Données insérées dans PostgreSQL")
