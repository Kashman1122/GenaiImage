import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the models
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get response from model
def get_data(question, image):
    if question and image is not None:
        response = model.generate_content([question, image])
        return response.text
    return "No response"

# Streamlit UI
st.title("Image Analysis with Generative AI")

# Image uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Camera input (supports Android devices)
camera_image = st.camera_input("Capture an image using your camera")

# Ask a question
question = st.text_input("Ask a question about the image:", "What is inside the image?")

# Process the image (uploaded or captured)
if st.button("Get AI Response"):
    if camera_image is not None:
        # Convert captured camera image to PIL format
        image = Image.open(camera_image)
        response = get_data(question, image)
        st.write("AI Response: ", response)
    elif uploaded_image is not None:
        # Use uploaded image
        image = Image.open(uploaded_image)
        response = get_data(question, image)
        st.write("AI Response: ", response)
    else:
        st.warning("Please upload an image or capture one using the camera.")
