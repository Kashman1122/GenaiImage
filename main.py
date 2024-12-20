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
  margin: 0;
  padding: 0;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #121212;
  color: white;
  font-family: Arial, sans-serif;
}

.chat-container {
  width: 80%;
  max-width: 800px;
  height: 90vh;
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
}

.camera-button, .send-button {
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.camera-button {
  background-color: #4caf50;
  color: white;
  margin-right: 5px;
}

.send-button {
  background-color: #2196f3;
  color: white;
}

.chat-input-area .camera-button:hover {
  background-color: #45a049;
}

.chat-input-area .send-button:hover {
  background-color: #0b7dda;
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
