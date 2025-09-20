import streamlit as st
from langchain-community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import PyPDF2

def read_resume(file):
    if file.type == "application/pdf":
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        st.warning("Unsupported file type. Please upload PDF or TXT.")
        return ""

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://example.com")
    resume_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
    resume_text = ""
    user_id = None

    if resume_file:
        resume_text = read_resume(resume_file)
        user_id = portfolio.add_resume(resume_text)

    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            jobs = llm.extract_jobs(data)
            for job in jobs:
                email = llm.write_mail(job, resume=resume_text)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)

