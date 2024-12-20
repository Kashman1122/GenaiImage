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
    try:
        if question and image:
            response = model.generate_content([question, image])
            return response.text
        elif question:
            response = model.generate_content(question)
            return response.text
    except Exception as e:
        return f"Error: {str(e)}"
    return "No response."

# Streamlit page configuration
st.set_page_config(page_title="AI Chat Assistant", layout="wide")
st.markdown(
    """
    <style>
    body {
        background-color: #121212;
        color: white;
        font-family: Arial, sans-serif;
    }
    .chat-container {
        width: 80%;
        max-width: 800px;
        height: 90vh;
        margin: auto;
        display: flex;
        flex-direction: column;
        background-color: #1e1e1e;
        border-radius: 10px;
        overflow: hidden;
    }
    .chat-messages {
        flex: 1;
        padding: 10px;
        overflow-y: auto;
    }
    .chat-bubble-user, .chat-bubble-ai {
        padding: 10px;
        margin: 5px;
        border-radius: 10px;
        max-width: 75%;
    }
    .chat-bubble-user {
        background-color: #4caf50;
        color: white;
        align-self: flex-end;
    }
    .chat-bubble-ai {
        background-color: #444;
        color: white;
        align-self: flex-start;
    }
    .chat-input-area {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px;
        background-color: #2c2c2c;
    }
    .chat-input {
        flex: 1;
        padding: 10px;
        border: none;
        border-radius: 5px;
        margin-right: 10px;
        font-size: 16px;
        color: white;
        background-color: #1e1e1e;
    }
    .camera-button, .send-button {
        padding: 10px 15px;
        border: none;
        border-radius: 5px;
        font-size: 16px;
        cursor: pointer;
        color: white;
    }
    .camera-button {
        background-color: #4caf50;
        margin-right: 5px;
    }
    .send-button {
        background-color: #2196f3;
    }
    .camera-button:hover {
        background-color: #45a049;
    }
    .send-button:hover {
        background-color: #0b7dda;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if "captured_image" not in st.session_state:
    st.session_state.captured_image = None

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

# Display chat messages
st.markdown("<div class='chat-messages'>", unsafe_allow_html=True)
for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Camera functionality
if st.session_state.camera_active:
    st.session_state.captured_image = st.camera_input("Capture an image", label_visibility="collapsed")
else:
    st.session_state.captured_image = None

# Input area
col1, col2, col3 = st.columns([8, 1, 1])
with col1:
    user_input = st.text_input("Type your message...", key="text_input", label_visibility="collapsed")
with col2:
    if st.button("📷 Open Camera"):
        st.session_state.camera_active = not st.session_state.camera_active
with col3:
    if st.button("➤ Send"):
        if user_input.strip():
            # Add user message to session
            st.session_state.messages.append({"is_user": True, "content": user_input})

            # Prepare image if captured
            image = None
            if st.session_state.captured_image:
                image = Image.open(st.session_state.captured_image)

            # Get AI response
            ai_response = get_data(user_input, image)
            st.session_state.messages.append({"is_user": False, "content": ai_response})
        else:
            st.warning("Please enter a message.")

st.markdown("</div>", unsafe_allow_html=True)
