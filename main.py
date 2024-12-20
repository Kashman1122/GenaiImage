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

# Function to generate AI responses
def get_data(question, image=None):
    if question and image:
        response = model.generate_content([question, image])
        return response.text
    elif question:
        response = model.generate_content(question)
        return response.text
    return "No response"

# Streamlit page configuration
st.set_page_config(page_title="AI Chat Assistant", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #121212;
            color: white;
        }
        .chat-container {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 15px;
            max-height: 600px;
            overflow-y: auto;
            margin-bottom: 20px;
        }
        .chat-bubble-user {
            text-align: right;
            background-color: #4caf50;
            color: white;
            display: inline-block;
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
        }
        .chat-bubble-ai {
            text-align: left;
            background-color: #444;
            color: white;
            display: inline-block;
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
        }
        .input-container {
            display: flex;
            justify-content: center;
            align-items: center;
            position: fixed;
            bottom: 10px;
            width: 100%;
            padding: 10px;
            background-color: #1e1e1e;
            border-radius: 10px;
        }
        .input-box {
            flex-grow: 1;
            padding: 10px;
            border: none;
            background-color: #333;
            color: white;
            border-radius: 5px;
            margin-right: 10px;
        }
        .input-box:focus {
            outline: none;
        }
        .send-button {
            border: none;
            background-color: #4caf50;
            color: white;
            border-radius: 5px;
            padding: 10px;
            cursor: pointer;
        }
        .camera-button {
            border: none;
            background-color: #444;
            color: white;
            border-radius: 5px;
            padding: 10px;
            cursor: pointer;
            margin-left: 5px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat messages
for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Camera toggle logic
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

# Camera Button Handling
if st.session_state.camera_active:
    camera_image = st.camera_input("Capture an image", label_visibility="collapsed")
else:
    camera_image = None

# Input area
user_input = st.text_input("Type your message...", key="text_input", label_visibility="collapsed")

# Buttons for actions
col1, col2, col3 = st.columns([2, 1, 1])
with col2:
    if st.button("📷 Open Camera"):
        st.session_state.camera_active = not st.session_state.camera_active
with col3:
    if st.button("➤ Send"):
        if user_input.strip():
            st.session_state.messages.append({"is_user": True, "content": user_input})
            image = None

            if camera_image:
                image = Image.open(camera_image)

            # Get AI response
            ai_response = get_data(user_input, image)
            st.session_state.messages.append({"is_user": False, "content": ai_response})
        else:
            st.warning("Please enter a message.")
