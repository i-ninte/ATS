# JobMatch: ATS Resume Evaluator 💼

Welcome to **JobMatch**, an ATS (Application Tracking System) Resume Evaluator that leverages Google's Gemini Generative AI to analyze how well your resume matches a given job description and provides suggestions for improvement.

## Table of Contents
- [Overview](#overview)
- [Installation](#installation)
- [Environment Setup](#environment-setup)
- [Usage](#usage)
- [Code Walkthrough](#code-walkthrough)
  - [Streamlit Setup](#streamlit-setup)
  - [Google Generative AI Integration](#google-generative-ai-integration)
  - [PDF Text Extraction](#pdf-text-extraction)
  - [App Interface](#app-interface)
- [Contributing](#contributing)
- [License](#license)

## Overview

**JobMatch** is a web-based tool built using [Streamlit](https://streamlit.io/) and integrated with [Google's Gemini Generative AI](https://cloud.google.com/ai/gemini). The app allows users to upload their resumes in PDF format, input a job description, and receive an AI-generated evaluation that includes:
- **Percentage match** between the resume and the job description.
- **Missing keywords** required to improve the resume.
- **Profile summary** aligned with the job description.

## Installation

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/i-ninte/ATS.git
   cd ATS
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Environment Setup

The project uses environment variables to store sensitive information, such as API keys. Follow these steps to set up your environment:

1. Create a `.env` file in the root directory.
2. Add your **Google API Key** to the `.env` file:
   ```bash
   GOOGLE_API_KEY=your_google_api_key
   ```

## Usage

To start the app locally, run:
```bash
streamlit run app.py
```

Once the app is running, you can:
1. Enter a job description.
2. Upload your resume as a PDF file.
3. Click the **Submit** button to get your resume evaluation.

## Code Walkthrough

### Streamlit Setup

The Streamlit framework powers the UI of the application. The app is configured with a page title and icon:

```python
st.set_page_config(
    page_title="JobMatch: ATS Resume Evaluator", 
    page_icon="💼", 
    layout="centered"
)
```

### Google Generative AI Integration

We use the Google Generative AI API to process the input and provide a detailed analysis. The API is configured using an API key stored in environment variables:

```python
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
```

The `get_gemini_response` function sends the user's resume and job description to the Gemini API for evaluation:

```python
def get_gemini_response(input_text):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        st.error(f"Error fetching response from Gemini API: {e}")
        return None
```

### PDF Text Extraction

The `input_pdf_text` function extracts the text from an uploaded PDF file using the PyPDF2 library:

```python
def input_pdf_text(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF file: {e}")
        return None
```

### App Interface

The user interface allows users to upload a resume, input the job description, and submit the data for evaluation. The key elements include:

1. **Job Description Input**:
   ```python
   job_description = st.text_area("Enter the Job Description", height=150)
   ```

2. **Resume Upload**:
   ```python
   uploaded_file = st.file_uploader("Upload your resume as a PDF", type=["pdf"])
   ```

3. **Submit Button**:
   Once the user inputs both the job description and resume, they can click the **Submit** button to trigger the evaluation:

   ```python
   if st.button("Submit"):
       resume_text = input_pdf_text(uploaded_file)
       input_prompt = f"..."  # Generate prompt for API
       response = get_gemini_response(input_prompt)
       st.json(response)  # Display the AI response in JSON format
   ```

The results include the **matching percentage**, **missing keywords**, and a **profile summary**.

## Contributing

Contributions are welcome! If you'd like to contribute, please fork the repository and submit a pull request.
