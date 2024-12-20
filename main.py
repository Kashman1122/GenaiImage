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
            background-color: #121212;
            color: white;
        }
        .chat-container {
            background-color: #1e1e1e;
            border-radius: 10px;
            padding: 15px;
            max-height: 500px;
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
        .send-button, .camera-button {
            border: none;
            background-color: #4caf50;
            color: white;
            border-radius: 50%;
            padding: 10px;
            cursor: pointer;
        }
        .hidden-camera {
            display: none;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.title("💬 AI Assistant - Dark Mode")

# Chat history container
if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.messages:
    if msg["is_user"]:
        st.markdown(f"<div class='chat-bubble-user'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='chat-bubble-ai'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Camera toggle logic
if "camera_active" not in st.session_state:
    st.session_state.camera_active = False

if st.session_state.camera_active:
    camera_image = st.camera_input("Capture an image", label_visibility="collapsed")
else:
    camera_image = None

# Input box
st.markdown(
    """
    <div class="input-container">
        <input id="text_input" class="input-box" type="text" placeholder="Type your message..." />
        <button class="camera-button" onclick="toggleCamera()">📷</button>
        <button class="send-button" onclick="sendMessage()">➤</button>
    </div>
    """,
    unsafe_allow_html=True,
)

# JavaScript for camera toggle and sending a message
st.markdown(
    """
    <script>
        let cameraActive = false;

        function toggleCamera() {
            cameraActive = !cameraActive;
            const camera = document.querySelector('.hidden-camera');
            if (camera) {
                camera.style.display = cameraActive ? 'block' : 'none';
            }
        }

        function sendMessage() {
            const input = document.getElementById('text_input');
            if (input.value.trim() !== "") {
                document.querySelector('button[type="submit"]').click();
            }
        }
    </script>
    """,
    unsafe_allow_html=True,
)

# Input handling
user_input = st.text_input("Enter your message:", key="text_input", label_visibility="collapsed")
uploaded_image = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if st.button("Send"):
    if user_input.strip():
        st.session_state.messages.append({"is_user": True, "content": user_input})
        image = None

        # Handle image input
        if camera_image:
            image = Image.open(camera_image)
        elif uploaded_image:
            image = Image.open(uploaded_image)

        # Get AI response
        ai_response = get_data(user_input, image)
        st.session_state.messages.append({"is_user": False, "content": ai_response})
    else:
        st.warning("Please enter a message.")
