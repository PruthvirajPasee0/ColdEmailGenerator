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
            model_name="llama-3.1-70b-versatile",
            temperature=0,
            groq_api_key=os.getenv("GROQ_API_KEY")
        )

    def extract_jobs(self, cleaned_text):
        prompt = PromptTemplate.from_template(
            """
            ### SCRAPED TEXT FROM WEBSITE:
            {page_data}
            ### INSTRUCTION:
            The scraped text is from the career's page of a website.
            Your job is to extract the job postings and return them in JSON format containing the 
            following keys: `role`, `experience`, `skills` and `description`.
            Only return the valid JSON.
            ### VALID JSON (NO PREAMBLE):    
            """
        )
        chain_extract = prompt | self.llm
        self.res = chain_extract.invoke(input={'page_data': cleaned_text})
        try:
            json_parser = JsonOutputParser()
            self.res = json_parser.parse(self.res.content)
        except OutputParserException:
            raise OutputParserException("Context too big. Unable to parse jobs.")
        return self.res if isinstance(self.res, list) else [self.res]
    
    def write_mail(self, job, links, name, company_name, reason):
        prompt_email = PromptTemplate.from_template(
            """
            ### JOB DESCRIPTION:
            {job_description} 
            You’re a skilled professional in crafting compelling cold emails, with a special talent for making a strong first impression. You understand how to convey enthusiasm and professionalism while clearly expressing interest in a job opportunity. 

            Your task is to write a cold email proposing my interest in a position at {company_name}. Here are my details -  
            - Name: {name}  
            - Reason for interest: {reason}
            Also add the most relevant ones from the following links of portfolios: {link_list} 

            Keep in mind that the tone should be friendly yet professional, and the email should include a call to action encouraging the recipient to respond.

            Do not provide a preamble.
            ### EMAIL (NO PREAMBLE):

            """
        )
        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job), "link_list": links, "company_name": company_name, "name": name, "reason":reason})
        return res.content