import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json
import re

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
st.set_page_config(
    page_title="JobMatch: ATS Resume Evaluator", 
    page_icon="💼", 
    layout="centered", 
    initial_sidebar_state="collapsed"
)

# Custom CSS for light and dark modes
st.markdown("""
    <style>
        /* Light mode */
        body, .main {
            background-color: #f0f2f6;
            color: #000;
        }
        h1, h2, h3, h4, h5, h6, label {
            color: #4CAF50;
        }
        p, textarea, .stTextInput input, .stTextArea textarea {
            color: #000;
            background-color: #fff;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }

        /* Dark mode */
        @media (prefers-color-scheme: dark) {
            body, .main {
                background-color: #121212;
                color: #fff;
            }
            h1, h2, h3, h4, h5, h6, label {
                color: #80d4ff;
            }
            p, textarea, .stTextInput input, .stTextArea textarea {
                background-color: #333;
                color: #fff;
                border: 1px solid #80d4ff;
            }
            .stButton button {
                background-color: #80d4ff;
                color: black;
                border-radius: 10px;
                padding: 10px 20px;
            }
            .stButton button:hover {
                background-color: #66c2e8;
            }
        }
    </style>
""", unsafe_allow_html=True)

# App title
st.title("JobMatch: ATS Resume Evaluator 💼")

# Instructions and description
st.markdown("""
    Welcome to **JobMatch**, the ATS Resume Evaluator!  
    Simply upload your resume, enter the job description, and get a detailed analysis of how well your resume matches the job, with suggestions for improvement.
""")

# Job description input
st.subheader("Job Description")
job_description = st.text_area("Enter the Job Description", height=150)

# Resume file upload
st.subheader("Upload Resume")
uploaded_file = st.file_uploader("Upload your resume as a PDF", type=["pdf"])

# Submit button
if st.button("Submit"):
    if not job_description:
        st.error("Please enter the job description.")
    elif not uploaded_file:
        st.error("Please upload your resume.")
    else:
        resume_text = input_pdf_text(uploaded_file)
        if resume_text:
            input_prompt = f"""
            Act as a skilled ATS (Applicant Tracking System) with deep understanding of tech fields, software engineering,
            data science, data analysis, AI/ML, and big data engineering.
            Evaluate the resume based on the given job description. Consider the job market very competitive and provide
            the best assistance for improving the resume.
            Assign the percentage Matching based on the job description and identify missing keywords with high accuracy.
            Also suggest only one best fit alternative job type the candidate might be suitable for.

            Resume: {resume_text}
            Job Description: {job_description}

            Respond with a JSON string structured as follows:
            {{
                "JD Match": "%",
                "MissingKeywords": [],
                "ProfileSummary": "",
                "Advice": [],
                "AlternativeJob": ""
            }}
            """

            response = get_gemini_response(input_prompt)

            # Clean up the response (remove ```json and other irregularities)
            cleaned_response = re.sub(r'```json|```', '', response).strip()

            if cleaned_response:
                try:
                    # Parse the cleaned_response as JSON
                    result = json.loads(cleaned_response)
                    
                    # Display JD Match
                    st.markdown("## Job Description Match")
                    st.markdown(f"<h1 style='text-align: center; color: #1e90ff;'>{result['JD Match']}</h1>", unsafe_allow_html=True)
                    
                    # Display Missing Keywords
                    st.subheader("Missing Keywords")
                    if result['MissingKeywords']:
                        st.write(", ".join(result['MissingKeywords']))
                    else:
                        st.write("No missing keywords identified.")
                    
                    # Display Profile Summary
                    st.subheader("Profile Summary")
                    st.write(result['ProfileSummary'])
                    
                    # Display Advice for Improving Match
                    st.subheader("How to Improve Your Match")
                    if result['Advice']:
                        for advice in result['Advice']:
                            st.write(f"- {advice}")
                    else:
                        st.write("No specific advice provided.")
                    
                    # Display Alternative Job Types
                    st.subheader("Alternative Job Type to Consider")
                    alternativeJob = result.get("AlternativeJob", "")
                    if alternativeJob:
                        st.write(alternativeJob)
                    else:
                        st.write("No alternative job types suggested.")
                    
                except json.JSONDecodeError as e:
                    st.error(f"Failed to parse the response nicely.")
                    st.write("Raw response:")
                    st.write(response)
            else:
                st.error("Failed to generate a response. Please try again.")
