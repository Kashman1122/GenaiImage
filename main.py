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

# Initialize the models
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to get response from model
def get_data(question, image=None):
    if question and image is not None:
        response = model.generate_content([question, image])
        return response.text
    elif question:
        response = model.generate_text(question)
        return response.text
    return "No response"

# Streamlit UI
st.title("AI Assistant with Image and Chat Support")

# Chat message container
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(
            f'<div style="text-align:right; background-color:#DCF8C6; padding:8px; border-radius:8px; margin:4px 0;">'
            f'<strong>You:</strong> {msg["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="text-align:left; background-color:#F0F0F0; padding:8px; border-radius:8px; margin:4px 0;">'
            f'<strong>AI:</strong> {msg["content"]}</div>',
            unsafe_allow_html=True,
        )

# Image uploader
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], key="file_upload")

# Camera input (supports Android devices)
camera_image = st.camera_input("Capture an image using your camera", key="camera_input")

# Input area at the bottom
st.markdown("<div style='position:fixed; bottom:10px; width:100%;'>", unsafe_allow_html=True)
input_col1, input_col2 = st.columns([4, 1])

# Text input
with input_col1:
    user_input = st.text_input("Type your message here:", "", key="text_input")

# Send button
with input_col2:
    if st.button("Send"):
        if user_input:
            st.session_state.messages.append({"is_user": True, "content": user_input})

            # Check if there's an image input
            if uploaded_image or camera_image:
                image = Image.open(uploaded_image or camera_image)
                ai_response = get_data(user_input, image)
            else:
                ai_response = get_data(user_input)

            st.session_state.messages.append({"is_user": False, "content": ai_response})

        else:
            st.warning("Please enter a message.")

st.markdown("</div>", unsafe_allow_html=True)
