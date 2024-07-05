import streamlit as st
import os
import google.generativeai as gai
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

if not api_key:
    st.error("Google API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")
else:
    gai.configure(api_key=api_key)

    model = gai.GenerativeModel('gemini-1.5-flash')

    def get_resume_tex(jd, information, resume):
        prompt = f"""
        Act as an experienced Application Tracking System (ATS) with expertise in the tech field, including software engineering, data science, data analysis, and big data engineering. Your job is to accept a template LaTeX code for a resume from the Candidate along with Job Description and Candidate's personal information. Based on the job description and Candidate's information, you populate the template latex code and generate a resume in tex format for the Candidate. Assess the job description and populate the resume with right keywords, that is optimized for ATS Scanner with respect to the provided Job Description.

        Here is the LaTeX code for the resume template: {resume}
        Here is the Candidate's information: {information}
        Here is the Job Description: {jd}

        Only respond with the LaTeX code for the resume.
        """
        response = model.generate_content(prompt)
        return response.text

    def get_resume_mk(information, jd):
        prompt = f"""
        Act as an experienced Application Tracking System (ATS) with expertise in the tech field, including software engineering, data science, data analysis, and big data engineering. Your job is to accept a Job Description and Candidate's personal information. Based on the job description and Candidate's information, you generate a resume in markdown code format for the Candidate. Assess the job description and populate the resume with right keywords, that is optimized for ATS Scanner with respect to the provided Job Description.

        Here is the Candidate's information: {information}
        Here is the Job Description: {jd}

        Only respond with the markdown code for resume and nothing else.
        """
        response = model.generate_content(prompt)
        return response.text

    st.title("Resume Copilot")
    st.header("Get ATS Optimized Resume with the help of latest AI technology")
    jd = st.text_area("Enter Job Description")
    info = st.text_area("Enter your information")
    res = st.text_area("Enter LaTeX Resume Template:")

    if st.button("Generate TeX Resume"):
        if jd and info and res:
            try:
                resp = get_resume_tex(jd, info, res)
                st.text_area("Here's your TeX Resume:", value=resp, height=600)
            except Exception as e:
                st.error(f"Error generating TeX resume: {e}")
        else:
            st.error("Please enter all the required fields")

    if st.button("Generate Markdown Resume"):
        if jd and info and not res:
            try:
                resp = get_resume_mk(info, jd)
                st.text_area("Here's your Markdown Resume:", value=resp, height=600)
            except Exception as e:
                st.error(f"Error generating Markdown resume: {e}")
        else:
            st.error("Please enter all the required fields")

    st.subheader("The program above outputs code in either TeX or Markdown, which you can then modify to suit your needs.")
