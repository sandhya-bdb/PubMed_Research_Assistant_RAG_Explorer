from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient
import numpy as np
import os

class VectorStore:
    def __init__(self, persist_directory: str = "chroma_db",
                 model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        # Initialize embedding model
        self.embedding_model = SentenceTransformer(model_name)
        os.makedirs(persist_directory, exist_ok=True)

        # ✅ Use new Chroma persistent client
        self.client = PersistentClient(path=persist_directory)

        # ✅ Create or get collection
        collection_name = "pubmed_collection"
        existing_collections = [c.name for c in self.client.list_collections()]
        if collection_name in existing_collections:
            self.collection = self.client.get_collection(collection_name)
        else:
            self.collection = self.client.create_collection(collection_name)

    def ingest(self, docs: list[str], metadatas: list[dict], ids: list[str]):
        embeddings = self.embedding_model.encode(docs, show_progress_bar=True)
        processed_embeddings = [
            emb.tolist() if hasattr(emb, "tolist") else emb for emb in embeddings
        ]

        self.collection.add(
            ids=ids,
            embeddings=processed_embeddings,
            metadatas=metadatas,
            documents=docs
        )

        # ✅ Optional persist
        try:
            self.client.persist()
        except AttributeError:
            pass  # client may auto-persist in new versions

    def query(self, query_text: str, k: int = 5):
        query_emb = self.embedding_model.encode([query_text])[0].tolist()

        # ✅ Fix: remove 'ids' from include list
        result = self.collection.query(
            query_embeddings=[query_emb],
            n_results=k,
            include=["documents", "metadatas", "distances"]
        )

        return result
