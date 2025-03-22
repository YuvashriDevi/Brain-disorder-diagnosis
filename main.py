import streamlit as st
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import torch
from torchvision import transforms
from PIL import Image
import time
import shap
import lime
import lime.lime_image
from fpdf import FPDF
import random


st.set_page_config(page_title="AI Chatbot for Alzheimer's MRI Diagnosis", layout="wide")

def load_css(file_name):
    with open(file_name, "r") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Load the external CSS file
load_css("styless.css")

# Enhanced Mock Output Generator

def mock_prediction():
    conditions = ["Alzheimer's Disease (AD)", "Mild Cognitive Impairment (MCI)", "Healthy Control (HC)"]
    diagnosis = random.choice(conditions)
    confidence = round(random.uniform(0.7, 0.99), 2)
    return diagnosis, confidence


def mock_heatmap():
    heatmap = np.random.randn(256, 256) * 255
    heatmap[heatmap < 0] = 0
    heatmap[heatmap > 255] = 255
    return heatmap.astype(np.uint8)


def mock_time_series():
    progression = np.cumsum(np.random.randn(36))
    progression[progression < 0] = 0
    return progression


def mock_shap():
    shap_image = np.random.rand(256, 256, 3) * 255
    return shap_image.astype(np.uint8)


def mock_lime():
    lime_image = np.random.randint(0, 255, (256, 256, 3)).astype(np.uint8)
    return lime_image


# PDF Report Generation
def generate_pdf(diagnosis, confidence):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Alzheimer's MRI Diagnosis Report", ln=True, align='C')
    pdf.cell(200, 10, txt=f"Diagnosis: {diagnosis}", ln=True)
    pdf.cell(200, 10, txt=f"Confidence: {confidence*100:.2f}%", ln=True)
    pdf.output("diagnosis_report.pdf")

# AI Chatbot Functionality

def chatbot_response(query, diagnosis):
    knowledge_base = {
        "What is Alzheimer's Disease?": "Alzheimer's disease is a progressive neurological disorder that leads to memory loss and cognitive decline.",
        "What is MCI?": "Mild Cognitive Impairment (MCI) is an early stage of memory loss or cognitive ability loss.",
        "What is Grad-CAM?": "Grad-CAM (Gradient-weighted Class Activation Mapping) is a visualization technique to see which parts of an image influenced the AI model's decision.",
        "What is LIME?": "LIME (Local Interpretable Model-agnostic Explanations) explains the predictions of black-box AI models in a human-understandable way.",
        "What is SHAP?": "SHAP (SHapley Additive Explanations) helps interpret the contribution of each input feature towards the model's prediction."
    }

    if "diagnosis" in query.lower():
        return f"Based on the MRI scan, the patient has {diagnosis}. Further deterioration is expected."

    for key in knowledge_base:
        if key.lower() in query.lower():
            return knowledge_base[key]

    return "I'm sorry, I currently don't have information about that."

# Streamlit UI Enhancements

st.markdown('<p class="title"> 🧠 AI Chatbot for Alzheimer MRI Diagnosis</p>',unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📁 Upload MRI Scan")
uploaded_file = st.sidebar.file_uploader("Upload MRI Scan (NIfTI/DICOM)", type=["nii", "dcm"])

# Chatbot Interaction
st.sidebar.header("💬 Chat with AI")
user_query = st.sidebar.text_input("Ask a Question")

if uploaded_file:
    st.subheader("📊 MRI Scan Preview")
    
    # Mocking MRI image
    mri_image = np.random.rand(256, 256)
    st.image(mri_image, caption='MRI Brain Scan')

    # Mock Model Prediction
    diagnosis, confidence = mock_prediction()

    st.subheader("🧠 Model Prediction")
   

  

    st.markdown('<div class="result-card diagnosis">🩺 <strong>Diagnosis:</strong> ' + diagnosis + '</div>', unsafe_allow_html=True)
    st.markdown('<div class="result-card confidence">📊 <strong>Confidence:</strong> {:.2f}%</div>'.format(confidence * 100), unsafe_allow_html=True)


    # Mock Grad-CAM Heatmap
    st.subheader("🟠 Brain Damage Heatmap (Grad-CAM)")
    heatmap = mock_heatmap()
    st.image(heatmap, caption='Grad-CAM Heatmap')

    # Mock SHAP Explanation
    st.subheader("🔍 SHAP Explanation")
    shap_image = mock_shap()
    st.image(shap_image, caption='SHAP Explanation')

    # Mock LIME Explanation
    st.subheader("💡 LIME Explanation")
    lime_image = mock_lime()
    st.image(lime_image, caption='LIME Explanation')

    # Mock Time-Series Prediction
    st.subheader("📉 Predicted Disease Progression")
    time_series = mock_time_series()
    st.line_chart(time_series)

    # Chatbot Interaction
    if user_query:
        response = chatbot_response(user_query, diagnosis)
        st.sidebar.write(f"🤖 Answer: {response}")

    # Generate Report Button
    if st.button("Generate PDF Report"):
        generate_pdf(diagnosis, confidence)
        st.success("PDF Report has been generated successfully!")

st.sidebar.info("Note: This is a mock demo. Real model integration will follow.")