# import streamlit as st
# from PIL import Image
# import google.generativeai as genai
# import os
# from dotenv import load_dotenv

# # Load environment variables
# load_dotenv()
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# # Initialize the models
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Function to get response from model
# def get_data(question, image):
#     if question and image is not None:
#         response = model.generate_content([question, image])
#         return response.text
#     return "No response"

# # Streamlit UI
# st.title("Image Analysis with Generative AI")

# # Image uploader
# uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# # Camera input (supports Android devices)
# camera_image = st.camera_input("Capture an image using your camera")

# # Ask a question
# question = st.text_input("Ask a question about the image:", "What is inside the image?")

# # Process the image (uploaded or captured)
# if st.button("Get AI Response"):
#     if camera_image is not None:
#         # Convert captured camera image to PIL format
#         image = Image.open(camera_image)
#         response = get_data(question, image)
#         st.write("AI Response: ", response)
#     elif uploaded_image is not None:
#         # Use uploaded image
#         image = Image.open(uploaded_image)
#         response = get_data(question, image)
#         st.write("AI Response: ", response)
#     else:
#         st.warning("Please upload an image or capture one using the camera.")


import streamlit as st
from PIL import Image
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate a response
def get_data(question, image=None):
    if question and image:
        response = model.generate_content([question, image])
        return response.text
    elif question:
        response = model.generate_content(question)
        return response.text
    return "No response"

# Streamlit UI
st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("🧠 AI Assistant: Chat & Image Analysis")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat display container
st.markdown("<div style='height:500px; overflow-y:scroll; padding:10px; border:1px solid #ccc; border-radius:10px;'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(
            f"<div style='text-align:right;'><span style='display:inline-block; background-color:#DCF8C6; padding:10px; border-radius:15px; margin:5px; max-width:70%;'>{msg['content']}</span></div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f"<div style='text-align:left;'><span style='display:inline-block; background-color:#F0F0F0; padding:10px; border-radius:15px; margin:5px; max-width:70%;'>{msg['content']}</span></div>",
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

# Image upload and camera capture
uploaded_image = st.file_uploader("Upload an image (optional)", type=["jpg", "jpeg", "png"])
camera_image = st.camera_input("Capture an image (optional)")

# Fixed input area
st.markdown("<div style='position:fixed; bottom:10px; width:100%; background-color:white; padding:10px; border-top:1px solid #ccc;'>", unsafe_allow_html=True)
input_col1, input_col2 = st.columns([5, 1])

# Text input
with input_col1:
    user_input = st.text_input("Type your message here:", "", key="text_input")

# Send button
with input_col2:
    if st.button("Send", key="send_button"):
        if user_input.strip():
            # Add user message
            st.session_state.messages.append({"is_user": True, "content": user_input})

            # Check for image
            image = None
            if camera_image:
                image = Image.open(camera_image)
            elif uploaded_image:
                image = Image.open(uploaded_image)

            # Get AI response
            ai_response = get_data(user_input, image)
            st.session_state.messages.append({"is_user": False, "content": ai_response})
        else:
            st.warning("Please enter a message.")

st.markdown("</div>", unsafe_allow_html=True)
