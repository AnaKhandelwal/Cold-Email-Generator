import uuid
import chromadb
from chromadb.config import Settings

# Use a temporary directory for persistence
chroma_client = chromadb.Client(
    Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory="/tmp/chroma"  # safe for Streamlit Cloud
    )
)

class Portfolio:
    def __init__(self, collection_name="user_resume_vectorstore"):
        self.collection = chroma_client.get_or_create_collection(name=collection_name)

    def add_resume(self, resume_text, user_id=None):
        if not user_id:
            user_id = str(uuid.uuid4())
        self.collection.add(
            documents=[resume_text],
            metadatas=[{"user_id": user_id}],
            ids=[user_id]
        )
        return user_id

    def query_resume(self, query_text, n_results=1):
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        return results.get('metadatas', [])
