import chromadb
import uuid
import os

class Portfolio:
    def __init__(self, collection_name="user_resume_vectorstore", store_path=None):
        if store_path is None:
            store_path = os.path.join(os.getcwd(), "vectorstore")
        os.makedirs(store_path, exist_ok=True)

        try:
            self.chroma_client = chromadb.PersistentClient(store_path)
            self.collection = self.chroma_client.get_or_create_collection(name=collection_name)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Chroma vector DB: {e}")

    def add_resume(self, resume_text, user_id=None):
        try:
            if not user_id:
                user_id = str(uuid.uuid4())
            self.collection.add(
                documents=[resume_text],
                metadatas={"user_id": user_id},
                ids=[user_id]
            )
            return user_id
        except Exception as e:
            raise RuntimeError(f"Failed to add resume to vector DB: {e}")

    def query_resume(self, query_text, n_results=1):
        try:
            return self.collection.query(query_texts=[query_text], n_results=n_results).get('metadatas', [])
        except Exception as e:
            raise RuntimeError(f"Failed to query vector DB: {e}")
