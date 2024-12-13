import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io
import PyPDF2

load_dotenv()

# Set up Gemini API client
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# Load the model
model = genai.GenerativeModel("gemini-1.5-flash")  # Use gemini-1.5-flash

# Function to extract info directly from PDF with Gemini
def extract_info_gemini_vision(pdf_file):
    if pdf_file:
        prompt = f"""
            Analyze the following contract document and extract the following information, make sure to indicate which page number and section number that the information is from, and if the information cannot be found please indicate that it was not found. Format the output as follows:
             1. Termination Notice No. of Days: <Termination Notice and which party is giving the notice>, Page(s): <page number(s)>, Section(s): <section number(s)>
             2. Auto Renewal: <Renewal Clause Details>, Page(s): <page number(s)>, Section(s): <section number(s)>
             3. Signed Date of the Client (Client): <Date of the client signing>, Page(s): <page number(s)>, Section(s): <section number(s)>
             
             Note: The Service Provider is always Towers Watson or Willis Towers Watson. Please extract only the Client's Signature Date.

            Text: 
            """
        try:
             pdf_content = pdf_file.read()
             response = model.generate_content([prompt, {"mime_type": "application/pdf", "data": pdf_content}])
             return response.text
        except Exception as e:
            return f"Error querying Gemini API: {e}"
    else:
         return "No file Uploaded"

# Streamlit app
st.title("Contract Information Extractor with Gemini Vision")
uploaded_file = st.file_uploader("Upload a Contract PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting information..."):
       extracted_data = extract_info_gemini_vision(uploaded_file)
       if extracted_data:
          st.success("Information extracted successfully!")
          st.write(extracted_data)
       else:
          st.error("Error during information extraction.")
