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

if uploaded_image is not None:
    # Display uploaded image
    image = Image.open(uploaded_image)
    st.image(image, caption="Uploaded Image", use_column_width=True)

    # Ask a question
    question = st.text_input("Ask a question about the image:", "What is inside the image?")

    if st.button("Get AI Response"):
        # Get response from the model
        response = get_data(question, image)
        st.write("AI Response: ", response)

