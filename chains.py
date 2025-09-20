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
            Extract the job postings in JSON format containing `role`, `experience`, `skills`, and `description`.
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
        """
        ## INSTRUCTION:
        You are writing a professional cold email for a job application which is relevant to the job description. Follow this exact format:

        1. Subject line reflecting the role or your expertise.  
        2. **Polite greeting** addressing the hiring manager or team.  
        3. **Intro paragraph**: mention the role/company and briefly introduce yourself.  
        4. **Expertise paragraph(s)**: summarize your key skills, experience, and relevant technologies.  
        5. **Portfolio/examples**: include 2–3 bullet points highlighting relevant achievements or projects.  
        6. **Summary paragraph**: explain why you are a good fit and how you can help the company achieve its goals.  
        7. **Call-to-action paragraph**: politely request a meeting, call, or discussion.  
        8. **Professional signature**: name, designation, and optional links.

        Candidate information (from uploaded resume):
        {user_info}

        Job / company information (scraped from the URL):
        {job_description}

        Follow this format exactly. Keep the tone professional, concise, and persuasive. Use first person (I, my, me).  

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
