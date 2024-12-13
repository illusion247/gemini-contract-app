import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO

load_dotenv()

# Set up Gemini API client
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Load the model
model = genai.GenerativeModel("gemini-pro") # Use "gemini-pro" for text only input, use "gemini-pro-vision" if you are working with documents

# Functions
def extract_text_from_pdf(pdf_file):
     try:
          text = ""
          pdf_file_object = BytesIO(pdf_file.read())
          pdf_reader = PyPDF2.PdfReader(pdf_file_object)
          for page_num in range(len(pdf_reader.pages)):
               page = pdf_reader.pages[page_num]
               page_text = page.extract_text()
               text+=page_text
          return text
     except Exception as e:
          print(f"Error extracting text from PDF: {e}")
          return None

def extract_info_gemini(text):
    if text:
      prompt = f"""
            Analyze the following contract document text and extract the following information:

            1. Termination Notice No. of Days:  How many days are required to give for a termination notice, and indicate which party is terminating the contract.
            2. Auto Renewal: Does the contract contains a renewal clause, if so please include details.
            3. Signed Date of the Client (Service Provider): Extract the date signed by the client.

            Text: {text}
        """
      try:
        response = model.generate_content(prompt)
        return response.text
      except Exception as e:
          return f"Error querying Gemini API: {e}"
    else:
        return "No text extracted from PDF"

# Streamlit app
st.title("Contract Information Extractor with Gemini")
uploaded_file = st.file_uploader("Upload a Contract PDF", type="pdf")


if uploaded_file:
    with st.spinner("Extracting information..."):
         text = extract_text_from_pdf(uploaded_file)
         if text:
            extracted_data = extract_info_gemini(text)
            st.success("Information extracted successfully!")
            st.write(extracted_data)
         else:
              st.error ("Error extracting text from the uploaded file")
