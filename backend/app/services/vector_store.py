import os
from pinecone import Pinecone, ServerlessSpec
from openai import OpenAI
import uuid
from ..core.config import settings

class VectorStore:
    def __init__(self):
        # We initialize clients dynamically so the API keys from settings are picked up
        self.pc = None
        self.index = None
        self.openai_client = None
        self.index_name = settings.PINECONE_INDEX_NAME

    def _initialize_clients(self):
        if not self.pc and settings.PINECONE_API_KEY:
            self.pc = Pinecone(api_key=settings.PINECONE_API_KEY)
            
            # Check if index exists, create if it doesn't
            if self.index_name not in self.pc.list_indexes().names():
                self.pc.create_index(
                    name=self.index_name,
                    dimension=1536, # openai text-embedding-3-small dimension
                    metric='cosine',
                    spec=ServerlessSpec(cloud='aws', region='us-east-1') # Default free-tier spec
                )
            self.index = self.pc.Index(self.index_name)
            
        if not self.openai_client and settings.OPENAI_API_KEY:
            self.openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def process_pdf(self, text: str):
        self._initialize_clients()
        if not self.index or not self.openai_client:
            raise ValueError("Pinecone or OpenAI not configured properly.")

        chunk_size = 500
        overlap = 100
        new_chunks = []
        
        if len(text) <= chunk_size:
            new_chunks.append(text)
        else:
            for i in range(0, len(text) - overlap, chunk_size - overlap):
                chunk = text[i:i + chunk_size]
                if chunk.strip():
                    new_chunks.append(chunk.strip())

        # Generate embeddings via OpenAI
        response = self.openai_client.embeddings.create(
            input=new_chunks,
            model="text-embedding-3-small"
        )
        
        # Prepare Upsert Payload
        vectors_to_upsert = []
        for i, data in enumerate(response.data):
            vec_id = str(uuid.uuid4())
            vectors_to_upsert.append({
                "id": vec_id,
                "values": data.embedding,
                "metadata": {"text": new_chunks[i]} # Store text in metadata so we can retrieve it
            })

        # Upsert in batches of 100
        batch_size = 100
        for i in range(0, len(vectors_to_upsert), batch_size):
            self.index.upsert(vectors=vectors_to_upsert[i:i + batch_size])

    def search(self, query: str, k: int = 5):
        self._initialize_clients()
        if not self.index or not self.openai_client:
            return []
            
        response = self.openai_client.embeddings.create(
            input=[query],
            model="text-embedding-3-small"
        )
        query_embedding = response.data[0].embedding
        
        results = self.index.query(
            vector=query_embedding,
            top_k=k,
            include_metadata=True
        )
        
        return [match['metadata']['text'] for match in results['matches'] if 'metadata' in match and 'text' in match['metadata']]

# Singleton instance
vector_store = VectorStore()

