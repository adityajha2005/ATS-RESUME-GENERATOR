import streamlit as st
import os
import google.generativeai as gai
from dotenv import load_dotenv
import re

load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Configuring the Generative AI model
if not api_key:
    st.error("Google API key not found. Please set the 'GOOGLE_API_KEY' environment variable.")
else:
    gai.configure(api_key=api_key)
    model = gai.GenerativeModel('gemini-1.5-flash')

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style.css")

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

def ats_check(jd, resume):
    jd_keywords = set(re.findall(r'\b\w+\b', jd.lower()))
    resume_keywords = set(re.findall(r'\b\w+\b', resume.lower()))
    
    matched_keywords = jd_keywords & resume_keywords
    
    # Calculate score as the ratio of matched keywords to total keywords in the job description
    score = len(matched_keywords) / len(jd_keywords) if jd_keywords else 0
    
    return score, matched_keywords

st.markdown("<h1 style='text-align: center; color: #2e3b4e;'>Resume Copilot</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: #2e3b4e;'>Get ATS Optimized Resume with the help of latest AI technology</h3>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

jd = st.text_area("Enter Job Description", placeholder="Enter the job description here...")
info = st.text_area("Enter your information", placeholder="Enter your personal information here...")
res = st.text_area("Enter LaTeX Resume Template:", placeholder="Paste your LaTeX resume template here...")

if st.button("Generate TeX Resume"):
    if jd and info and res:
        try:
            resp = get_resume_tex(jd, info, res)
            st.text_area("Here's your TeX Resume:", value=resp, height=600)
            
            # ATS Check
            ats_score, matched_keywords = ats_check(jd, resp)
            st.markdown(f"### ATS Score: {ats_score:.2f}")
            st.markdown(f"#### Matched Keywords: {', '.join(matched_keywords)}")
        except Exception as e:
            st.error(f"Error generating TeX resume: {e}")
    else:
        st.error("Please enter all the required fields")

if st.button("Generate Markdown Resume"):
    if jd and info and not res:
        try:
            resp = get_resume_mk(info, jd)
            st.text_area("Here's your Markdown Resume:", value=resp, height=600)
            
            # ATS Check
            ats_score, matched_keywords = ats_check(jd, resp)
            st.markdown(f"### ATS Score: {ats_score:.2f}")
            st.markdown(f"#### Matched Keywords: {', '.join(matched_keywords)}")
        except Exception as e:
            st.error(f"Error generating Markdown resume: {e}")
    else:
        st.error("Please enter all the required fields")

st.subheader("The program above outputs code in either TeX or Markdown, which you can then modify to suit your needs.")
