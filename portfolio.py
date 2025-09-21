import uuid

# --- Patch sqlite BEFORE importing chromadb ---
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

import chromadb


class Portfolio:
    def __init__(self, collection_name="user_resume_vectorstore"):
        try:
            # In-memory client (safe for Streamlit Cloud)
            self.chroma_client = chromadb.Client()
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chroma vector DB: {e}")

    def add_resume(self, resume_text, user_id=None):
        try:
            if not user_id:
                user_id = str(uuid.uuid4())
            self.collection.add(
                documents=[resume_text],
                metadatas=[{"user_id": user_id}],  # must be list of dicts
                ids=[user_id]
            )
            return user_id
        except Exception as e:
            raise RuntimeError(f"Failed to add resume to vector DB: {e}")

    def query_resume(self, query_text, n_results=1):
        try:
            return self.collection.query(
                query_texts=[query_text],
                n_results=n_results
            ).get('metadatas', [])
        except Exception as e:
            raise RuntimeError(f"Failed to query vector DB: {e}")
