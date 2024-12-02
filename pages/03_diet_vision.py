import streamlit as st
import base64
from ai import vision

st.title("Identify your food")
st.write("Take a picture of your food or upload a picture of it and get nutritional info about it")

col1, col2 = st.columns([1,2])

with col1:
    enable_camera = st.checkbox("Enable camera")
    camera_picture = st.camera_input("Take a picture", disabled=not enable_camera)
    uploaded_picture = st.file_uploader("Upload a picture")


with col2:
    if camera_picture:
        image_data = base64.b64encode(camera_picture.getvalue()).decode("utf-8")
        st.markdown(vision.generate_response(image_data))
    elif uploaded_picture:
        image_data = base64.b64encode(uploaded_picture.getvalue()).decode("utf-8")
        st.markdown(vision.generate_response(image_data))
