import uuid
from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()  

class Portfolio:
    def __init__(self, collection_name="user_resume_vectorstore"):
 
        self.vectorstore = FAISS.from_texts([], embedding=embeddings)

    def add_resume(self, resume_text, user_id=None):
        if not user_id:
            user_id = str(uuid.uuid4())
        self.vectorstore.add_texts(
            texts=[resume_text],
            metadatas=[{"user_id": user_id}],
            ids=[user_id]
        )
        return user_id

    def query_resume(self, query_text, n_results=1):
        results = self.vectorstore.similarity_search_with_score(query_text, k=n_results)
        return [r[0].metadata for r in results]
