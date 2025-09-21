import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
import PyPDF2
import pdfplumber

MAX_CHARS = 11000

def read_resume(file):
    if file.type == "application/pdf":
        text = ""
        try:
            reader = PyPDF2.PdfReader(file)
            for page in reader.pages:
                text += page.extract_text() or ""
        except:
            with pdfplumber.open(file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""
        return text
    elif file.type == "text/plain":
        return file.read().decode("utf-8")
    else:
        st.warning("Unsupported file type. Please upload PDF or TXT.")
        return ""

def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a Job URL:", value="https://example.com")
    resume_file = st.file_uploader("Upload your resume (PDF or TXT)", type=["pdf", "txt"])
    resume_text = ""
    user_id = None

    if resume_file:
        resume_text = read_resume(resume_file)
        if resume_text.strip():
            user_id = portfolio.add_resume(resume_text)
        else:
            st.error("Resume could not be parsed. Please upload a valid PDF/TXT.")

    submit_button = st.button("Generate Cold Email")

    if submit_button:
        if not url_input or not resume_text:
            st.error("Please provide both a Job URL and your resume.")
        else:
            try:
                loader = WebBaseLoader([url_input])
                raw_text = loader.load().pop().page_content
                cleaned_text = clean_text(raw_text)
                # Truncate to avoid LLM input size issues
                cleaned_text = cleaned_text[:MAX_CHARS]
                jobs = llm.extract_jobs(cleaned_text)
                if jobs:
                    for job in jobs:
                        email = llm.write_mail(job, resume=resume_text)
                        st.code(email, language='markdown')
                else:
                    st.warning("No job postings found or page could not be parsed.")
            except Exception as e:
                st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)
