import streamlit as st
import requests
from PIL import Image
import io
import pathlib



def load_css(file_path):
    with open(file_path, "r") as f:
        css = f.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


css_path = pathlib.Path("style.css")  
load_css(css_path)


# Title of the app
st.markdown('<p class="title"> Brain Disorder Diagnosis AI</p>', unsafe_allow_html=True)

# Sidebar for Navigation
st.sidebar.markdown("<h2 class='header'>🧭 Navigation</h2>", unsafe_allow_html=True)

app_mode = st.sidebar.selectbox("Choose the app mode", ["Diagnosis", "Chatbot"])
st.sidebar.markdown(
    '<h3 class="heading">📖 User Guide</h3>',
    unsafe_allow_html=True
)
st.sidebar.markdown(
    """
    <div class="custom-info">
        🔹 <b>Diagnosis Mode</b>: Upload an MRI scan for analysis.<br><br>
        🔹 <b>Chatbot Mode</b>: Ask AI questions about the diagnosis.<br><br>
        🔹 <b>Results</b>: AI will show predictions with confidence scores.
    </div>
    """,
    unsafe_allow_html=True
)  

#  About AI Model
st.sidebar.markdown(
    '<h3 class="heading">🤖 About AI Model</h3>',
    unsafe_allow_html=True
)
st.sidebar.markdown('<p class="Ai"> Our AI uses deep learning to analyze MRI scans for brain disorders.</p>',unsafe_allow_html=True)

#  Contact & Support
st.sidebar.markdown(
    '<h3 class="heading">📞 Contact Us</h3>',
    unsafe_allow_html=True
)

st.sidebar.markdown(
    '<p class="email-text">✉️ Email: support@brainai.com</p>',   
    unsafe_allow_html=True
)



if app_mode == "Diagnosis":
    st.markdown('<h2 class="header">Upload MRI Scan for Analysis</h2>', unsafe_allow_html=True)

    uploaded_file = st.file_uploader("Upload an MRI scan (JPG, PNG, or DICOM)", type=["jpg", "png", "dcm"])
    
    if uploaded_file is not None:
        try:
            # For common image formats
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded MRI Scan", use_container_width=True)
        except Exception as e:
            st.error("Error reading image. Make sure the file is a valid image format.")

        if st.button("Analyze MRI"):
            # Convert the file to bytes for the API
            file_bytes = uploaded_file.getvalue()
            files = {"file": file_bytes}
        try:
                response = requests.post("http://127.0.0.1:5000/analyze", files=files)
                data = response.json()
                st.success(f"Prediction: {data.get('result', 'N/A')}")
                st.info(f"Confidence Score: {data.get('confidence', 'N/A')}%")
                
                # Display Grad-CAM heatmap if provided by the backend
                if data.get("heatmap"):
                    # Assuming the backend returns an image URL or base64 string; here we expect a URL.
                    st.image(data["heatmap"], caption="Grad-CAM Heatmap", use_column_width=True)
                    
        except Exception as e:
                st.error(f"Error contacting the AI model: {e}")


if app_mode == "Chatbot":
    
    st.markdown('<h2 class="header">Upload MRI Scan for Analysis</h2>', unsafe_allow_html=True)

    st.markdown('<p style="font-size:20px; color:black;">Ask any question regarding the AI diagnosis, such as:</p>', unsafe_allow_html=True)

    st.write("- Why was this scan classified as Alzheimer’s-positive?")
    st.write("- What features did the model consider important?")
    
    user_question = st.text_input("Enter your question here:")
    
    if st.button("Send"):
        if user_question:
            try:
                # Create a payload with the user's question
                payload = {"question": user_question}
                response = requests.post("http://127.0.0.1:5000/chat", json=payload)
                data = response.json()
                st.write("**AI Explanation:**")
                st.write(data.get("answer", "No answer provided."))
            except Exception as e:
                st.error(f"⚠ Chatbot Error: {e}")
        else:
            st.warning("⚠ Please type a question first before sending.")

  


