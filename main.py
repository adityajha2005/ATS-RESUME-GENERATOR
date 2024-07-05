import streamlit as st
import os
import google.generativeai as gai
from dotenv import load_dotenv

load_dotenv()
gai.configure(api_key=os.environ['GOOGLE_API_KEY'])

model = gai.GenerativeModel('gemini-1.5-flash')

def get_resume_tex(jd,information,resume):


def get_resume_mk(information,jd):

st.title("Resume Copilot")
st.header("Get ATS Optimized Resume with the help of latest AI technology")
jd=st.text_area("Enter Job Description")
info=st.text_area("Enter your information")
res=st.text_area("Enter LaTeX Resume Template: ")


if st.button("Generate TeX Resume"):
    if jd and info and res:
        resp = get_resume_tex(jd,info,res)
        st.text_area("Here's your TeX Resume:",value=resp,height=600)
    else:
        st.error("Please enter all the required fields")
    
if st.button("Generate Markdown Resume"):
    if jd and info and not res:
        resp=get_resume_mk(info,id)
        st.text_area("Here's your Markdown Resume:",value=resp,height=600)
    else:
        st.error("Please enter all the required fields")

st.subheader("The program above outputs code in either TeX or Markdown, which you can then modify to suit your needs.")