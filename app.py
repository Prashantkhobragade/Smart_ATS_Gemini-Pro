import streamlit as st 
import google.generativeai as genai 
import os
from dotenv import load_dotenv 
import PyPDF2 as pdf 



#load env variable
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

genai.configure(api_key=GOOGLE_API_KEY)


def get_gemini_response(input):
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(input)
    return response.text


def input_pdf_text(uploaded_file):
    reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in range(len(reader.pages)):
        page = reader.pages[page]
        text += str(page.extract_text())
    return text

#Prompt Template

input_prompt = """
hey Act like a skilled or very experience ATS(Application Tracking System).
with a deep understanding of tech field, software engineering, data scientist,
data analyst, ML Engineer and big data enginner. Your task is to 
evaluate the resume based on the given job description.
You must consider the job market is very competitave and you should 
provide best assistance for improving the resumes. Assign the percentage
Matching based on Jd and the missing Ketwords with high accuracy.
resume:{text}
description:{jd}

I want the response in one string having the structure{{"JD Match": "%", "Missing Keywords":[], "Profile summary":}}
"""
    
## Streamlit App
st.title("Smart ATS Powered By Gemini Pro")
st.text("Improve your Resume with our ATS powered by Gemini Pro")
jd = st.text_input("Enter your Job Description")
uploaded_file = st.file_uploader("Upload your Resume", type=["pdf"])

submit = st.button("Submit")

if submit:
    if uploaded_file is not None:
        text = input_pdf_text(uploaded_file)
        response = get_gemini_response(input_prompt)
        st.subheader("Smart ATS Response: ")
        st.write(response)
