import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from dotenv import load_dotenv

load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq(
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY"),
            model_name="llama-3.3-70b-versatile"
        )

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}

            ### INSTRUCTION:
            The scraped text is from the career page of a website.
            Extract job postings from the text in JSON format with fields `role`, `experience`, `skills`, and `description`.
            Keep the JSON concise and only include relevant content.
            Only return valid JSON.
            ### VALID JSON (NO PREAMBLE):
            """
        )
        chain_extract = prompt_extract | self.llm
        res = chain_extract.invoke(input={"page_data": cleaned_text})
        try:
            json_parser = JsonOutputParser()
            res = json_parser.parse(res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return res if isinstance(res, list) else [res]

    def write_mail(self, job, resume=""):
        prompt_email = PromptTemplate.from_template(
   prompt_email = PromptTemplate.from_template(
    """
    ## INSTRUCTION:
    You are writing a professional cold email for a job application. 
    The email must be approximately 150 words and directly relevant to BOTH the company and the job description.
    Use the candidate's resume ({user_info}) to highlight relevant skills, experience, and achievements. 
    Follow this exact format:

    1. Subject line reflecting the role or your expertise.  
    2. **Polite greeting** addressing the hiring manager or team.  
    3. **Intro paragraph**: mention the specific role and the **company name (extract it from {job_description})**, and briefly introduce yourself.  
    4. **Expertise paragraph(s)**: summarize key skills, experience, and relevant technologies from the resume that match the job description.  
    5. **Portfolio/examples**: include 2–3 bullet points highlighting relevant achievements or projects from the resume.  
    6. **Summary paragraph**: explain why you are a strong fit and how you can contribute to the company’s goals (always use the company name explicitly, not a placeholder).  
    7. **Call-to-action paragraph**: politely request a meeting, call, or discussion.  
    8. **Professional signature**: name, designation, and optional links.

    Candidate information (from uploaded resume):
    {user_info}

    Job / company information (scraped from the URL):
    {job_description}

    Follow this format exactly. Keep the tone professional, concise, and persuasive. 
    Use first person (I, my, me). 
    **Important: Extract the actual company name from {job_description} and use it throughout. Do not write [Company Name].**
    Limit content to ~150 words.

    ### EMAIL (NO PREAMBLE):
    NO PREAMBLE, JUST THE EMAIL
    """
)


        chain_email = prompt_email | self.llm
        res = chain_email.invoke({
            "job_description": str(job),
            "user_info": resume
        })
        return res.content










