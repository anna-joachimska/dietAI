import streamlit as st
import base64
from ai import vision

st.title("Identify your food")
st.write("Take a picture of your food and get nutritional info about it")

col1, col2 = st.columns([1,2])

with col1:
    enable_camera = st.checkbox("Enable camera")
    picture = st.camera_input("Take a picture", disabled=not enable_camera)

with col2:
    if picture:
        image_data = base64.b64encode(picture.getvalue()).decode("utf-8")
        st.markdown(vision.generate_response(image_data))