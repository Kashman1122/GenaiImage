import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
import cv2
import numpy as np
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

# Function to capture an image from the webcam
def capture_image():
    cap = cv2.VideoCapture(0)  # Open the webcam
    st.text("Press 's' to capture an image or 'q' to quit.")
    captured_image = None
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image.")
            break
        # Display the live camera feed
        st.image(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB), channels="RGB", use_column_width=True)
        
        key = cv2.waitKey(1) & 0xFF
        if key == ord('s'):  # Capture image
            captured_image = frame
            break
        elif key == ord('q'):  # Quit
            break
    
    cap.release()
    cv2.destroyAllWindows()
    return captured_image

# Streamlit UI
st.title("Image Analysis with Generative AI")

# Image uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Option to use live camera
use_camera = st.checkbox("Use live camera to capture an image")

captured_image = None
if use_camera:
    if st.button("Open Camera"):
        captured_image = capture_image()
        if captured_image is not None:
            st.image(cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB), caption="Captured Image", use_column_width=True)

# Ask a question
question = st.text_input("Ask a question about the image:", "What is inside the image?")

# Process the image (uploaded or captured)
if st.button("Get AI Response"):
    if captured_image is not None:
        # Convert captured image to PIL format
        image = Image.fromarray(cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB))
        response = get_data(question, image)
        st.write("AI Response: ", response)
    elif uploaded_image is not None:
        # Use uploaded image
        image = Image.open(uploaded_image)
        response = get_data(question, image)
        st.write("AI Response: ", response)
    else:
        st.warning("Please upload an image or capture one using the camera.")
