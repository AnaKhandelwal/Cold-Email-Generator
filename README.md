# 📧 Cold Email Generator

An AI-powered app that generates **personalized cold emails** using resumes and job descriptions.  
Built with **Streamlit, LangChain, and ChromaDB**.

---

## 🚀 Features
- 📝 Upload and store resumes in a vector database (ChromaDB).  
- 🔍 Retrieve relevant resume content with semantic search.  
- 🤖 Generate tailored cold emails using AI.  
- 💾 Uses in-memory ChromaDB by default (works on Streamlit Cloud).  

---

## 📂 Project Structure
cold-email-generator/
│── main.py # Streamlit app entry point

│── chains.py # LangChain chains for email generation

│── portfolio.py # Handles resume storage & queries with ChromaDB

│── requirements.txt # Project dependencies

├── .streamlit/ # Streamlit Cloud config (secrets.toml goes here)

│ └── secrets.toml
