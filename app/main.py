import streamlit as st
from chains import Chain
from portfolio import Portfolio
from utils import clean_text
from langchain_community.document_loaders import WebBaseLoader

def streamlit_app(llm, portfolio, clean_text):
    st.title("Cold Email Generation.")
    url_input = st.text_input("Enter a URL: ", value="https://jobs.nike.com/job/R-43648?from=job%20search%20funnel")
    name_input = st.text_input("Enter Your Name: ", value= "Rohan Mishra")
    company_name_input = st.text_input("Enter Company Name: ", value= "Nike Pvt Ltd")
    reason_input = st.text_input("Enter Reason or Intrests for applying for this job ", value= "The companies employee enviroment, skilled professional enviroment")
    submit_button =st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            portfolio.load_portfolio()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = portfolio.query_links(skills)
                email = llm.write_mail(job, links, name_input, company_name_input, reason_input)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")

if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    streamlit_app(chain, portfolio, clean_text)