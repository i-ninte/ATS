import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the Generative AI API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to get the response from Gemini API
def get_gemini_response(input_text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        st.error(f"Error fetching response from Gemini API: {e}")
        return None

# Function to extract text from uploaded PDF
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None

# Streamlit app interface
st.title("ATS Resume Evaluator")

# Job description input
job_description = st.text_area("Enter the Job Description", height=150)

# Resume file upload
uploaded_file = st.file_uploader("Upload your resume as a PDF", type=["pdf"])

# Submit button
if st.button("Submit"):
    if not job_description:
        st.error("Please enter the job description.")
    elif not uploaded_file:
        st.error("Please upload your resume.")
    else:
        # Extract text from PDF
        resume_text = input_pdf_text(uploaded_file)
        
        if resume_text:
            # Prepare input prompt for Gemini API
            input_prompt = f"""
            Hey act like a skilled or very experienced ATS (Application Tracking System)
            with a deep understanding of tech fields, software engineering, data science, data analysis, AI/ML,
            and big data engineering.
            Your task is to evaluate the resume based on the given job description.
            You must consider the job market to be very competitive, and you should provide
            the best assistance for improving the resume. Assign the percentage Matching based on the job description 
            and the missing keywords with high accuracy. 
            Resume: {resume_text}
            Job Description: {job_description}
            I want the response in one single string with the structure:
            {{"JD Match": "%", "MissingKeywords": [], "Profile Summary": ""}}
            """
            
            # Get response from Gemini API
            response = get_gemini_response(input_prompt)
            
            if response:
                st.success("Evaluation completed.")
                st.write(response)
            else:
                st.error("Failed to generate a response. Please try again.")
