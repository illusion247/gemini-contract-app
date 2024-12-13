import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import io

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
            Analyze the following contract document and extract the following information:

            1. Termination Notice No. of Days:  How many days are required to give for a termination notice, and indicate which party is terminating the contract.
            2. Auto Renewal: Does the contract contains a renewal clause, if so please include details. Find infromation that refers to the renewal of contract.
            3. Signed Date of the Client (client): Extract the date signed by the client. 
            4. Effectivity Date: find infromation or clause about the effectivity date of the contract. 

            additional instruction: provide the page number and section for reference if information is available 
           
            Note: The Service Provider is always Towers Watson or Willis Towers Watson. Please extract only the Client's Signature Date.
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
st.title("Contract Information Extractor")
uploaded_file = st.file_uploader("Upload a Contract PDF", type="pdf")

if uploaded_file:
    with st.spinner("Extracting information..."):
       extracted_data = extract_info_gemini_vision(uploaded_file)
       if extracted_data:
          st.success("Information extracted successfully!")
          st.write(extracted_data)
       else:
          st.error("Error during information extraction.")
