import cv2
import numpy as np
import streamlit as st
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import load_model

# Load your trained model
model = load_model('/Users/abhinavyadav/Downloads/DSMP 1.0/eye_detection.h5')
IMG_SIZE = 224  # Resize the image to the input size of your model (e.g., 224x224)

# Streamlit App Title
st.title("👁️ Real-Time Eye Detection")
st.write("Detect whether eyes are open or closed in real-time using your webcam.")

# Sidebar
st.sidebar.title("🔧 Controls")
run = st.sidebar.checkbox("Start Webcam")
st.sidebar.write("Toggle the checkbox to start/stop the webcam.")
st.sidebar.write("Press 'Stop' to end the app.")
st.sidebar.info("Tip: Ensure your webcam is properly connected and accessible.")

# Create a container for video feed (first row)
with st.container():
    st.header("📹 Webcam Feed")
    FRAME_WINDOW = st.image([])

# Create a container for status display (second row)
with st.container():
    st.header("🔍 Eye Status")
    status_placeholder = st.markdown("**Status:** Waiting for webcam input...")

# Initialize webcam
cap = cv2.VideoCapture(0)

while run:
    ret, frame = cap.read()
    if not ret:
        status_placeholder.error("Failed to capture image. Please check your webcam.")
        break

    # Convert frame to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Resize the frame for model input
    img_resized = cv2.resize(frame_rgb, (IMG_SIZE, IMG_SIZE))

    # Preprocess the image
    img_array = img_to_array(img_resized) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # Predict eye status
    prediction = model.predict(img_array)

    # Update prediction status
    if prediction[0][0] > 0.8:
        status = "Eye is Open 👀"
        status_color = "green"
    else:
        status = "Eye is Closed 😴"
        status_color = "red"

    # Update UI with the prediction status
    status_placeholder.markdown(f"**Status:** <span style='color:{status_color}'>{status}</span>", unsafe_allow_html=True)

    # Display the video feed
    FRAME_WINDOW.image(frame_rgb)

# Release resources when the checkbox is unchecked
cap.release()
cv2.destroyAllWindows()
