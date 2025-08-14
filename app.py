import os
import streamlit as st
import pytesseract
from PIL import Image
import openai

# Load OpenAI API key securely from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

st.set_page_config(page_title="HealthEase OCR + AI + Doctor Notes", layout="wide")

st.title("📄 HealthEase Medical Report Assistant")

st.sidebar.header("Upload & Process")
uploaded_file = st.sidebar.file_uploader("Upload a medical report image", type=["png", "jpg", "jpeg"])

# Doctor notes storage (session-based for now)
if "doctor_notes" not in st.session_state:
    st.session_state["doctor_notes"] = []

def extract_text_from_image(image):
    """Extract text from image using Tesseract OCR"""
    return pytesseract.image_to_string(image)

def simplify_text_with_ai(text):
    """Use OpenAI to simplify medical text"""
    prompt = f"Summarize and explain this medical report in simple language for a patient:\n{text}"
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful medical assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.4
    )
    return response.choices[0].message["content"]

if uploaded_file:
    st.subheader("🖼 Uploaded Report")
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Medical Report", use_column_width=True)

    with st.spinner("Extracting text from image..."):
        extracted_text = extract_text_from_image(image)

    st.subheader("📜 Extracted Text")
    st.text_area("OCR Output", extracted_text, height=200)

    if st.button("Simplify with AI"):
        with st.spinner("Generating patient-friendly summary..."):
            simplified_text = simplify_text_with_ai(extracted_text)
        st.subheader("🩺 AI Simplified Report")
        st.write(simplified_text)

# Doctor notes section
st.sidebar.subheader("Doctor's Panel")
doctor_comment = st.sidebar.text_area("Write doctor's comments/prescription here")

if st.sidebar.button("Save Doctor's Note"):
    st.session_state["doctor_notes"].append(doctor_comment)
    st.sidebar.success("Doctor's note saved.")

st.subheader("📌 Doctor's Notes & Prescriptions")
for idx, note in enumerate(st.session_state["doctor_notes"], 1):
    st.markdown(f"**{idx}.** {note}")
