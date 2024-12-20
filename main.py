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
        response = model.generate_text(question)
        return response.text
    return "No response"

# Streamlit UI Configuration
st.set_page_config(page_title="AI Assistant", layout="wide")
st.markdown(
    """
    <style>
        body {
            background-color: #1e1e1e;
            color: white;
        }
        .chat-container {
            background-color: #2e2e2e;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 10px;
            overflow-y: auto;
            max-height: 400px;
        }
        .chat-bubble-user {
            text-align: right;
            color: #000;
            background-color: #4caf50;
            display: inline-block;
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
        }
        .chat-bubble-ai {
            text-align: left;
            color: #000;
            background-color: #f0f0f0;
            display: inline-block;
            padding: 10px;
            border-radius: 15px;
            margin: 5px 0;
            max-width: 70%;
        }
        .input-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            background-color: #3e3e3e;
            border-radius: 10px;
            padding: 5px 10px;
        }
        .input-container input {
            flex-grow: 1;
            border: none;
            background-color: transparent;
            color: white;
            outline: none;
        }
        .input-container button {
            border: none;
            background-color: #4caf50;
            color: white;
            border-radius: 50%;
            padding: 8px;
            cursor: pointer;
        }
        .camera-icon {
            margin-left: 10px;
            cursor: pointer;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💬 AI Assistant: Dark Mode Chat")

# Initialize session state for chat messages
if "messages" not in st.session_state:
    st.session_state.messages = []

# Chat history container
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Input area with camera icon
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")
camera_image = st.camera_input("Capture an image", label_visibility="collapsed")

st.markdown(
    """
    <div class="input-container">
        <input id="text_input" type="text" placeholder="Type your message here..." />
        <img src="https://img.icons8.com/material-outlined/24/ffffff/camera.png" class="camera-icon" />
        <button id="send_button">➤</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# Process input
if st.button("Send"):
    user_input = st.text_input("Enter your message:", "", key="text_input", label_visibility="collapsed")
    if user_input.strip():
        st.session_state.messages.append({"is_user": True, "content": user_input})

        # Handle image input
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
